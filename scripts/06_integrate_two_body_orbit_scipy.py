"""Integrate and animate Earth's orbit with SciPy's adaptive ODE solver.

The Cartesian two-body equations are integrated with ``scipy.integrate.solve_ivp``.
Unlike the velocity-Verlet example, this solver selects its internal time steps
adaptively to satisfy configured error tolerances. The numerical path is
compared with the analytical conic shape, and conservation errors quantify
the quality of the solution.
"""

from math import pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

from orbitworks.constants import AU, DAY, MU_EARTH, MU_SUN, YEAR
from orbitworks.graphics_mpl import set_plot_options

# Approximate J2000 Earth--Moon-barycenter elements from JPL.
EARTH_SEMI_MAJOR_AXIS = 1.00000261 * AU
EARTH_ECCENTRICITY = 0.01671123
# EARTH_ECCENTRICITY = 1.00


# User configuration.
NUMBER_OF_PERIODS = 5.0
OUTPUT_POINTS_PER_PERIOD = 4_000
INTEGRATION_METHOD = "DOP853"
RELATIVE_TOLERANCE = 1e-10
ABSOLUTE_TOLERANCE = 1e-9
ANALYTICAL_CURVE_POINTS = 2_000
ANIMATION_SECONDS_PER_PERIOD = 3.5
ANIMATION_FPS = 60
SHOW_FIGURE = True
STATIC_FIGURE_PATH = None  # For example: "earth_orbit_scipy.png"
ANIMATION_PATH = None  # For example: "earth_orbit_scipy.gif"


class OrbitSolution:
    """Store sampled Cartesian states and SciPy solver statistics."""

    def __init__(
        self,
        time,
        position,
        velocity,
        function_evaluations,
    ):
        self.time = time
        self.position = position
        self.velocity = velocity
        self.function_evaluations = function_evaluations


class ConservationDiagnostics:
    """Store the Kepler invariants evaluated at every output time."""

    def __init__(self, energy, angular_momentum, eccentricity_vector):
        self.energy = energy
        self.angular_momentum = angular_momentum
        self.eccentricity_vector = eccentricity_vector


def earth_initial_state(gravitational_parameter):
    """Construct Earth's Cartesian position and velocity at perihelion.

    For semi-major axis ``a`` and eccentricity ``e``,

        r_p = a(1 - e),
        v_p = sqrt(GM(1 + e)/(a(1 - e))).

    At perihelion, the velocity is perpendicular to the radius. The state
    vector is therefore ``[r_p, 0, 0, v_p]``.
    """
    semi_major_axis = EARTH_SEMI_MAJOR_AXIS
    eccentricity = EARTH_ECCENTRICITY
    perihelion_radius = semi_major_axis * (1.0 - eccentricity)
    perihelion_speed = sqrt(
        gravitational_parameter
        * (1.0 + eccentricity)
        / (semi_major_axis * (1.0 - eccentricity))
    )
    period = 2.0 * pi * sqrt(semi_major_axis**3 / gravitational_parameter)
    state = np.array([perihelion_radius, 0.0, 0.0, perihelion_speed])
    return state, period


def two_body_equations(time, state, gravitational_parameter):
    """Return the first-order Cartesian form of Newton's orbital equation.

    The state is ``[x, y, vx, vy]``. Newtonian gravity gives

        dx/dt = vx,
        dy/dt = vy,
        dvx/dt = -GM*x/r**3,
        dvy/dt = -GM*y/r**3,

    where ``r = sqrt(x**2 + y**2)``. The unused ``time`` argument is required
    by SciPy's generic ``solve_ivp`` interface.
    """
    del time
    x, y, velocity_x, velocity_y = state
    radius = sqrt(x**2 + y**2)
    if radius == 0.0:
        raise ValueError("Gravitational acceleration is singular at r = 0.")
    acceleration_factor = -gravitational_parameter / radius**3
    return np.array(
        [
            velocity_x,
            velocity_y,
            acceleration_factor * x,
            acceleration_factor * y,
        ]
    )


def integrate_with_scipy(
    initial_state,
    gravitational_parameter,
    duration,
    number_of_output_points,
):
    """Integrate the two-body ODE with adaptive error-controlled steps.

    ``solve_ivp`` varies its internal step size until local errors satisfy
    ``atol + rtol*abs(state)``. The uniformly spaced ``output_time`` values
    only request interpolated results for plotting and diagnostics; they do
    not impose a fixed integration step.
    """
    output_time = np.linspace(0.0, duration, number_of_output_points)
    result = solve_ivp(
        two_body_equations,
        (0.0, duration),
        initial_state,
        method=INTEGRATION_METHOD,
        t_eval=output_time,
        args=(gravitational_parameter,),
        rtol=RELATIVE_TOLERANCE,
        atol=np.asarray(ABSOLUTE_TOLERANCE),
    )
    if not result.success:
        raise RuntimeError(f"SciPy integration failed: {result.message}")

    position = result.y[:2].T
    velocity = result.y[2:].T
    return OrbitSolution(
        result.t,
        position,
        velocity,
        result.nfev,
    )


def analytical_orbit_shape(number_of_points):
    """Sample the conic path without assigning a time to its points.

    Binet's equation gives

        r(theta) = p/(1 + e*cos(theta)),
        p = a(1 - e**2).

    This curve is an analytical geometrical reference, not an analytical
    time-dependent solution.
    """
    eccentricity = EARTH_ECCENTRICITY
    semi_latus_rectum = EARTH_SEMI_MAJOR_AXIS * (1.0 - eccentricity**2)
    theta = np.linspace(0.0, 2.0 * pi, number_of_points)
    radius = semi_latus_rectum / (1.0 + eccentricity * np.cos(theta))
    return np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))


def relative_shape_error(solution):
    """Measure radial deviation from the analytical conic at the same angle."""
    eccentricity = EARTH_ECCENTRICITY
    semi_latus_rectum = EARTH_SEMI_MAJOR_AXIS * (1.0 - eccentricity**2)
    theta = np.arctan2(solution.position[:, 1], solution.position[:, 0])
    conic_radius = semi_latus_rectum / (1.0 + eccentricity * np.cos(theta))
    numerical_radius = np.linalg.norm(solution.position, axis=1)
    return (numerical_radius - conic_radius) / conic_radius


def calculate_diagnostics(solution, gravitational_parameter):
    """Evaluate quantities conserved by exact inverse-square dynamics.

    The diagnostics are specific energy, specific angular momentum, and the
    eccentricity vector:

        energy = |v|**2/2 - GM/|r|,
        ell = (r x v)_z,
        e = ((|v|**2 - GM/|r|)r - (r.v)v)/GM.
    """
    radius = np.linalg.norm(solution.position, axis=1)
    speed_squared = np.sum(solution.velocity**2, axis=1)
    radial_velocity_product = np.sum(solution.position * solution.velocity, axis=1)
    energy = 0.5 * speed_squared - gravitational_parameter / radius
    angular_momentum = (
        solution.position[:, 0] * solution.velocity[:, 1]
        - solution.position[:, 1] * solution.velocity[:, 0]
    )
    eccentricity_vector = (
        (speed_squared - gravitational_parameter / radius)[:, np.newaxis]
        * solution.position
        - radial_velocity_product[:, np.newaxis] * solution.velocity
    ) / gravitational_parameter
    return ConservationDiagnostics(
        energy,
        angular_momentum,
        eccentricity_vector,
    )


def relative_change(values):
    """Calculate ``(q(t)-q(0))/|q(0)|`` for a conserved scalar ``q``."""
    return (values - values[0]) / abs(values[0])


def calculate_percentage_errors(solution, diagnostics):
    """Return absolute relative invariant and conic errors in percent."""
    eccentricity_magnitude = np.linalg.norm(diagnostics.eccentricity_vector, axis=1)
    return {
        "energy": 100.0 * np.abs(relative_change(diagnostics.energy)),
        "angular momentum": 100.0
        * np.abs(relative_change(diagnostics.angular_momentum)),
        "eccentricity magnitude": 100.0
        * np.abs(relative_change(eccentricity_magnitude)),
        "conic shape": 100.0 * np.abs(relative_shape_error(solution)),
    }


def print_quality_report(solution, errors, orbital_period):
    """Print solver effort and maximum percentage errors."""
    print(
        f"Integrated duration: {solution.time[-1] / orbital_period:.3f} "
        "orbital periods"
    )
    print(f"Requested output intervals: {len(solution.time) - 1}")
    print(f"ODE right-hand-side evaluations: {solution.function_evaluations}")
    print(f"SciPy method: {INTEGRATION_METHOD}")
    print(f"Relative tolerance: {RELATIVE_TOLERANCE:.1e}")
    for name, values in errors.items():
        print(f"Maximum relative {name} deviation: {np.max(values):.3e} %")


def create_visualization(
    solution,
    analytical_shape,
    errors,
    animate,
):
    """Overlay orbit shapes and display percentage errors on log axes."""
    set_plot_options(fontsize=11, color_order="matlab", linewidth=1.5)
    figure = plt.figure(figsize=(13, 6.5), constrained_layout=True)
    grid = figure.add_gridspec(2, 2, width_ratios=(1.25, 1.0))
    orbit_axes = figure.add_subplot(grid[:, 0])
    upper_error_axes = figure.add_subplot(grid[0, 1])
    lower_error_axes = figure.add_subplot(grid[1, 1])

    numerical_au = solution.position / AU
    analytical_au = analytical_shape / AU
    time_years = solution.time / YEAR
    orbit_axes.plot(
        analytical_au[:, 0],
        analytical_au[:, 1],
        "--",
        color="#555555",
        linewidth=2.0,
        label="analytical conic shape",
    )
    orbit_axes.plot(
        numerical_au[:, 0],
        numerical_au[:, 1],
        color="#0072BD",
        alpha=0.25,
        label="SciPy numerical orbit",
    )
    (trail,) = orbit_axes.plot([], [], color="#0072BD", linewidth=2.2)
    (earth,) = orbit_axes.plot(
        [], [], "o", color="#2E86DE", markersize=8, label="Earth"
    )
    orbit_axes.plot(
        0.0,
        0.0,
        "o",
        color="#FDB813",
        markeredgecolor="#9C6B00",
        markersize=12,
        label="Sun",
    )
    orbit_axes.set_aspect("equal", adjustable="box")
    orbit_axes.set_xlabel("x [AU]")
    orbit_axes.set_ylabel("y [AU]")
    orbit_axes.legend(loc="upper right")

    floor = 100.0 * np.finfo(float).eps
    upper_error_axes.semilogy(
        time_years,
        np.maximum(errors["energy"], floor),
        label="energy",
    )
    upper_error_axes.semilogy(
        time_years,
        np.maximum(errors["conic shape"], floor),
        label="conic shape",
    )
    upper_error_axes.set_ylabel("absolute relative deviation [%]")
    upper_error_axes.set_title("SciPy numerical error diagnostics")
    upper_error_axes.legend(loc="best")
    lower_error_axes.semilogy(
        time_years,
        np.maximum(errors["angular momentum"], floor),
        label="angular momentum",
    )
    lower_error_axes.semilogy(
        time_years,
        np.maximum(errors["eccentricity magnitude"], floor),
        label="eccentricity magnitude",
    )
    lower_error_axes.set_xlabel("time [Julian years]")
    lower_error_axes.set_ylabel("absolute relative deviation [%]")
    lower_error_axes.legend(loc="best")

    if not animate:
        trail.set_data(numerical_au[:, 0], numerical_au[:, 1])
        earth.set_data([numerical_au[-1, 0]], [numerical_au[-1, 1]])
        orbit_axes.set_title("Adaptive numerical and analytical orbit shapes")
        return figure, None

    animation_frames = max(
        2,
        round(NUMBER_OF_PERIODS * ANIMATION_SECONDS_PER_PERIOD * ANIMATION_FPS),
    )
    animation_interval_ms = 1_000.0 / ANIMATION_FPS
    frame_indices = np.linspace(
        0,
        len(solution.time) - 1,
        animation_frames,
        dtype=int,
    )
    orbit_title = orbit_axes.set_title("")

    def initialize_animation():
        trail.set_data([], [])
        earth.set_data([], [])
        orbit_title.set_text("")
        return trail, earth, orbit_title

    def update_animation(frame_index):
        index = frame_indices[frame_index]
        trail.set_data(numerical_au[: index + 1, 0], numerical_au[: index + 1, 1])
        earth.set_data([numerical_au[index, 0]], [numerical_au[index, 1]])
        orbit_title.set_text(
            f"SciPy Earth orbit: t = {solution.time[index] / DAY:.1f} days"
        )
        return trail, earth, orbit_title

    orbit_animation = FuncAnimation(
        figure,
        update_animation,
        init_func=initialize_animation,
        frames=len(frame_indices),
        interval=animation_interval_ms,
        blit=True,
        repeat=True,
    )
    return figure, orbit_animation


def main():
    """Run the configured adaptive SciPy integration experiment."""
    if NUMBER_OF_PERIODS <= 0.0:
        raise ValueError("NUMBER_OF_PERIODS must be positive.")
    if OUTPUT_POINTS_PER_PERIOD < 2:
        raise ValueError("OUTPUT_POINTS_PER_PERIOD must be at least two.")
    if ANIMATION_SECONDS_PER_PERIOD <= 0.0:
        raise ValueError("ANIMATION_SECONDS_PER_PERIOD must be positive.")
    if ANIMATION_FPS <= 0:
        raise ValueError("ANIMATION_FPS must be positive.")
    if ANALYTICAL_CURVE_POINTS < 2:
        raise ValueError("ANALYTICAL_CURVE_POINTS must be at least two.")
    if RELATIVE_TOLERANCE <= 0.0 or np.any(np.asarray(ABSOLUTE_TOLERANCE) <= 0.0):
        raise ValueError("SciPy integration tolerances must be positive.")

    gravitational_parameter = MU_SUN + MU_EARTH
    initial_state, period = earth_initial_state(gravitational_parameter)
    duration = NUMBER_OF_PERIODS * period
    number_of_output_points = max(
        2,
        round(NUMBER_OF_PERIODS * OUTPUT_POINTS_PER_PERIOD) + 1,
    )
    solution = integrate_with_scipy(
        initial_state,
        gravitational_parameter,
        duration,
        number_of_output_points,
    )
    analytical_shape = analytical_orbit_shape(ANALYTICAL_CURVE_POINTS)
    diagnostics = calculate_diagnostics(solution, gravitational_parameter)
    errors = calculate_percentage_errors(solution, diagnostics)
    print_quality_report(solution, errors, period)

    should_animate = SHOW_FIGURE or ANIMATION_PATH is not None
    figure, orbit_animation = create_visualization(
        solution,
        analytical_shape,
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
