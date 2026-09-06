"""ORBITWORKS: practical sliders, compact controls, and live connection status.

Run ``poetry run python -m orbitworks.app`` and open http://127.0.0.1:8054.
This module and its adjacent assets are the current application. For a local
launcher that also opens the browser, use ``orbitworks.launch_app()``.
"""

from math import hypot, pi, sqrt
from pathlib import Path
from uuid import uuid4

import numpy as np
from dash import ClientsideFunction, Dash, Input, Output, dcc, html
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from orbitworks.constants import MU_EARTH, R_EARTH, YEAR

# SI constants; launch controls measure x/y in Earth radii and speed in local vc.
HOST = "127.0.0.1"
PORT = 8054
DEBUG = False
POSITION_LIMIT = 10000.0
OUTER_RADIUS = 100000.0  # Earth radii; comfortably beyond all launch positions.
MAXIMUM_FLIGHT_TIME = 1000.0 * YEAR
MINIMUM_ALTITUDE = 1.0  # metres above the surface
MAXIMUM_SPEED_RATIO = 3.0
MAXIMUM_PLAYBACK_RATE = 1e10
RELATIVE_TOLERANCE = 1e-10
ABSOLUTE_TOLERANCE = 1e-12
SAMPLE_COUNT = 3000
TIME_UNIT = sqrt(R_EARTH**3 / MU_EARTH)
SPEED_UNIT = sqrt(MU_EARTH / R_EARTH)
DEFAULTS = {
    "x": 1.0 + 500000.0 / R_EARTH,
    "y": 0.0,
    "ratio": 1.0,
    "angle": 90.0,
    "rate": 2000.0,
}


def gravity_equations(time, state):
    """Evaluate dr/dt=v and dv/dt=-r/|r|^3 with GM=1 in scaled coordinates.

    Length is scaled by Earth's radius and time by sqrt(R^3/GM), as in the
    previous versions. DOP853 chooses its internal steps adaptively.
    """
    radius = np.linalg.norm(state[:2])
    return np.concatenate((state[2:], -state[:2] / radius**3))


def impact_event(time, state):
    """Stop at the first inward crossing of Earth's surface."""
    return np.linalg.norm(state[:2]) - 1.0


impact_event.terminal = True
impact_event.direction = -1


def outer_event(time, state):
    """Stop at the game boundary; this does not imply positive orbital energy."""
    return np.linalg.norm(state[:2]) - OUTER_RADIUS


outer_event.terminal = True
outer_event.direction = 1


def periapsis_event(time, state):
    """Locate an inward-to-outward radial turn for a predicted colliding orbit.

    A grazing trajectory can cross the surface twice within one large solver
    step. Its radial turn brackets the first impact even if the ordinary
    impact event misses that short interval. Using this event avoids imposing
    a tiny global step on flights starting thousands of Earth radii away.
    """
    return np.dot(state[:2], state[2:])


periapsis_event.terminal = True
periapsis_event.direction = 1


def compute_positioned_flight(x, y, speed_ratio, angle):
    """Calculate one flight from scaled position, local speed ratio and angle.

    At radius r, vc=sqrt(GM/r). Angle alpha is measured counterclockwise
    from the positive x-axis: v = speed_ratio*vc*(cos(alpha), sin(alpha)).
    Its direction is independent of the launcher's position.
    The ratio is preserved while positioning the launcher, not the SI speed.

    In dimensionless variables, energy=|v|^2/2-1/r, ell=x*vy-y*vx, and
    e_vector=(|v|^2-1/r)*r_vector-(r_vector.v)*v. Negative energy gives
    a=-1/(2*energy) and T=2*pi*a^(3/2). A completed bound orbit can replay
    its numerical period; impacts, boundary stops, and time caps cannot.
    """
    values = (x, y, speed_ratio, angle)
    if any(v is None for v in values) or not np.all(np.isfinite(values)):
        raise ValueError("Enter a finite value in each launch field.")
    if abs(x) > POSITION_LIMIT or abs(y) > POSITION_LIMIT:
        raise ValueError(
            "Each coordinate must lie between −10,000 and +10,000 Earth radii."
        )
    radius = hypot(x, y)
    if radius < 1.0 + MINIMUM_ALTITUDE / R_EARTH:
        raise ValueError("Place the launcher at least 1 metre above Earth's surface.")
    if not 0 <= speed_ratio <= MAXIMUM_SPEED_RATIO or not -180 <= angle <= 180:
        raise ValueError(
            "Use a speed ratio from 0 to 3 and an angle from −180° to 180°."
        )
    alpha = np.deg2rad(angle)
    velocity = speed_ratio / sqrt(radius) * np.array([np.cos(alpha), np.sin(alpha)])
    state = np.concatenate(([x, y], velocity))
    energy = float(np.dot(velocity, velocity) / 2 - 1 / radius)
    ell = x * velocity[1] - y * velocity[0]
    eccentricity_vector = (np.dot(velocity, velocity) - 1 / radius) * state[
        :2
    ] - np.dot(state[:2], velocity) * velocity
    eccentricity = float(np.linalg.norm(eccentricity_vector))
    parabolic = abs(energy) < 1e-12 / radius
    bound = energy < 0 and not parabolic
    axis = -1 / (2 * energy) if not parabolic else None
    period = 2 * pi * axis**1.5 if bound else None
    if abs(ell) < 1e-10:
        orbit_type = "Radial · " + ("bound" if bound else "unbound")
    else:
        orbit_type = (
            "Parabolic"
            if parabolic
            else (
                ("Circular" if eccentricity < 1e-8 else "Elliptical")
                if bound
                else "Hyperbolic"
            )
        )
    periapsis = ell**2 / (1 + eccentricity)
    time_cap = MAXIMUM_FLIGHT_TIME / TIME_UNIT
    duration = min(period, time_cap) if bound else time_cap
    events = [impact_event, outer_event]
    # No radial turn is needed for a zero-angular-momentum impact: the normal
    # event is reached before the point-mass singularity.
    if periapsis < 1 and abs(ell) > 1e-10:
        events.append(periapsis_event)
    result = solve_ivp(
        gravity_equations,
        (0, duration),
        state,
        method="DOP853",
        rtol=RELATIVE_TOLERANCE,
        atol=ABSOLUTE_TOLERANCE,
        dense_output=True,
        events=events,
    )
    if not result.success:
        raise ValueError(f"Integration could not finish: {result.message}")
    end_time = result.t[-1]
    if result.t_events[0].size:
        outcome = "impact"
    elif result.t_events[1].size:
        outcome = "out of range"
    elif len(events) == 3 and result.t_events[2].size:
        # Bracket a possibly missed shallow contact between launch and the
        # terminal radial turn. Refine on the solver's continuous interpolant.
        if np.linalg.norm(result.y[:2, -1]) > 1:
            raise ValueError(
                "This grazing contact is below numerical resolution; adjust the angle slightly."
            )
        end_time = brentq(
            lambda t: np.linalg.norm(result.sol(t)[:2]) - 1, 0, end_time, xtol=1e-12
        )
        outcome = "impact"
    else:
        outcome = "orbiting" if bound and period <= time_cap else "time limit"
    time = np.unique(
        np.concatenate(
            (result.t[result.t < end_time], np.linspace(0, end_time, SAMPLE_COUNT))
        )
    )
    states = result.sol(time).T
    energies = np.sum(states[:, 2:] ** 2, axis=1) / 2 - 1 / np.linalg.norm(
        states[:, :2], axis=1
    )
    energy_scale = 1 / radius if parabolic else abs(energy)
    return {
        "id": uuid4().hex,
        "orbit_type": orbit_type,
        "eccentricity": eccentricity,
        "outcome": outcome,
        "repeat": outcome == "orbiting",
        "duration": float(end_time * TIME_UNIT),
        "period": period * TIME_UNIT if period is not None else None,
        "launch_x": x,
        "launch_y": y,
        "speed_ratio": speed_ratio,
        "speed": speed_ratio / sqrt(radius) * SPEED_UNIT / 1000,
        "angle": angle,
        "altitude": (radius - 1) * R_EARTH / 1000,
        "periapsis": float(periapsis),
        "apoapsis": float(axis * (1 + eccentricity)) if bound else None,
        "specific_energy": energy * SPEED_UNIT**2,
        "energy_error": float(100 * np.max(np.abs(energies - energy)) / energy_scale),
        "energy_normalization": "GM/r₀" if parabolic else "|initial energy|",
        "time": (time * TIME_UNIT).tolist(),
        "x": states[:, 0].tolist(),
        "y": states[:, 1].tolist(),
        "vx": (states[:, 2] / TIME_UNIT).tolist(),
        "vy": (states[:, 3] / TIME_UNIT).tolist(),
    }


app = Dash(
    __name__,
    assets_folder=str(Path(__file__).parent / "assets"),
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Google+Sans:wght@400..700&display=swap"
    ],
)
app.title = "ORBITWORKS"
server = app.server


@server.get("/health")
def health():
    """Let the browser detect a stopped server without disturbing flight state."""
    return {"app": "orbitworks", "status": "ok"}, 200, {"Cache-Control": "no-store"}


def button(text, identifier, hint):
    """Provide a visible action with an unobtrusive hover description."""
    return html.Button(text, id=identifier, title=hint, type="button")


app.layout = html.Div(
    [
        dcc.Store(id="launch-request"),
        dcc.Store(id="flight-result"),
        dcc.Store(
            id="scene-config",
            data={
                "radiusKm": R_EARTH / 1000,
                "gm": MU_EARTH,
                "minRadius": 1 + MINIMUM_ALTITUDE / R_EARTH,
                "positionLimit": POSITION_LIMIT,
                "positionSliderLimit": 10.0,
                "outerRadius": OUTER_RADIUS,
                "maxRatio": MAXIMUM_SPEED_RATIO,
                "maxRate": MAXIMUM_PLAYBACK_RATE,
                "defaults": DEFAULTS,
            },
        ),
        html.Div(id="client-ready", hidden=True),
        html.Aside(
            [
                html.H1("OrbitWorks", className="wordmark"),
                html.P(
                    "Place it, aim it, and let gravity take over!", className="subtitle"
                ),
                html.Div(
                    [
                        html.Div(id="x-control", className="control"),
                        html.Div(id="y-control", className="control"),
                        html.Div(id="ratio-control", className="control"),
                        html.Div(id="angle-control", className="control"),
                        html.Div(id="rate-control", className="control"),
                    ],
                    className="launch-controls",
                ),
                html.Div(
                    [
                        button("Pause", "pause", "Pause/resume (Space)"),
                        button(
                            "Clear all", "clear", "Remove flights and reset the clock"
                        ),
                    ],
                    className="button-row",
                ),
                html.Div(
                    [
                        html.Div(
                            id="launch-validity", role="status", className="validation"
                        ),
                        html.Div(
                            id="launch-message", role="status", className="message"
                        ),
                        button(
                            "Launch",
                            "fire",
                            "Press F to launch, or double-click the launcher base",
                        ),
                    ],
                    className="launch-footer",
                ),
            ],
            className="sidebar",
        ),
        html.Main(
            [
                html.Header(
                    [
                        html.Div(
                            [
                                html.Span(className="live-dot"),
                                html.Span("Connecting", id="simulation-status-label"),
                            ],
                            id="simulation-status",
                            className="scene-label",
                            role="status",
                            **{"data-state": "connecting"},
                        ),
                    ],
                    className="scene-header",
                ),
                html.Div(
                    [
                        button("Centre Earth", "centre", "Return to Earth (Home)"),
                        button(
                            "Show all trajectories",
                            "fit",
                            "Fit only the paths travelled so far",
                        ),
                        button(
                            "Follow selected",
                            "follow",
                            "Follow a selected flight; pan to release",
                        ),
                        button("−", "zoom-out", "Zoom out"),
                        button("+", "zoom-in", "Zoom in"),
                        button(
                            "Help",
                            "controls-help",
                            "Mouse, keyboard and model guide (H)",
                        ),
                    ],
                    className="toolbar",
                ),
                html.Div(
                    [
                        html.Canvas(
                            id="orbit-canvas",
                            tabIndex=0,
                            **{
                                "aria-label": "Interactive OrbitWorks scene. Use Help for controls."
                            },
                        ),
                        html.Div(id="view-scale", className="view-scale"),
                        html.Div(id="simulation-clock", className="clock"),
                        html.Div(id="preview-label", className="preview-label"),
                        html.Div(
                            "Drag the arrow to aim & set speed · double-click the launcher to fire",
                            className="scene-hint",
                        ),
                    ],
                    className="canvas-container",
                ),
                html.Div(id="camera-status", className="camera-status"),
            ],
            className="main-panel",
        ),
        html.Aside(
            [
                html.Div(
                    [html.H2("Flights log"), html.Span("0", id="flight-count")],
                    className="log-heading",
                ),
                html.Div(
                    "Your flights will appear here.",
                    id="empty-log",
                    className="empty-log",
                ),
                html.Div(id="flight-log", className="flight-log"),
            ],
            className="flight-panel",
        ),
        html.Dialog(
            [
                html.Div(
                    [
                        html.H2("ORBITWORKS · Help"),
                        button("Close ✕", "close-help", "Close (Escape)"),
                    ],
                    className="log-heading",
                ),
                html.H3("Controls"),
                html.Dl(
                    [
                        html.Dt("Place"),
                        html.Dd(
                            "Left-click an empty spot in the scene to place the launcher."
                        ),
                        html.Dt("Move"),
                        html.Dd(
                            "Drag the round base of the launcher to a new position."
                        ),
                        html.Dt("Aim"),
                        html.Dd(
                            "Drag the arrowhead around the launcher to choose a direction."
                        ),
                        html.Dt("Angle only"),
                        html.Dd(
                            "Hold Shift and scroll the mouse wheel over the scene to rotate the arrow without changing speed or zoom. Scroll up to turn counterclockwise; scroll down to turn clockwise."
                        ),
                        html.Dt("Speed"),
                        html.Dd(
                            "Drag the arrowhead farther from the launcher to increase speed, or closer to reduce it."
                        ),
                        html.Dt("Launch"),
                        html.Dd(
                            "Double-click the round launcher base to fire a new projectile."
                        ),
                        html.Dt("Launch key"),
                        html.Dd("Press F to fire a new projectile."),
                        html.Dt("Zoom"),
                        html.Dd("Scroll the mouse wheel to zoom in or out."),
                        html.Dt("Pan"),
                        html.Dd(
                            "Hold the right mouse button and drag to move around the scene."
                        ),
                        html.Dt("Time"),
                        html.Dd("Press the space bar to pause or resume the motion."),
                        html.Dt("Centre key"),
                        html.Dd(
                            "Press Home to bring Earth back to the centre of the view."
                        ),
                        html.Dt("Help key"),
                        html.Dd("Press H to open this guide, and Escape to close it."),
                    ]
                ),
                html.H3("Left panel"),
                html.Dl(
                    [
                        html.Dt("Horizontal position"),
                        html.Dd(
                            "Choose how far left or right to place the launcher, in Earth radii. Negative values are left of Earth; positive values are right."
                        ),
                        html.Dt("Vertical position"),
                        html.Dd(
                            "Choose how far below or above Earth to place the launcher, in Earth radii. Negative values are below Earth; positive values are above."
                        ),
                        html.Dt("Position boxes"),
                        html.Dd(
                            "The position sliders cover −10 to +10 Earth radii. Use the number boxes or drag in the scene for more distant positions, up to ±10,000. The launcher must be outside Earth."
                        ),
                        html.Dt("Launch speed"),
                        html.Dd(
                            "Choose the speed relative to the circular-orbit speed at the launch position. A value of 1 can give a circle when aimed sideways around Earth; about 1.4142 is escape speed. The actual speed is also shown in km/s."
                        ),
                        html.Dt("Launch angle"),
                        html.Dd(
                            "Set the direction in degrees, measured counterclockwise from the right: 0° points right and 90° points up."
                        ),
                        html.Dt("Time multiplier"),
                        html.Dd(
                            "Choose how quickly time passes. A value of 1 is real time; 2,000 means 2,000 seconds of motion for each second you watch. Higher values help you watch distant flights."
                        ),
                        html.Dt("Pause / Resume"),
                        html.Dd(
                            "Stop the motion temporarily, or continue from where you paused."
                        ),
                        html.Dt("Clear all"),
                        html.Dd("Remove every flight and reset the elapsed time."),
                        html.Dt("Launch"),
                        html.Dd(
                            "Fire a new projectile using the current settings. You can change the settings and launch again while existing flights continue."
                        ),
                    ]
                ),
                html.H3("Top buttons"),
                html.Dl(
                    [
                        html.Dt("Centre Earth"),
                        html.Dd(
                            "Bring Earth back to the centre at a comfortable zoom level."
                        ),
                        html.Dt("Show all trajectories"),
                        html.Dd(
                            "Adjust the view to include Earth, the launcher and the paths your projectiles have travelled."
                        ),
                        html.Dt("Follow selected"),
                        html.Dd(
                            "Keep the selected projectile in view as it moves. Click again to stop following."
                        ),
                        html.Dt("−"),
                        html.Dd("Zoom out to see a larger area."),
                        html.Dt("+"),
                        html.Dd("Zoom in for a closer look."),
                        html.Dt("Help"),
                        html.Dd("Open this guide."),
                    ]
                ),
                html.H3("Flights log"),
                html.Dl(
                    [
                        html.Dt("Select"),
                        html.Dd(
                            "Each shot creates a coloured card on the right. Click its heading to highlight that flight. Its colour matches its path in the scene."
                        ),
                        html.Dt("Status"),
                        html.Dd(
                            "The badge tells you whether a projectile is flying, has hit Earth, or has reached a calculation limit."
                        ),
                        html.Dt("Details"),
                        html.Dd(
                            "Open a flight's information, including its distance, age, launch settings and orbit shape. Period is the time for one complete orbit; periapsis and apoapsis are the nearest and farthest distances from Earth's centre."
                        ),
                        html.Dt("Hide / Show"),
                        html.Dd(
                            "Hide a flight's path and marker to reduce clutter, or show them again. Hiding does not delete the flight."
                        ),
                        html.Dt("×"),
                        html.Dd("Remove that flight from the scene and log."),
                        html.Dt("More flights"),
                        html.Dd(
                            "Scroll the log to find earlier shots. Select a flight, then use Follow selected above the scene to watch it."
                        ),
                    ]
                ),
                html.H3("Technical details"),
                html.P(
                    "Earth is a stationary, perfectly spherical body. Projectiles move under its gravity alone: there is no atmosphere, no force from the Sun or Moon, and no attraction or collisions between projectiles. A projectile stops when it reaches Earth's surface."
                ),
                html.P(
                    "The paths are calculated using Newton's law of gravity and a numerical method that adjusts its time steps for accuracy. The thin dashed line predicts the next shot's path. Calculations end at impact, at 100,000 Earth radii, or after 1,000 simulated years; a complete bound orbit needs only one period to be calculated."
                ),
            ],
            id="controls-dialog",
            **{"aria-labelledby": "controls-help"},
        ),
    ],
    className="app-shell",
)


@app.callback(
    Output("flight-result", "data"),
    Input("launch-request", "data"),
    prevent_initial_call=True,
)
def fire_projectile(request):
    """Compute a captured launch; its epoch discards stale results after Clear."""
    envelope = {"epoch": request["epoch"], "request_id": request["id"]}
    try:
        flight = compute_positioned_flight(
            request.get("x"),
            request.get("y"),
            request.get("ratio"),
            request.get("angle"),
        )
        return dict(envelope, flight=flight)
    except ValueError as error:
        return dict(envelope, error=str(error))


app.clientside_callback(
    ClientsideFunction(namespace="orbitworks", function_name="update"),
    Output("client-ready", "children"),
    Input("scene-config", "data"),
    Input("flight-result", "data"),
)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
