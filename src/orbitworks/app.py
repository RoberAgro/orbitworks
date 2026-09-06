"""OrbitWorks v3: wide launch ranges and a compact, direct-manipulation UI.

Run ``poetry run python app/app_v3.py`` and open http://127.0.0.1:8052.
The earlier apps and their assets are independent and remain unchanged.
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
PORT = 8052
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
    "angle": 0.0,
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

    At radius r, vc=sqrt(GM/r). With alpha measured from the counterclockwise
    local horizontal, v = speed_ratio*vc*(sin(alpha)*e_r+cos(alpha)*e_theta).
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
    radial = np.array([x, y]) / radius
    tangent = np.array([-radial[1], radial[0]])
    alpha = np.deg2rad(angle)
    velocity = (
        speed_ratio / sqrt(radius) * (np.sin(alpha) * radial + np.cos(alpha) * tangent)
    )
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


app = Dash(__name__, assets_folder=str(Path(__file__).parent / "assets_v3"))
app.title = "OrbitWorks"
server = app.server


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
                "outerRadius": OUTER_RADIUS,
                "maxRatio": MAXIMUM_SPEED_RATIO,
                "maxRate": MAXIMUM_PLAYBACK_RATE,
                "defaults": DEFAULTS,
            },
        ),
        html.Div(id="client-ready", hidden=True),
        html.Aside(
            [
                html.H1("OrbitWorks"),
                html.P("Place it, Aim it, Let gravity take over", className="subtitle"),
                html.Div(
                    [
                        html.Div(id="x-control", className="control"),
                        html.Div(id="y-control", className="control"),
                        html.Div(id="ratio-control", className="control"),
                        html.Div(id="angle-control", className="control"),
                    ],
                    className="launch-controls",
                ),
                html.Div(id="launch-validity", role="status", className="validation"),
                button(
                    "Launch", "fire", "Launch (F), or double-click the launcher base"
                ),
                html.Div(id="launch-message", role="status", className="message"),
                html.Div(
                    [
                        html.Div(id="rate-control", className="control"),
                        html.Div(
                            [
                                button("Pause", "pause", "Pause/resume (Space)"),
                                button(
                                    "Clear all",
                                    "clear",
                                    "Remove flights and reset the clock",
                                ),
                            ],
                            className="button-row",
                        ),
                    ],
                    className="time-controls",
                ),
            ],
            className="sidebar",
        ),
        html.Main(
            [
                html.Header(
                    [
                        html.Div(
                            [html.Span(className="live-dot"), "LIVE"],
                            className="scene-label",
                        ),
                        html.Div(id="simulation-clock", className="clock"),
                    ],
                    className="scene-header",
                ),
                html.Div(
                    [
                        button("Centre Earth", "centre", "Return to Earth (Home)"),
                        button(
                            "Fit trails", "fit", "Fit only the paths travelled so far"
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
                            "Mouse, keyboard and model guide (?)",
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
                    [html.H2("Flights"), html.Span("0", id="flight-count")],
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
                        html.H2("OrbitWorks · Help"),
                        button("Close ✕", "close-help", "Close (Escape)"),
                    ],
                    className="log-heading",
                ),
                html.Dl(
                    [
                        html.Dt("Place / move"),
                        html.Dd("Left-click empty space or drag the launcher base."),
                        html.Dt("Aim & speed"),
                        html.Dd(
                            "Drag the arrowhead: direction sets the angle, length sets v/vc. Shift + wheel adjusts only the angle."
                        ),
                        html.Dt("Launch"),
                        html.Dd(
                            "Double-click the launcher base, click Launch, or press F. Double-clicking empty space only positions the launcher."
                        ),
                        html.Dt("Zoom / pan"),
                        html.Dd(
                            "Scroll to zoom. Right-drag to pan and release Follow mode."
                        ),
                        html.Dt("Navigate"),
                        html.Dd(
                            "Centre Earth (Home), Fit trails, or select a flight and Follow selected."
                        ),
                        html.Dt("Time"),
                        html.Dd(
                            "Space pauses/resumes. The time multiplier slider is logarithmic; its value is simulated seconds per real second."
                        ),
                    ]
                ),
                html.H3("Scales"),
                html.P(
                    "x and y each span −10,000 to +10,000 Earth radii. Use the number boxes or scene dragging for precise near-Earth placement. Angle is relative to the local counterclockwise horizontal: 0° tangential, +90° outward, −90° inward."
                ),
                html.P(
                    "Moving the launcher preserves v/vc, where vc = √(GM/r). The actual km/s value is shown beside Speed. Ratio 1 gives a circle only with tangential aim; √2 is escape speed."
                ),
                html.H3("Model"),
                html.P(
                    "Independent projectiles around a stationary Earth, without air resistance. The dashed preview ends at contact or the distance boundary. Numerical flights stop at impact, 100,000 Earth radii, or 1,000 simulated years. Complete bound orbits replay one computed period. At high playback speeds, short-period orbits can appear to skip between frames."
                ),
                html.P(
                    "The arrow uses screen length to represent normalized speed, so zooming never changes your launch settings. Shortcuts are inactive while typing. Inputs, trajectories and camera state belong to this browser tab."
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
    ClientsideFunction(namespace="cannonV3", function_name="update"),
    Output("client-ready", "children"),
    Input("scene-config", "data"),
    Input("flight-result", "data"),
)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
