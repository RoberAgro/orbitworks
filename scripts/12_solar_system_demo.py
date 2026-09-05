"""Plot idealized two-body orbits for all eight Solar System planets.

Planetary mass does not uniquely determine an orbit. Each orbit also needs an
initial state, represented here by its J2000 semi-major axis, eccentricity,
and longitude of perihelion. The script reconstructs the perihelion state,
calculates the specific angular momentum, and evaluates the conic equation.

Orbital elements:
https://ssd.jpl.nasa.gov/planets/approx_pos.html
"""

from math import pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from orbitworks.constants import (
    AU,
    G,
    M_EARTH,
    M_JUPITER,
    M_MARS,
    M_MERCURY,
    M_NEPTUNE,
    M_SATURN,
    M_SUN,
    M_URANUS,
    M_VENUS,
    YEAR,
)
from orbitworks.graphics_mpl import set_plot_options

# User configuration.
NUMBER_OF_POINTS = 1_500
SHOW_FIGURE = True
FIGURE_PATH = None  # For example: "solar_system_orbits.png"


class Planet:
    """Store independent physical data and approximate J2000 orbit elements."""

    def __init__(
        self,
        name,
        mass,
        semi_major_axis_au,
        eccentricity,
        longitude_of_perihelion_deg,
        color,
    ):
        self.name = name
        self.mass = mass
        self.semi_major_axis_au = semi_major_axis_au
        self.eccentricity = eccentricity
        self.longitude_of_perihelion_deg = longitude_of_perihelion_deg
        self.color = color


class CalculatedOrbit:
    """Store orbital quantities derived from a planet's independent data."""

    def __init__(
        self,
        planet,
        gravitational_parameter,
        perihelion_radius,
        perihelion_speed,
        specific_angular_momentum,
        semi_latus_rectum,
        period,
    ):
        self.planet = planet
        self.gravitational_parameter = gravitational_parameter
        self.perihelion_radius = perihelion_radius
        self.perihelion_speed = perihelion_speed
        self.specific_angular_momentum = specific_angular_momentum
        self.semi_latus_rectum = semi_latus_rectum
        self.period = period


# Approximate elements at J2000 from JPL's 1800--2050 element table. The Earth
# row uses the Earth--Moon barycenter, consistent with that source.
PLANETS = (
    Planet("Mercury", M_MERCURY, 0.38709927, 0.20563593, 77.45779628, "#7f7f7f"),
    Planet("Venus", M_VENUS, 0.72333566, 0.00677672, 131.60246718, "#D9A441"),
    Planet("Earth", M_EARTH, 1.00000261, 0.01671123, 102.93768193, "#2E86DE"),
    Planet("Mars", M_MARS, 1.52371034, 0.09339410, -23.94362959, "#C1440E"),
    Planet("Jupiter", M_JUPITER, 5.20288700, 0.04838624, 14.72847983, "#B07D52"),
    Planet("Saturn", M_SATURN, 9.53667594, 0.05386179, 92.59887831, "#D8C27A"),
    Planet("Uranus", M_URANUS, 19.18916464, 0.04725744, 170.95427630, "#73C7C7"),
    Planet("Neptune", M_NEPTUNE, 30.06992276, 0.00859048, 44.96476227, "#3155A6"),
)


def calculate_orbit(planet):
    """Calculate dependent orbital quantities from the independent inputs.

    The relative two-body parameter is ``G(M_sun + m)``. For an ellipse,

        r_p = a(1 - e),
        v_p = sqrt(GM(1 + e)/(a(1 - e))),
        ell = r_p*v_p,
        p = ell**2/GM,
        T = 2*pi*sqrt(a**3/GM).

    Planetary mass affects speeds and periods, while ``a``, ``e``, and the
    perihelion longitude independently specify size, shape, and orientation.
    """
    semi_major_axis = planet.semi_major_axis_au * AU
    eccentricity = planet.eccentricity

    # The relative two-body equation uses G times the sum of both masses.
    gravitational_parameter = G * (M_SUN + planet.mass)
    perihelion_radius = semi_major_axis * (1.0 - eccentricity)

    # Vis-viva evaluated at perihelion, where velocity is purely tangential.
    perihelion_speed = sqrt(
        gravitational_parameter
        * (1.0 + eccentricity)
        / (semi_major_axis * (1.0 - eccentricity))
    )
    specific_angular_momentum = perihelion_radius * perihelion_speed
    semi_latus_rectum = specific_angular_momentum**2 / gravitational_parameter
    period = 2.0 * pi * sqrt(semi_major_axis**3 / gravitational_parameter)

    return CalculatedOrbit(
        planet=planet,
        gravitational_parameter=gravitational_parameter,
        perihelion_radius=perihelion_radius,
        perihelion_speed=perihelion_speed,
        specific_angular_momentum=specific_angular_momentum,
        semi_latus_rectum=semi_latus_rectum,
        period=period,
    )


def sample_orbit(
    orbit,
    number_of_points,
):
    """Evaluate ``r=p/(1+e*cos(theta))`` and rotate it to perihelion.

    The conic equation first gives coordinates with perihelion on the positive
    x-axis. Adding the longitude of perihelion rotates that curve into its
    approximate J2000 orientation in the ecliptic plane.
    """
    theta = np.linspace(0.0, 2.0 * pi, number_of_points)
    radius = orbit.semi_latus_rectum / (1.0 + orbit.planet.eccentricity * np.cos(theta))

    longitude = np.deg2rad(orbit.planet.longitude_of_perihelion_deg)
    x = radius * np.cos(theta + longitude) / AU
    y = radius * np.sin(theta + longitude) / AU
    return x, y


def print_orbit_table(orbits):
    """Print independent orbital inputs and selected calculated quantities."""
    print(
        f"{'planet':<9} {'mass [kg]':>13} {'a [AU]':>9} {'e':>9} "
        f"{'vp [km/s]':>11} {'period [yr]':>12}"
    )
    for orbit in orbits:
        planet = orbit.planet
        print(
            f"{planet.name:<9} "
            f"{planet.mass:13.5e} "
            f"{planet.semi_major_axis_au:9.4f} "
            f"{planet.eccentricity:9.5f} "
            f"{orbit.perihelion_speed / 1e3:11.3f} "
            f"{orbit.period / YEAR:12.3f}"
        )


def plot_orbits(
    axes,
    orbits,
    title,
):
    """Plot selected conic paths with the Sun at their common focus."""
    axes.scatter(
        [0.0],
        [0.0],
        s=90,
        color="#FDB813",
        edgecolor="#9C6B00",
        linewidth=0.8,
        zorder=4,
        label="Sun",
    )

    for orbit in orbits:
        x, y = sample_orbit(orbit, NUMBER_OF_POINTS)
        axes.plot(
            x,
            y,
            color=orbit.planet.color,
            linewidth=1.7,
            label=orbit.planet.name,
        )

    axes.set_aspect("equal", adjustable="box")
    axes.set_xlabel("x [AU]")
    axes.set_ylabel("y [AU]")
    axes.set_title(title)
    axes.grid(alpha=0.35)
    axes.legend(fontsize=9, ncols=2, loc="best")


def create_figure():
    """Create separate views so both inner and outer orbits remain legible."""
    calculated_orbits = tuple(calculate_orbit(planet) for planet in PLANETS)
    print_orbit_table(calculated_orbits)

    set_plot_options(fontsize=11, color_order="matlab", linewidth=1.5)
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(14, 7),
        constrained_layout=True,
    )
    plot_orbits(axes[0], calculated_orbits[:4], "Inner planets")
    plot_orbits(axes[1], calculated_orbits, "All eight planets")
    figure.suptitle(
        "Idealized J2000 Keplerian orbits (coplanar projection)",
        fontsize=15,
    )
    return figure


def main():
    """Run the Solar System example using the top-level configuration."""
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
