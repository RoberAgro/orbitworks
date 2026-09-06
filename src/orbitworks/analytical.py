"""Closed-form two-body orbital elements, classification, and conservation checks.

Like :mod:`orbitworks.propagation`, every function here takes the
gravitational parameter ``mu`` explicitly, so the same code serves both SI-unit
and nondimensional (``mu=1``) callers. Position and velocity are always the
planar Cartesian vectors ``[x, y]`` / ``[vx, vy]``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt

import numpy as np

__all__ = [
    "OrbitElements",
    "classify_orbit",
    "periapsis_distance",
    "apoapsis_distance",
    "energy_error",
    "angular_momentum_error",
    "eccentricity_vector_error",
]


@dataclass
class OrbitElements:
    """Orbital elements inferred from one Cartesian state, plus its type."""

    orbit_type: str
    specific_energy: float
    specific_angular_momentum: float
    eccentricity_vector: np.ndarray
    eccentricity: float
    semi_latus_rectum: float
    semi_major_axis: float | None
    period: float | None

    @property
    def is_bound(self) -> bool:
        """Return whether the conic has negative energy and a finite period."""
        return self.orbit_type in ("circle", "ellipse")


def classify_orbit(
    position,
    velocity,
    mu,
    *,
    eccentricity_tolerance=1e-8,
    energy_tolerance=1e-10,
) -> OrbitElements:
    """Infer energy, angular momentum, eccentricity, and conic type.

    For position ``r`` and velocity ``v``, the invariants are

        energy = |v|^2/2 - mu/|r|,
        ell = (r x v)_z,
        e_vector = ((|v|^2 - mu/|r|)*r - (r.v)*v) / mu.

    ``energy_tolerance`` is relative to the local gravitational-energy scale
    ``mu/|r|``; energy within that tolerance of zero is classified as a
    parabola. ``eccentricity_tolerance`` distinguishes a circle from a
    (numerically) eccentric ellipse. Angular-momentum degeneracy (a purely
    radial trajectory) is not classified here, since callers differ on how to
    handle it; check ``specific_angular_momentum`` directly if relevant.
    """
    position = np.asarray(position, dtype=float)
    velocity = np.asarray(velocity, dtype=float)
    radius = np.linalg.norm(position)
    speed_squared = float(np.dot(velocity, velocity))
    radial_velocity_product = float(np.dot(position, velocity))

    specific_energy = 0.5 * speed_squared - mu / radius
    specific_angular_momentum = position[0] * velocity[1] - position[1] * velocity[0]
    eccentricity_vector = (
        (speed_squared - mu / radius) * position - radial_velocity_product * velocity
    ) / mu
    eccentricity = float(np.linalg.norm(eccentricity_vector))
    semi_latus_rectum = specific_angular_momentum**2 / mu

    energy_scale = mu / radius
    if abs(specific_energy) <= energy_tolerance * energy_scale:
        orbit_type = "parabola"
        semi_major_axis = None
        period = None
    elif specific_energy < 0.0:
        semi_major_axis = -mu / (2.0 * specific_energy)
        period = 2.0 * pi * sqrt(semi_major_axis**3 / mu)
        orbit_type = "circle" if eccentricity < eccentricity_tolerance else "ellipse"
    else:
        semi_major_axis = -mu / (2.0 * specific_energy)
        period = None
        orbit_type = "hyperbola"

    return OrbitElements(
        orbit_type,
        specific_energy,
        specific_angular_momentum,
        eccentricity_vector,
        eccentricity,
        semi_latus_rectum,
        semi_major_axis,
        period,
    )


def periapsis_distance(elements: OrbitElements) -> float:
    """Return ``p / (1 + e)``, the closest distance to the focus."""
    return elements.semi_latus_rectum / (1.0 + elements.eccentricity)


def apoapsis_distance(elements: OrbitElements) -> float | None:
    """Return ``a * (1 + e)`` for a bound orbit, or ``None`` if unbound."""
    if not elements.is_bound:
        return None
    return elements.semi_major_axis * (1.0 + elements.eccentricity)


def energy_error(positions, velocities, mu, reference: OrbitElements, *, scale=None):
    """Return the percentage deviation of specific energy from ``reference``.

    ``positions``/``velocities`` are arrays of shape ``(N, 2)`` sampled along a
    numerically propagated trajectory. Pass ``scale`` explicitly for a
    parabola, whose reference energy is zero and cannot normalize itself.
    """
    positions = np.asarray(positions, dtype=float)
    velocities = np.asarray(velocities, dtype=float)
    radius = np.linalg.norm(positions, axis=1)
    speed_squared = np.sum(velocities**2, axis=1)
    energy = 0.5 * speed_squared - mu / radius
    if scale is None:
        scale = abs(reference.specific_energy)
    return 100.0 * np.abs(energy - reference.specific_energy) / scale


def angular_momentum_error(positions, velocities, reference: OrbitElements):
    """Return the percentage deviation of specific angular momentum from ``reference``.

    Undefined (``nan``) for a reference angular momentum of zero (a radial
    trajectory), since there is nothing to take a relative deviation against.
    """
    positions = np.asarray(positions, dtype=float)
    velocities = np.asarray(velocities, dtype=float)
    angular_momentum = positions[:, 0] * velocities[:, 1] - positions[:, 1] * velocities[:, 0]
    with np.errstate(invalid="ignore", divide="ignore"):
        return (
            100.0
            * np.abs(angular_momentum - reference.specific_angular_momentum)
            / abs(reference.specific_angular_momentum)
        )


def eccentricity_vector_error(positions, velocities, mu, reference: OrbitElements):
    """Return the percentage deviation of the eccentricity vector from ``reference``."""
    positions = np.asarray(positions, dtype=float)
    velocities = np.asarray(velocities, dtype=float)
    radius = np.linalg.norm(positions, axis=1)
    speed_squared = np.sum(velocities**2, axis=1)
    radial_velocity_product = np.sum(positions * velocities, axis=1)
    eccentricity_vector = (
        (speed_squared - mu / radius)[:, np.newaxis] * positions
        - radial_velocity_product[:, np.newaxis] * velocities
    ) / mu
    return (
        100.0
        * np.linalg.norm(eccentricity_vector - reference.eccentricity_vector, axis=1)
        / max(reference.eccentricity, 1.0)
    )
