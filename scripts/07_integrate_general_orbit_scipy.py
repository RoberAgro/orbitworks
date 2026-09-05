"""Integrate circular, elliptical, parabolic, or hyperbolic Kepler orbits.

The initial Cartesian state determines the conic; the integrator does not need
to be told which orbit type to expect. Specific orbital energy classifies the
result as bound, parabolic, or unbound, while the angular momentum and
eccentricity vector determine the corresponding analytical conic.

Bound integrations have a known period and therefore use a final time equal to
``NUMBER_OF_PERIODS`` periods. Open trajectories have no period. For them, a
terminal SciPy event stops integration when the body crosses ``ESCAPE_RADIUS``.
A second terminal event stops any trajectory that hits the central body.
"""

from math import acos, atan2, pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle
from scipy.integrate import solve_ivp

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

ANALYTICAL_CURVE_POINTS = 2_000
ANIMATION_SECONDS_PER_PERIOD = 2.5
UNBOUND_ANIMATION_SECONDS = 5.0
ANIMATION_FPS = 40
SHOW_FIGURE = True
STATIC_FIGURE_PATH = None  # For example: "general_orbit.png"
ANIMATION_PATH = None  # For example: "general_orbit.gif"


class OrbitProperties:
    """Store conic properties inferred from a Cartesian initial state."""

    def __init__(
        self,
        orbit_type,
        specific_energy,
        specific_angular_momentum,
        eccentricity_vector,
        eccentricity,
        semi_latus_rectum,
        semi_major_axis,
        period,
    ):
        self.orbit_type = orbit_type
        self.specific_energy = specific_energy
        self.specific_angular_momentum = specific_angular_momentum
        self.eccentricity_vector = eccentricity_vector
        self.eccentricity = eccentricity
        self.semi_latus_rectum = semi_latus_rectum
        self.semi_major_axis = semi_major_axis
        self.period = period

    @property
    def is_bound(self):
        """Return whether the conic has negative energy and a finite period."""
        return self.orbit_type in ("circle", "ellipse")


class OrbitSolution:
    """Store sampled states, event information, and solver effort."""

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


def calculate_orbit_properties(state):
    """Infer the energy, angular momentum, eccentricity, and conic type.

    For position ``r`` and velocity ``v``, the invariants are

        energy = |v|^2/2 - GM/|r|,
        ell = (r x v)_z,
        e_vector = ((|v|^2 - GM/|r|)r - (r.v)v)/GM.

    Negative, zero, and positive energy correspond to an ellipse, parabola,
    and hyperbola. A zero-eccentricity ellipse is reported as a circle.
    """
    position = state[:2]
    velocity = state[2:]
    radius = np.linalg.norm(position)
    speed_squared = np.dot(velocity, velocity)
    radial_velocity_product = np.dot(position, velocity)
    specific_energy = 0.5 * speed_squared - GRAVITATIONAL_PARAMETER / radius
    specific_angular_momentum = position[0] * velocity[1] - position[1] * velocity[0]
    eccentricity_vector = (
        (speed_squared - GRAVITATIONAL_PARAMETER / radius) * position
        - radial_velocity_product * velocity
    ) / GRAVITATIONAL_PARAMETER
    eccentricity = np.linalg.norm(eccentricity_vector)
    semi_latus_rectum = specific_angular_momentum**2 / GRAVITATIONAL_PARAMETER

    energy_scale = GRAVITATIONAL_PARAMETER / radius
    classification_tolerance = 1e-10 * energy_scale
    if abs(specific_energy) <= classification_tolerance:
        orbit_type = "parabola"
        semi_major_axis = None
        period = None
    elif specific_energy < 0.0:
        semi_major_axis = -GRAVITATIONAL_PARAMETER / (2.0 * specific_energy)
        period = 2.0 * pi * sqrt(semi_major_axis**3 / GRAVITATIONAL_PARAMETER)
        orbit_type = "circle" if eccentricity < 1e-8 else "ellipse"
    else:
        orbit_type = "hyperbola"
        semi_major_axis = -GRAVITATIONAL_PARAMETER / (2.0 * specific_energy)
        period = None

    return OrbitProperties(
        orbit_type,
        specific_energy,
        specific_angular_momentum,
        eccentricity_vector,
        eccentricity,
        semi_latus_rectum,
        semi_major_axis,
        period,
    )


def two_body_equations(time, state):
    """Return the Cartesian first-order form of Newton's orbital equation.

    For state ``[x, y, vx, vy]``, the acceleration is

        d^2 r/dt^2 = -GM r/|r|^3.
    """
    del time
    position = state[:2]
    radius = np.linalg.norm(position)
    if radius == 0.0:
        raise ValueError("Gravitational acceleration is singular at r = 0.")
    acceleration = -GRAVITATIONAL_PARAMETER * position / radius**3
    return np.concatenate((state[2:], acceleration))


def escape_radius_event(time, state):
    """Become zero on an outward crossing of the configured escape radius."""
    del time
    return np.linalg.norm(state[:2]) - ESCAPE_RADIUS


escape_radius_event.terminal = True
escape_radius_event.direction = 1.0


def collision_event(time, state):
    """Become zero on an inward crossing of the central body's surface."""
    del time
    return np.linalg.norm(state[:2]) - CENTRAL_BODY_RADIUS


collision_event.terminal = True
collision_event.direction = -1.0


def integration_duration(properties):
    """Choose a known bound duration or a safety limit for an open orbit.

    Elliptical motion has a calculable period, so no period-counting event is
    required. Open motion has no period; its time span is merely a safety cap,
    and the escape-radius event normally terminates it first.
    """
    if properties.is_bound:
        return NUMBER_OF_PERIODS * properties.period

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


def integrate_orbit(state, properties):
    """Integrate adaptively until the time limit, escape, or collision.

    Bound trajectories use only the collision event because their specified
    final time already represents the requested number of periods. Parabolic
    and hyperbolic trajectories additionally use the terminal escape event.
    """
    duration = integration_duration(properties)
    output_time = np.linspace(0.0, duration, OUTPUT_POINTS)
    events = [collision_event]
    if not properties.is_bound:
        events.append(escape_radius_event)

    result = solve_ivp(
        two_body_equations,
        (0.0, duration),
        state,
        method=INTEGRATION_METHOD,
        t_eval=output_time,
        events=events,
        rtol=RELATIVE_TOLERANCE,
        atol=ABSOLUTE_TOLERANCE,
    )
    if not result.success:
        raise RuntimeError(f"SciPy integration failed: {result.message}")

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


def sample_analytical_conic(properties):
    """Sample the invariant conic, oriented by its eccentricity vector.

    The polar equation measured from periapsis is

        r = p/(1 + e cos(theta)).

    Closed conics are sampled for a full revolution. Open branches are sampled
    only as far as ``ESCAPE_RADIUS`` so the analytical and numerical paths have
    the same visible scale.
    """
    if properties.eccentricity < 1e-12:
        periapsis_angle = 0.0
    else:
        periapsis_angle = atan2(
            properties.eccentricity_vector[1],
            properties.eccentricity_vector[0],
        )

    if properties.is_bound:
        relative_angle = np.linspace(
            -pi,
            pi,
            ANALYTICAL_CURVE_POINTS,
        )
    else:
        cosine_limit = (
            properties.semi_latus_rectum / ESCAPE_RADIUS - 1.0
        ) / properties.eccentricity
        angle_limit = acos(float(np.clip(cosine_limit, -1.0, 1.0)))
        relative_angle = np.linspace(
            -angle_limit,
            angle_limit,
            ANALYTICAL_CURVE_POINTS,
        )

    radius = properties.semi_latus_rectum / (
        1.0 + properties.eccentricity * np.cos(relative_angle)
    )
    angle = relative_angle + periapsis_angle
    return np.column_stack((radius * np.cos(angle), radius * np.sin(angle)))


def calculate_percentage_errors(solution, properties):
    """Calculate conservation and analytical conic errors in percent."""
    radius = np.linalg.norm(solution.position, axis=1)
    speed_squared = np.sum(solution.velocity**2, axis=1)
    radial_velocity_product = np.sum(
        solution.position * solution.velocity,
        axis=1,
    )
    energy = 0.5 * speed_squared - GRAVITATIONAL_PARAMETER / radius
    angular_momentum = (
        solution.position[:, 0] * solution.velocity[:, 1]
        - solution.position[:, 1] * solution.velocity[:, 0]
    )
    eccentricity_vector = (
        (speed_squared - GRAVITATIONAL_PARAMETER / radius)[:, np.newaxis]
        * solution.position
        - radial_velocity_product[:, np.newaxis] * solution.velocity
    ) / GRAVITATIONAL_PARAMETER

    if properties.orbit_type != "parabola":
        energy_error = (
            100.0
            * np.abs(energy - properties.specific_energy)
            / abs(properties.specific_energy)
        )
    else:
        # A parabolic orbit has zero energy, so division by its reference value
        # is undefined. Normalize by the local gravitational-energy scale.
        energy_scale = GRAVITATIONAL_PARAMETER / INITIAL_RADIUS
        energy_error = 100.0 * np.abs(energy) / energy_scale

    angular_momentum_error = (
        100.0
        * np.abs(angular_momentum - properties.specific_angular_momentum)
        / abs(properties.specific_angular_momentum)
    )
    eccentricity_vector_error = (
        100.0
        * np.linalg.norm(
            eccentricity_vector - properties.eccentricity_vector,
            axis=1,
        )
        / max(properties.eccentricity, 1.0)
    )

    if properties.eccentricity < 1e-12:
        analytical_radius = np.full_like(radius, properties.semi_latus_rectum)
    else:
        eccentricity_direction = (
            properties.eccentricity_vector / properties.eccentricity
        )
        cosine_from_periapsis = solution.position @ eccentricity_direction / radius
        analytical_radius = properties.semi_latus_rectum / (
            1.0 + properties.eccentricity * cosine_from_periapsis
        )
    shape_error = 100.0 * np.abs(radius - analytical_radius) / analytical_radius

    return {
        "energy": energy_error,
        "angular momentum": angular_momentum_error,
        "eccentricity vector": eccentricity_vector_error,
        "conic shape": shape_error,
    }


def print_report(properties, solution, errors):
    """Print the inferred orbit and numerical-quality diagnostics."""
    print(f"Orbit type: {properties.orbit_type}")
    print(f"Eccentricity: {properties.eccentricity:.8f}")
    print(f"Specific energy: {properties.specific_energy:.6e} J/kg")
    print(
        "Specific angular momentum: "
        f"{properties.specific_angular_momentum:.6e} m^2/s"
    )
    if properties.period is not None:
        print(f"Orbital period: {properties.period / 3600.0:.6f} h")
        print(f"Integrated periods: {solution.time[-1] / properties.period:.6f}")
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


def create_visualization(solution, properties, analytical_conic, errors, animate):
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
        properties.period if properties.period is not None else solution.time[-1]
    )
    scaled_time = solution.time / time_scale
    time_label = "time / orbital period" if properties.is_bound else "time / final time"
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
        orbit_title.set_text(f"{orbit_adjective(properties.orbit_type)} orbit")
        return figure, None

    if properties.is_bound:
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
            f"{orbit_adjective(properties.orbit_type)} orbit: "
            f"t = {scaled_time[index]:.2f} "
            f"{'periods' if properties.is_bound else 'of final time'}"
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
    properties = calculate_orbit_properties(state)
    if abs(properties.specific_angular_momentum) < 1e-14:
        raise ValueError("A radial orbit has no regular polar conic representation.")

    solution = integrate_orbit(state, properties)
    analytical_conic = sample_analytical_conic(properties)
    errors = calculate_percentage_errors(solution, properties)
    print_report(properties, solution, errors)

    should_animate = SHOW_FIGURE or ANIMATION_PATH is not None
    figure, orbit_animation = create_visualization(
        solution,
        properties,
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
