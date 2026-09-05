"""Visualize how initial tangential velocity selects a Keplerian conic.

The body starts at radius ``r0`` with zero radial velocity. Its tangential
speed determines the integration constants in Binet's equation:

    specific angular momentum: ell = r0 * v0
    eccentricity:              e = r0 * v0**2 / (G * M) - 1
    semi-latus rectum:         p = ell**2 / (G * M)

The eccentricity expression assumes ``v0`` is at least the circular speed, so
the initial point is periapsis. The four selected speeds produce a circle,
ellipse, parabola, and hyperbola around Earth.
"""

from math import acos, pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from orbitworks.constants import G, M_EARTH, R_EARTH
from orbitworks.graphics_mpl import set_plot_options

# User configuration.
INITIAL_RADIUS = 4.0 * R_EARTH
MAXIMUM_PLOTTED_RADIUS = 6.0 * INITIAL_RADIUS
NUMBER_OF_POINTS = 2_000
SHOW_FIGURE = True
FIGURE_PATH = None  # For example: "conic_sections.png"
CONIC_CASES = (
    ("Circle", 1.0),
    ("Ellipse", sqrt(1.5)),
    ("Parabola", sqrt(2.0)),
    ("Hyperbola", sqrt(2.5)),
)


class ConicOrbit:
    """Store the constants obtained from one tangential initial state."""

    def __init__(
        self,
        name,
        speed_ratio,
        initial_speed,
        specific_energy,
        specific_angular_momentum,
        eccentricity,
        semi_latus_rectum,
        binet_amplitude,
    ):
        self.name = name
        self.speed_ratio = speed_ratio
        self.initial_speed = initial_speed
        self.specific_energy = specific_energy
        self.specific_angular_momentum = specific_angular_momentum
        self.eccentricity = eccentricity
        self.semi_latus_rectum = semi_latus_rectum
        self.binet_amplitude = binet_amplitude


def orbit_from_tangential_state(
    name,
    central_mass,
    initial_radius,
    speed_ratio,
):
    """Calculate the conic selected by an initial tangential velocity.

    At periapsis, ``ell = r0*v0``. Substitution into the energy and conic
    relations gives

        energy = v0**2/2 - GM/r0,
        e = r0*v0**2/GM - 1,
        p = ell**2/GM.

    Thus the initial speed fixes the integration constants in Binet's
    equation and selects the type of conic.
    """
    gravitational_parameter = G * central_mass
    circular_speed = sqrt(gravitational_parameter / initial_radius)
    initial_speed = speed_ratio * circular_speed

    if initial_speed < circular_speed:
        raise ValueError("The initial point is periapsis only when v0 >= vc.")

    specific_angular_momentum = initial_radius * initial_speed
    specific_energy = 0.5 * initial_speed**2 - gravitational_parameter / initial_radius
    eccentricity = initial_radius * initial_speed**2 / gravitational_parameter - 1.0
    semi_latus_rectum = specific_angular_momentum**2 / gravitational_parameter

    # In u(theta) = GM/ell^2 + C cos(theta), C = e/p.
    binet_amplitude = eccentricity / semi_latus_rectum

    return ConicOrbit(
        name=name,
        speed_ratio=speed_ratio,
        initial_speed=initial_speed,
        specific_energy=specific_energy,
        specific_angular_momentum=specific_angular_momentum,
        eccentricity=eccentricity,
        semi_latus_rectum=semi_latus_rectum,
        binet_amplitude=binet_amplitude,
    )


def sample_orbit(
    orbit,
    initial_radius,
    maximum_radius,
    number_of_points,
):
    """Sample the conic ``r(theta) = p/(1 + e*cos(theta))``.

    Closed conics are sampled through a complete revolution. Parabolic and
    hyperbolic radii diverge at their asymptotes, so their plotted branches
    are truncated at ``maximum_radius``.
    """
    eccentricity = orbit.eccentricity

    if eccentricity < 1.0 - 1e-12:
        theta = np.linspace(-pi, pi, number_of_points)
    else:
        # Open conics extend to infinity. Stop each plotted branch at the same
        # finite radius so its shape remains visible without approaching the
        # asymptote numerically.
        cosine_limit = (orbit.semi_latus_rectum / maximum_radius - 1.0) / eccentricity
        theta_limit = acos(float(np.clip(cosine_limit, -1.0, 1.0)))
        theta = np.linspace(-theta_limit, theta_limit, number_of_points)

    radius = orbit.semi_latus_rectum / (1.0 + eccentricity * np.cos(theta))
    x = radius * np.cos(theta) / initial_radius
    y = radius * np.sin(theta) / initial_radius
    return x, y


def print_orbit_table(orbits):
    """Display how each chosen velocity produces energy, eccentricity, and p."""
    print(
        f"{'orbit':<11} {'v0/vc':>8} {'v0 [km/s]':>12} "
        f"{'energy [MJ/kg]':>15} {'e':>8} {'p/r0':>9}"
    )
    for orbit in orbits:
        print(
            f"{orbit.name:<11} "
            f"{orbit.speed_ratio:8.4f} "
            f"{orbit.initial_speed / 1e3:12.4f} "
            f"{orbit.specific_energy / 1e6:15.4f} "
            f"{orbit.eccentricity:8.4f} "
            f"{1.0 + orbit.eccentricity:9.4f}"
        )


def create_figure():
    """Plot the four orbit classes generated by the configured velocities."""
    orbits = [
        orbit_from_tangential_state(
            name,
            M_EARTH,
            INITIAL_RADIUS,
            speed_ratio,
        )
        for name, speed_ratio in CONIC_CASES
    ]

    print_orbit_table(orbits)

    set_plot_options()
    figure, axes = plt.subplots(2, 2, figsize=(10, 9), constrained_layout=True)

    for axes_item, orbit in zip(axes.flat, orbits, strict=True):
        x, y = sample_orbit(
            orbit,
            initial_radius=INITIAL_RADIUS,
            maximum_radius=MAXIMUM_PLOTTED_RADIUS,
            number_of_points=NUMBER_OF_POINTS,
        )
        axes_item.plot(x, y, linewidth=2.0)
        axes_item.add_patch(
            Circle(
                (0.0, 0.0),
                R_EARTH / INITIAL_RADIUS,
                color="#4C78A8",
                alpha=0.75,
                label="Earth",
            )
        )
        axes_item.scatter(
            [1.0],
            [0.0],
            marker="o",
            color="#E45756",
            zorder=3,
            label="initial point",
        )
        axes_item.set_aspect("equal", adjustable="datalim")
        axes_item.set_xlabel(r"$x/r_0$")
        axes_item.set_ylabel(r"$y/r_0$")
        axes_item.set_title(
            rf"{orbit.name}: $e={orbit.eccentricity:.1f}$, "
            rf"$v_0/v_c={orbit.speed_ratio:.3f}$"
        )

    axes[0, 0].legend(loc="upper right")
    figure.suptitle(
        "The initial tangential speed selects the conic section",
        fontsize=14,
    )
    return figure


def main():
    """Run the conic-section experiment using the top-level configuration."""
    figure = create_figure()

    if FIGURE_PATH is not None:
        figure_path = Path(FIGURE_PATH)
        figure_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(figure_path, dpi=200, bbox_inches="tight")
        print(f"Saved figure to {figure_path}")

    if SHOW_FIGURE:
        plt.show()


if __name__ == "__main__":
    main()
