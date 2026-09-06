"""Conic-section shape: sampling ``r = p/(1 + e*cos(theta))`` and comparing to it.

This is pure geometry, oriented by an eccentricity vector, with no time
dependence and no reference to a particular unit system.
"""

from __future__ import annotations

from math import acos, atan2, pi

import numpy as np

from orbitworks.analytical import OrbitElements

__all__ = [
    "periapsis_angle",
    "angle_limit_for_radius",
    "sample_conic",
    "conic_shape_error",
]


def periapsis_angle(eccentricity_vector, *, eccentricity=None) -> float:
    """Return the direction of periapsis, or 0.0 for a circle (no fixed periapsis).

    ``eccentricity`` avoids recomputing the norm when already known.
    """
    if eccentricity is None:
        eccentricity = float(np.linalg.norm(eccentricity_vector))
    if eccentricity < 1e-12:
        return 0.0
    return atan2(eccentricity_vector[1], eccentricity_vector[0])


def angle_limit_for_radius(eccentricity, semi_latus_rectum, radius) -> float | None:
    """Return the relative-to-periapsis angle at which the conic reaches ``radius``.

    Returns ``None`` if the branch never reaches that radius (e.g. periapsis
    already lies beyond it). Intended for trimming an open (parabolic or
    hyperbolic) branch to a chosen display or escape radius before sampling.
    """
    cosine = (semi_latus_rectum / radius - 1.0) / eccentricity
    if cosine < -1.0 or cosine > 1.0:
        return None
    return acos(float(np.clip(cosine, -1.0, 1.0)))


def sample_conic(elements: OrbitElements, *, angle_limit=None, num_points=2000):
    """Sample points on the conic described by ``elements``.

    ``angle_limit`` restricts sampling to ``[-angle_limit, angle_limit]``
    relative to periapsis; ``None`` samples a full revolution, appropriate for
    a closed conic (circle or ellipse). Use :func:`angle_limit_for_radius` to
    trim an open branch to a chosen radius.
    """
    angle = periapsis_angle(elements.eccentricity_vector, eccentricity=elements.eccentricity)
    limit = pi if angle_limit is None else angle_limit
    relative_angle = np.linspace(-limit, limit, num_points)
    radius = elements.semi_latus_rectum / (1.0 + elements.eccentricity * np.cos(relative_angle))
    absolute_angle = relative_angle + angle
    return np.column_stack((radius * np.cos(absolute_angle), radius * np.sin(absolute_angle)))


def conic_shape_error(positions, elements: OrbitElements):
    """Return the percentage deviation of sampled radii from the invariant conic.

    ``positions`` is an array of shape ``(N, 2)`` sampled along a numerically
    propagated trajectory; ``elements`` is the :class:`~orbitworks.analytical.OrbitElements`
    computed from the initial state that the conic is expected to follow.
    """
    positions = np.asarray(positions, dtype=float)
    radius = np.linalg.norm(positions, axis=1)
    if elements.eccentricity < 1e-12:
        analytical_radius = np.full_like(radius, elements.semi_latus_rectum)
    else:
        eccentricity_direction = elements.eccentricity_vector / elements.eccentricity
        cosine_from_periapsis = positions @ eccentricity_direction / radius
        analytical_radius = elements.semi_latus_rectum / (
            1.0 + elements.eccentricity * cosine_from_periapsis
        )
    return 100.0 * np.abs(radius - analytical_radius) / analytical_radius
