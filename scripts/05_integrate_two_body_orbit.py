"""Numerically integrate and animate Earth's orbit around the Sun.

The Earth--Sun relative position is integrated in Cartesian coordinates with
the velocity-Verlet method. The numerical path is compared with the analytical
conic shape ``r(theta)``, without using an analytical time evolution. Energy,
angular momentum, and the eccentricity vector measure numerical quality.
"""

from math import pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from orbitworks.constants import AU, DAY, MU_EARTH, MU_SUN, YEAR
from orbitworks.graphics_mpl import set_plot_options

# Approximate J2000 Earth--Moon-barycenter elements from JPL. The initial
# Cartesian state is placed at perihelion.
EARTH_SEMI_MAJOR_AXIS = 1.00000261 * AU
EARTH_ECCENTRICITY = 0.01671123

# User configuration.
NUMBER_OF_PERIODS = 2.0
STEPS_PER_PERIOD = 4_000
ANALYTICAL_CURVE_POINTS = 2_000
ANIMATION_FRAMES = 600
ANIMATION_INTERVAL_MS = 1.0
SHOW_FIGURE = True
STATIC_FIGURE_PATH = None  # For example: "earth_orbit.png"
ANIMATION_PATH = None  # For example: "earth_orbit.gif"


class OrbitSolution:
    """Store the discrete numerical approximation to ``r(t)`` and ``v(t)``."""

    def __init__(self, time, position, velocity):
        self.time = time
        self.position = position
        self.velocity = velocity


class ConservationDiagnostics:
    """Store invariants evaluated at every numerical time step."""

    def __init__(self, energy, angular_momentum, eccentricity_vector):
        self.energy = energy
        self.angular_momentum = angular_momentum
        self.eccentricity_vector = eccentricity_vector


def gravitational_acceleration(
    position,
    gravitational_parameter,
):
    """Evaluate Newtonian gravitational acceleration in Cartesian form.

    For the relative position vector ``r`` between Earth and the Sun, the
    two-body equation is

        d2r/dt2 = -G(M_sun + M_earth) r / |r|**3.

    Multiplication by ``r / |r|`` supplies the inward radial direction while
    the remaining factor gives the inverse-square magnitude.
    """
    radius = np.linalg.norm(position)
    if radius == 0.0:
        raise ValueError("Gravitational acceleration is singular at r = 0.")
    return -gravitational_parameter * position / radius**3


def earth_initial_state(
    gravitational_parameter,
):
    """Construct Earth's Cartesian state at perihelion.

    For semi-major axis ``a`` and eccentricity ``e``, the perihelion radius
    and speed are

        r_p = a(1 - e),
        v_p = sqrt(GM(1 + e) / (a(1 - e))).

    At perihelion the velocity is perpendicular to the radius. The orbital
    period ``T = 2*pi*sqrt(a**3/GM)`` determines the integration duration.
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
    position = np.array([perihelion_radius, 0.0])
    velocity = np.array([0.0, perihelion_speed])
    return position, velocity, period


def integrate_velocity_verlet(
    initial_position,
    initial_velocity,
    gravitational_parameter,
    duration,
    number_of_steps,
):
    """Integrate the Cartesian two-body equation with velocity Verlet.

    With time step ``dt``, velocity Verlet advances the state according to

        r[n+1] = r[n] + v[n] dt + a[n] dt**2 / 2,
        v[n+1] = v[n] + (a[n] + a[n+1]) dt / 2.

    This second-order, time-reversible method is well suited to conservative
    mechanical systems because it avoids the secular energy drift typical of
    basic forward Euler integration.
    """
    if number_of_steps < 1:
        raise ValueError("number_of_steps must be at least one.")

    time = np.linspace(0.0, duration, number_of_steps + 1)
    time_step = time[1] - time[0]
    position = np.empty((number_of_steps + 1, 2))
    velocity = np.empty((number_of_steps + 1, 2))
    position[0] = initial_position
    velocity[0] = initial_velocity

    acceleration = gravitational_acceleration(initial_position, gravitational_parameter)
    for index in range(number_of_steps):
        position[index + 1] = (
            position[index]
            + velocity[index] * time_step
            + 0.5 * acceleration * time_step**2
        )
        next_acceleration = gravitational_acceleration(
            position[index + 1], gravitational_parameter
        )
        velocity[index + 1] = (
            velocity[index] + 0.5 * (acceleration + next_acceleration) * time_step
        )
        acceleration = next_acceleration

    return OrbitSolution(time, position, velocity)


def analytical_orbit_shape(number_of_points):
    """Sample the analytical conic without specifying motion along it.

    The orbit derived from Binet's equation is

        r(theta) = p / (1 + e*cos(theta)),
        p = a(1 - e**2).

    Sampling ``theta`` draws only the geometrical path. It does not determine
    the time at which Earth reaches any particular point on that path.
    """
    semi_major_axis = EARTH_SEMI_MAJOR_AXIS
    eccentricity = EARTH_ECCENTRICITY
    semi_latus_rectum = semi_major_axis * (1.0 - eccentricity**2)
    theta = np.linspace(0.0, 2.0 * pi, number_of_points)
    radius = semi_latus_rectum / (1.0 + eccentricity * np.cos(theta))
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.column_stack((x, y))


def relative_shape_error(solution):
    """Measure how far each numerical point lies from the analytical conic.

    Each numerical Cartesian position determines an angle ``theta`` and a
    radius ``r_num``. The analytical radius at that same angle is
    ``p/(1 + e*cos(theta))``. Their normalized difference tests the orbit's
    shape without comparing the timing of the two solutions.
    """
    eccentricity = EARTH_ECCENTRICITY
    semi_latus_rectum = EARTH_SEMI_MAJOR_AXIS * (1.0 - eccentricity**2)
    theta = np.arctan2(solution.position[:, 1], solution.position[:, 0])
    analytical_radius = semi_latus_rectum / (1.0 + eccentricity * np.cos(theta))
    numerical_radius = np.linalg.norm(solution.position, axis=1)
    return (numerical_radius - analytical_radius) / analytical_radius


def calculate_diagnostics(
    solution,
    gravitational_parameter,
):
    """Evaluate the conserved quantities of the Kepler problem.

    Per unit orbiting mass, the invariants are

        energy = |v|**2 / 2 - GM / |r|,
        angular momentum = (r x v)_z,
        eccentricity vector = ((|v|**2 - GM/|r|)r - (r.v)v) / GM.

    Exact dynamics keeps all three constant. Their numerical variation is
    therefore a direct diagnostic of integration error.
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
    return ConservationDiagnostics(energy, angular_momentum, eccentricity_vector)


def relative_change(values):
    """Calculate ``(q(t) - q(0)) / |q(0)|`` for a conserved scalar ``q``."""
    return (values - values[0]) / abs(values[0])


def print_quality_report(
    solution,
    diagnostics,
    orbital_period,
):
    """Report maximum invariant drift and conic-shape error in percent."""
    energy_error = 100.0 * np.abs(relative_change(diagnostics.energy))
    momentum_error = 100.0 * np.abs(relative_change(diagnostics.angular_momentum))
    eccentricity_magnitude = np.linalg.norm(diagnostics.eccentricity_vector, axis=1)
    eccentricity_error = 100.0 * np.abs(relative_change(eccentricity_magnitude))
    shape_error = 100.0 * np.abs(relative_shape_error(solution))
    integrated_periods = solution.time[-1] / orbital_period

    print(f"Integrated duration: {integrated_periods:.3f} orbital periods")
    print(f"Integration steps: {len(solution.time) - 1}")
    print(f"Time step: {(solution.time[1] - solution.time[0]) / 3600:.3f} h")
    print(f"Maximum relative energy deviation: {np.max(energy_error):.3e} %")
    print(
        "Maximum relative angular-momentum deviation: "
        f"{np.max(momentum_error):.3e} %"
    )
    print(
        "Maximum relative eccentricity-magnitude deviation: "
        f"{np.max(eccentricity_error):.3e} %"
    )
    print(f"Maximum relative conic-shape deviation: {np.max(shape_error):.3e} %")


def create_visualization(
    solution,
    analytical_shape,
    diagnostics,
    number_of_frames,
    animation_interval_ms,
    animate,
):
    """Compare orbit shapes and display numerical conservation errors.

    The left panel overlays the time-integrated Cartesian path on the conic
    derived from Binet's equation. The right panels show absolute relative
    deviations in percent on logarithmic axes. When enabled, the marker and
    trail reveal the nonuniform motion along the ellipse.
    """
    set_plot_options(fontsize=11, color_order="matlab", linewidth=1.5)
    figure = plt.figure(figsize=(13, 6.5), constrained_layout=True)
    grid = figure.add_gridspec(2, 2, width_ratios=(1.25, 1.0))
    orbit_axes = figure.add_subplot(grid[:, 0])
    energy_axes = figure.add_subplot(grid[0, 1])
    momentum_axes = figure.add_subplot(grid[1, 1])

    numerical_au = solution.position / AU
    analytical_au = analytical_shape / AU
    time_years = solution.time / YEAR
    orbit_axes.plot(
        analytical_au[:, 0],
        analytical_au[:, 1],
        "--",
        color="#555555",
        linewidth=2.0,
        label="analytical Kepler orbit",
    )
    orbit_axes.plot(
        numerical_au[:, 0],
        numerical_au[:, 1],
        color="#0072BD",
        alpha=0.25,
        label="complete numerical orbit",
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

    energy_error = 100.0 * np.abs(relative_change(diagnostics.energy))
    momentum_error = 100.0 * np.abs(relative_change(diagnostics.angular_momentum))
    eccentricity_magnitude = np.linalg.norm(diagnostics.eccentricity_vector, axis=1)
    eccentricity_error = 100.0 * np.abs(relative_change(eccentricity_magnitude))
    shape_error = 100.0 * np.abs(relative_shape_error(solution))
    logarithmic_floor = 100.0 * np.finfo(float).eps

    energy_axes.semilogy(
        time_years,
        np.maximum(energy_error, logarithmic_floor),
        color="#D95319",
        label="energy",
    )
    energy_axes.semilogy(
        time_years,
        np.maximum(shape_error, logarithmic_floor),
        label="conic shape",
    )
    energy_axes.set_ylabel("absolute relative deviation [%]")
    energy_axes.set_title("Numerical error diagnostics")
    energy_axes.legend(loc="best")
    momentum_axes.semilogy(
        time_years,
        np.maximum(momentum_error, logarithmic_floor),
        label="angular momentum",
    )
    momentum_axes.semilogy(
        time_years,
        np.maximum(eccentricity_error, logarithmic_floor),
        label="eccentricity magnitude",
    )
    momentum_axes.set_xlabel("time [Julian years]")
    momentum_axes.set_ylabel("absolute relative deviation [%]")
    momentum_axes.legend(loc="best")

    if not animate:
        trail.set_data(numerical_au[:, 0], numerical_au[:, 1])
        earth.set_data([numerical_au[-1, 0]], [numerical_au[-1, 1]])
        orbit_axes.set_title("Numerical and analytical Earth orbit")
        return figure, None

    frame_indices = np.linspace(0, len(solution.time) - 1, number_of_frames, dtype=int)

    def initialize_animation():
        trail.set_data([], [])
        earth.set_data([], [])
        return trail, earth

    def update_animation(frame_index):
        index = frame_indices[frame_index]
        trail.set_data(numerical_au[: index + 1, 0], numerical_au[: index + 1, 1])
        earth.set_data([numerical_au[index, 0]], [numerical_au[index, 1]])
        orbit_axes.set_title(f"Earth orbit: t = {solution.time[index] / DAY:.1f} days")
        return trail, earth

    orbit_animation = FuncAnimation(
        figure,
        update_animation,
        init_func=initialize_animation,
        frames=len(frame_indices),
        interval=animation_interval_ms,
        blit=False,
        repeat=True,
    )
    return figure, orbit_animation


def main():
    """Run the configured numerical experiment and visualization."""
    if NUMBER_OF_PERIODS <= 0.0:
        raise ValueError("NUMBER_OF_PERIODS must be positive.")
    if STEPS_PER_PERIOD < 1:
        raise ValueError("STEPS_PER_PERIOD must be positive.")
    if ANIMATION_FRAMES < 2:
        raise ValueError("ANIMATION_FRAMES must be at least two.")
    if ANIMATION_INTERVAL_MS <= 0.0:
        raise ValueError("ANIMATION_INTERVAL_MS must be positive.")

    gravitational_parameter = MU_SUN + MU_EARTH
    initial_position, initial_velocity, period = earth_initial_state(
        gravitational_parameter
    )
    duration = NUMBER_OF_PERIODS * period
    number_of_steps = max(1, round(NUMBER_OF_PERIODS * STEPS_PER_PERIOD))
    solution = integrate_velocity_verlet(
        initial_position,
        initial_velocity,
        gravitational_parameter,
        duration,
        number_of_steps,
    )
    analytical_shape = analytical_orbit_shape(ANALYTICAL_CURVE_POINTS)
    diagnostics = calculate_diagnostics(solution, gravitational_parameter)
    print_quality_report(solution, diagnostics, period)

    should_animate = SHOW_FIGURE or ANIMATION_PATH is not None
    figure, orbit_animation = create_visualization(
        solution,
        analytical_shape,
        diagnostics,
        ANIMATION_FRAMES,
        ANIMATION_INTERVAL_MS,
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
            writer=PillowWriter(fps=round(1_000.0 / ANIMATION_INTERVAL_MS)),
            dpi=120,
        )
        print(f"Saved animation to {animation_path}")
    if SHOW_FIGURE:
        plt.show()


if __name__ == "__main__":
    main()
