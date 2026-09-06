"""Integrate circular, elliptical, parabolic, or hyperbolic Kepler orbits.

This calls the shared core functions in ``orbitworks.numerical``,
``orbitworks.analytical`` and ``orbitworks.geometry`` instead of
reimplementing them locally. Those same functions also back
``orbitworks.app``, so both this script and the app run one tested
implementation of the equations of motion, orbital-element classification and
conic-shape sampling. Only script-specific orchestration (choosing an
integration duration, wrapping the result, printing a report, and plotting)
stays local, alongside ``OrbitSolution``, which is bookkeeping for this
script's plots rather than a core physics result.

The initial Cartesian state determines the conic; the integrator does not need
to be told which orbit type to expect. Specific orbital energy classifies the
result as bound, parabolic, or unbound, while the angular momentum and
eccentricity vector determine the corresponding analytical conic.

Bound integrations have a known period and therefore use a final time equal to
``NUMBER_OF_PERIODS`` periods. Open trajectories have no period. For them, a
terminal SciPy event stops integration when the body crosses ``ESCAPE_RADIUS``.
A second terminal event stops any trajectory that hits the central body.
"""

from math import pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle

from orbitworks import analytical, geometry, numerical
from orbitworks.constants import R_EARTH, MU_EARTH
from orbitworks.graphics_mpl import set_plot_options

# User configuration.
GRAVITATIONAL_PARAMETER = MU_EARTH
CENTRAL_BODY_RADIUS = R_EARTH
INITIAL_RADIUS = 4.0 * R_EARTH

# Velocity components relative to the circular speed at INITIAL_RADIUS.
# Useful tangential values with zero radial speed are:
#   circle:    1.0
#   ellipse:   sqrt(1.5)
#   parabola:  sqrt(2.0)
#   hyperbola: sqrt(2.5)
INITIAL_RADIAL_SPEED_RATIO = 0.0
INITIAL_TANGENTIAL_SPEED_RATIO = sqrt(1.5)

NUMBER_OF_PERIODS = 2.0
ESCAPE_RADIUS = 20.0 * INITIAL_RADIUS
UNBOUND_TIME_LIMIT_IN_LOCAL_PERIODS = 20.0
OUTPUT_POINTS = 8_000
INTEGRATION_METHOD = "DOP853"
RELATIVE_TOLERANCE = 1e-10
ABSOLUTE_TOLERANCE = 1e-8

# Matches orbitworks.analytical.classify_orbit's defaults; named here since the
# report and error plot below refer to them directly.
ECCENTRICITY_TOLERANCE = 1e-8
ENERGY_TOLERANCE = 1e-10

ANALYTICAL_CURVE_POINTS = 2_000
ANIMATION_SECONDS_PER_PERIOD = 2.5
UNBOUND_ANIMATION_SECONDS = 5.0
ANIMATION_FPS = 40
SHOW_FIGURE = True
STATIC_FIGURE_PATH = None  # For example: "general_orbit.png"
ANIMATION_PATH = None  # For example: "general_orbit.gif"


class OrbitSolution:
    """Store sampled states, event information, and solver effort.

    This is presentation bookkeeping for this script (plots, report, GIF
    export), not a core physics result, so it stays local rather than moving
    to ``orbitworks.numerical``.
    """

    def __init__(
        self,
        time,
        position,
        velocity,
        termination_reason,
        function_evaluations,
    ):
        self.time = time
        self.position = position
        self.velocity = velocity
        self.termination_reason = termination_reason
        self.function_evaluations = function_evaluations


def initial_state():
    """Construct the configured Cartesian state at ``(INITIAL_RADIUS, 0)``.

    The velocity scale is the local circular speed

        v_c = sqrt(GM/r_0).

    Radial velocity lies along +x and tangential velocity along +y. With zero
    radial speed, tangential ratios 1 and sqrt(2) are respectively the circular
    and escape speeds. Values between them give ellipses; larger values give
    hyperbolas.
    """
    circular_speed = sqrt(GRAVITATIONAL_PARAMETER / INITIAL_RADIUS)
    position = np.array([INITIAL_RADIUS, 0.0])
    velocity = circular_speed * np.array(
        [INITIAL_RADIAL_SPEED_RATIO, INITIAL_TANGENTIAL_SPEED_RATIO]
    )
    return np.concatenate((position, velocity))


def integration_duration(elements):
    """Choose a known bound duration or a safety limit for an open orbit.

    Elliptical motion has a calculable period, so no period-counting event is
    required. Open motion has no period; its time span is merely a safety cap,
    and the escape-radius event normally terminates it first.
    """
    if elements.is_bound:
        return NUMBER_OF_PERIODS * elements.period

    local_period = 2.0 * pi * sqrt(INITIAL_RADIUS**3 / GRAVITATIONAL_PARAMETER)
    return UNBOUND_TIME_LIMIT_IN_LOCAL_PERIODS * local_period


def append_terminal_event(result, event_index):
    """Append an exact terminal-event state if it lies beyond the output grid."""
    if len(result.t_events[event_index]) == 0:
        return result.t, result.y

    event_time = result.t_events[event_index][-1]
    event_state = result.y_events[event_index][-1]
    if np.isclose(event_time, result.t[-1], rtol=0.0, atol=1e-12):
        return result.t, result.y
    return (
        np.append(result.t, event_time),
        np.column_stack((result.y, event_state)),
    )


def integrate_orbit(state, elements):
    """Integrate adaptively until the time limit, escape, or collision.

    Bound trajectories use only the collision event because their specified
    final time already represents the requested number of periods. Parabolic
    and hyperbolic trajectories additionally use the terminal escape event.
    """
    duration = integration_duration(elements)
    output_time = np.linspace(0.0, duration, OUTPUT_POINTS)
    events = [numerical.make_collision_event(CENTRAL_BODY_RADIUS)]
    if not elements.is_bound:
        events.append(numerical.make_escape_event(ESCAPE_RADIUS))

    result = numerical.propagate(
        state,
        GRAVITATIONAL_PARAMETER,
        duration,
        events=events,
        method=INTEGRATION_METHOD,
        rtol=RELATIVE_TOLERANCE,
        atol=ABSOLUTE_TOLERANCE,
        dense_output=False,
        t_eval=output_time,
    )

    termination_reason = "configured final time"
    terminal_event_index = None
    if len(result.t_events[0]) > 0:
        termination_reason = "collision radius reached"
        terminal_event_index = 0
    elif len(events) > 1 and len(result.t_events[1]) > 0:
        termination_reason = "escape radius reached"
        terminal_event_index = 1

    time = result.t
    states = result.y
    if terminal_event_index is not None:
        time, states = append_terminal_event(result, terminal_event_index)

    return OrbitSolution(
        time,
        states[:2].T,
        states[2:].T,
        termination_reason,
        result.nfev,
    )


def sample_analytical_conic(elements):
    """Sample the invariant conic, oriented by its eccentricity vector.

    Closed conics are sampled for a full revolution. Open branches are sampled
    only as far as ``ESCAPE_RADIUS`` so the analytical and numerical paths have
    the same visible scale.
    """
    angle_limit = None
    if not elements.is_bound:
        angle_limit = geometry.angle_limit_for_radius(
            elements.eccentricity, elements.semi_latus_rectum, ESCAPE_RADIUS
        )
    return geometry.sample_conic(
        elements, angle_limit=angle_limit, num_points=ANALYTICAL_CURVE_POINTS
    )


def calculate_percentage_errors(solution, elements):
    """Calculate conservation and analytical conic errors in percent."""
    if elements.orbit_type != "parabola":
        scale = None
    else:
        # A parabolic orbit has zero energy, so division by its reference value
        # is undefined. Normalize by the local gravitational-energy scale.
        scale = GRAVITATIONAL_PARAMETER / INITIAL_RADIUS

    return {
        "energy": analytical.energy_error(
            solution.position, solution.velocity, GRAVITATIONAL_PARAMETER, elements, scale=scale
        ),
        "angular momentum": analytical.angular_momentum_error(
            solution.position, solution.velocity, elements
        ),
        "eccentricity vector": analytical.eccentricity_vector_error(
            solution.position, solution.velocity, GRAVITATIONAL_PARAMETER, elements
        ),
        "conic shape": geometry.conic_shape_error(solution.position, elements),
    }


def print_report(elements, solution, errors):
    """Print the inferred orbit and numerical-quality diagnostics."""
    print(f"Orbit type: {elements.orbit_type}")
    print(f"Eccentricity: {elements.eccentricity:.8f}")
    print(f"Specific energy: {elements.specific_energy:.6e} J/kg")
    print(
        "Specific angular momentum: "
        f"{elements.specific_angular_momentum:.6e} m^2/s"
    )
    if elements.period is not None:
        print(f"Orbital period: {elements.period / 3600.0:.6f} h")
        print(f"Integrated periods: {solution.time[-1] / elements.period:.6f}")
    print(f"Termination: {solution.termination_reason}")
    print(f"ODE right-hand-side evaluations: {solution.function_evaluations}")
    for name, values in errors.items():
        print(f"Maximum relative {name} deviation: {np.max(values):.3e} %")


def orbit_adjective(orbit_type):
    """Return the adjective used to label each conic trajectory."""
    return {
        "circle": "Circular",
        "ellipse": "Elliptical",
        "parabola": "Parabolic",
        "hyperbola": "Hyperbolic",
    }[orbit_type]


def create_visualization(solution, elements, analytical_conic, errors, animate):
    """Plot the numerical and analytical paths with conservation errors."""
    set_plot_options(fontsize=11, color_order="matlab", linewidth=1.5)
    figure, (orbit_axes, error_axes) = plt.subplots(
        1,
        2,
        figsize=(13, 6.5),
        constrained_layout=True,
    )

    scale = INITIAL_RADIUS
    numerical_path = solution.position / scale
    analytical_path = analytical_conic / scale
    central_radius = CENTRAL_BODY_RADIUS / scale
    orbit_axes.plot(
        analytical_path[:, 0],
        analytical_path[:, 1],
        "--",
        color="#555555",
        linewidth=2.0,
        label="analytical conic",
    )
    orbit_axes.plot(
        numerical_path[:, 0],
        numerical_path[:, 1],
        color="#0072BD",
        alpha=0.25,
        label="SciPy trajectory",
    )
    orbit_axes.add_patch(
        Circle(
            (0.0, 0.0),
            central_radius,
            facecolor="#4C78A8",
            edgecolor="#17365D",
            label="central body",
        )
    )
    (trail,) = orbit_axes.plot([], [], color="#0072BD", linewidth=2.2)
    (body,) = orbit_axes.plot([], [], "o", color="#D95319", markersize=7)
    orbit_title = orbit_axes.set_title("")
    orbit_axes.set_aspect("equal", adjustable="box")
    orbit_axes.set_xlabel("x / initial radius")
    orbit_axes.set_ylabel("y / initial radius")
    orbit_axes.legend(loc="best")

    floor = 100.0 * np.finfo(float).eps
    time_scale = (
        elements.period if elements.period is not None else solution.time[-1]
    )
    scaled_time = solution.time / time_scale
    time_label = "time / orbital period" if elements.is_bound else "time / final time"
    for name, values in errors.items():
        error_axes.semilogy(
            scaled_time,
            np.maximum(values, floor),
            label=name,
        )
    error_axes.set_xlabel(time_label)
    error_axes.set_ylabel("absolute relative deviation [%]")
    error_axes.set_title("Numerical error diagnostics")
    error_axes.legend(loc="best")

    if not animate:
        trail.set_data(numerical_path[:, 0], numerical_path[:, 1])
        body.set_data([numerical_path[-1, 0]], [numerical_path[-1, 1]])
        orbit_title.set_text(f"{orbit_adjective(elements.orbit_type)} orbit")
        return figure, None

    if elements.is_bound:
        animation_seconds = NUMBER_OF_PERIODS * ANIMATION_SECONDS_PER_PERIOD
    else:
        animation_seconds = UNBOUND_ANIMATION_SECONDS
    animation_frames = max(2, round(animation_seconds * ANIMATION_FPS))
    frame_indices = np.linspace(
        0,
        len(solution.time) - 1,
        animation_frames,
        dtype=int,
    )

    def initialize_animation():
        trail.set_data([], [])
        body.set_data([], [])
        orbit_title.set_text("")
        return trail, body, orbit_title

    def update_animation(frame_index):
        index = frame_indices[frame_index]
        trail.set_data(
            numerical_path[: index + 1, 0],
            numerical_path[: index + 1, 1],
        )
        body.set_data(
            [numerical_path[index, 0]],
            [numerical_path[index, 1]],
        )
        orbit_title.set_text(
            f"{orbit_adjective(elements.orbit_type)} orbit: "
            f"t = {scaled_time[index]:.2f} "
            f"{'periods' if elements.is_bound else 'of final time'}"
        )
        return trail, body, orbit_title

    orbit_animation = FuncAnimation(
        figure,
        update_animation,
        init_func=initialize_animation,
        frames=len(frame_indices),
        interval=1_000.0 / ANIMATION_FPS,
        blit=True,
        repeat=True,
    )
    return figure, orbit_animation


def validate_configuration():
    """Reject configurations that are singular or cannot be visualized."""
    if GRAVITATIONAL_PARAMETER <= 0.0:
        raise ValueError("GRAVITATIONAL_PARAMETER must be positive.")
    if not 0.0 < CENTRAL_BODY_RADIUS < INITIAL_RADIUS:
        raise ValueError("Require 0 < CENTRAL_BODY_RADIUS < INITIAL_RADIUS.")
    if ESCAPE_RADIUS <= INITIAL_RADIUS:
        raise ValueError("ESCAPE_RADIUS must exceed INITIAL_RADIUS.")
    if OUTPUT_POINTS < 2 or ANALYTICAL_CURVE_POINTS < 2:
        raise ValueError("Plotting point counts must be at least two.")
    if NUMBER_OF_PERIODS <= 0.0 or UNBOUND_TIME_LIMIT_IN_LOCAL_PERIODS <= 0.0:
        raise ValueError("Integration durations must be positive.")
    if ANIMATION_SECONDS_PER_PERIOD <= 0.0 or UNBOUND_ANIMATION_SECONDS <= 0.0:
        raise ValueError("Animation durations must be positive.")
    if ANIMATION_FPS <= 0:
        raise ValueError("ANIMATION_FPS must be positive.")
    if RELATIVE_TOLERANCE <= 0.0 or ABSOLUTE_TOLERANCE <= 0.0:
        raise ValueError("Integration tolerances must be positive.")


def main():
    """Run the configured general two-body integration experiment."""
    validate_configuration()
    state = initial_state()
    elements = analytical.classify_orbit(
        state[:2],
        state[2:],
        GRAVITATIONAL_PARAMETER,
        eccentricity_tolerance=ECCENTRICITY_TOLERANCE,
        energy_tolerance=ENERGY_TOLERANCE,
    )
    if abs(elements.specific_angular_momentum) < 1e-14:
        raise ValueError("A radial orbit has no regular polar conic representation.")

    solution = integrate_orbit(state, elements)
    analytical_conic = sample_analytical_conic(elements)
    errors = calculate_percentage_errors(solution, elements)
    print_report(elements, solution, errors)

    should_animate = SHOW_FIGURE or ANIMATION_PATH is not None
    figure, orbit_animation = create_visualization(
        solution,
        elements,
        analytical_conic,
        errors,
        should_animate,
    )
    if STATIC_FIGURE_PATH is not None:
        figure_path = Path(STATIC_FIGURE_PATH)
        figure_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(figure_path, dpi=200, bbox_inches="tight")
        print(f"Saved static figure to {figure_path}")
    if ANIMATION_PATH is not None:
        animation_path = Path(ANIMATION_PATH)
        if animation_path.suffix.lower() != ".gif":
            raise ValueError("ANIMATION_PATH must point to a .gif file.")
        animation_path.parent.mkdir(parents=True, exist_ok=True)
        assert orbit_animation is not None
        orbit_animation.save(
            animation_path,
            writer=PillowWriter(fps=ANIMATION_FPS),
            dpi=120,
        )
        print(f"Saved animation to {animation_path}")
    if SHOW_FIGURE:
        plt.show()


if __name__ == "__main__":
    main()
