"""Physical constants used throughout OrbitWorks.

All values use SI units: metres, kilograms, and seconds. The Newtonian
constant of gravitation is the 2022 CODATA value. Astronomical units and
Solar System gravitational parameters follow the values collected by JPL's
Solar System Dynamics group.

References
----------
https://physics.nist.gov/constants
https://ssd.jpl.nasa.gov/astro_par.html
"""

from typing import Final

__all__ = [
    "AU",
    "DAY",
    "G",
    "M_EARTH",
    "M_JUPITER",
    "M_MARS",
    "M_MERCURY",
    "M_NEPTUNE",
    "M_SATURN",
    "M_SUN",
    "M_URANUS",
    "M_VENUS",
    "MU_EARTH",
    "MU_JUPITER",
    "MU_MARS",
    "MU_MERCURY",
    "MU_NEPTUNE",
    "MU_SATURN",
    "MU_SUN",
    "MU_URANUS",
    "MU_VENUS",
    "R_EARTH",
    "YEAR",
]

# Fundamental and conventional units.
G: Final = 6.67430e-11  # m^3 kg^-1 s^-2; 2022 CODATA
AU: Final = 149_597_870_700.0  # m; exact IAU astronomical unit
DAY: Final = 86_400.0  # s
YEAR: Final = 365.25 * DAY  # s; Julian year

# Gravitational parameters from JPL DE440, converted from km^3/s^2 to m^3/s^2.
# The giant-planet values describe their planetary systems, as used by JPL.
MU_MERCURY: Final = 22_031.868551e9
MU_VENUS: Final = 324_858.592000e9
MU_EARTH: Final = 398_600.435507e9
MU_MARS: Final = 42_828.375816e9
MU_JUPITER: Final = 126_712_764.100000e9
MU_SATURN: Final = 37_940_584.841800e9
MU_URANUS: Final = 5_794_556.400000e9
MU_NEPTUNE: Final = 6_836_527.100580e9
MU_SUN: Final = 1.32712440041279419e20

# Dynamical masses inferred from M = GM/G. In orbital calculations, the
# gravitational parameters above are known much more precisely than these
# masses because the experimental uncertainty in G is comparatively large.
M_MERCURY: Final = MU_MERCURY / G
M_VENUS: Final = MU_VENUS / G
M_EARTH: Final = MU_EARTH / G
M_MARS: Final = MU_MARS / G
M_JUPITER: Final = MU_JUPITER / G
M_SATURN: Final = MU_SATURN / G
M_URANUS: Final = MU_URANUS / G
M_NEPTUNE: Final = MU_NEPTUNE / G
M_SUN: Final = MU_SUN / G

# Mean Earth radius (IUGG conventional mean radius).
R_EARTH: Final = 6_371_008.4  # m
