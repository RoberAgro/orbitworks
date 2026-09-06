"""Numerical propagation of the two-body Cartesian equations of motion.

These are unit-agnostic: every function takes the gravitational parameter
``mu`` (and any radius it needs) explicitly, so the same code serves callers
working in SI units and callers working in nondimensional/scaled units
(``mu=1``). State vectors are always the planar Cartesian form
``[x, y, vx, vy]``.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

__all__ = [
    "make_equations_of_motion",
    "make_collision_event",
    "make_escape_event",
    "make_periapsis_turn_event",
    "propagate",
    "refine_radius_crossing",
]


def make_equations_of_motion(mu):
    """Return ``f(t, state)`` for ``d[x,y,vx,vy]/dt`` under inverse-square gravity.

    The acceleration is ``-mu * r / |r|^3``; ``mu`` is fixed by closure so the
    returned function has the plain ``(time, state)`` signature SciPy expects.
    """

    def equations_of_motion(time, state):
        del time
        position = state[:2]
        radius = np.linalg.norm(position)
        acceleration = -mu * position / radius**3
        return np.concatenate((state[2:], acceleration))

    return equations_of_motion


def make_collision_event(collision_radius):
    """Return a terminal event zeroing on an inward crossing of ``collision_radius``."""

    def collision_event(time, state):
        del time
        return np.linalg.norm(state[:2]) - collision_radius

    collision_event.terminal = True
    collision_event.direction = -1.0
    return collision_event


def make_escape_event(escape_radius):
    """Return a terminal event zeroing on an outward crossing of ``escape_radius``."""

    def escape_event(time, state):
        del time
        return np.linalg.norm(state[:2]) - escape_radius

    escape_event.terminal = True
    escape_event.direction = 1.0
    return escape_event


def make_periapsis_turn_event():
    """Return a terminal event zeroing at an inward-to-outward radial turn.

    ``dot(r, v)`` changes sign from negative (still falling inward) to
    positive (now rising) exactly at a radial turning point. A grazing
    trajectory can cross a collision radius twice within one large adaptive
    step; bracketing this turn catches a shallow contact that a simple
    collision event could otherwise miss within that step.
    """

    def periapsis_turn_event(time, state):
        del time
        return np.dot(state[:2], state[2:])

    periapsis_turn_event.terminal = True
    periapsis_turn_event.direction = 1.0
    return periapsis_turn_event


def propagate(
    state0,
    mu,
    duration,
    *,
    events=(),
    method="DOP853",
    rtol=1e-10,
    atol=1e-12,
    dense_output=True,
    t_eval=None,
):
    """Integrate the planar two-body IVP from ``t=0`` to ``duration`` or an event.

    Returns the raw SciPy ``OdeResult``: callers choose how to sample the
    dense solution (uniform grid, adaptive nodes, or both), since that choice
    is presentation-specific rather than part of the physics.
    """
    result = solve_ivp(
        make_equations_of_motion(mu),
        (0.0, duration),
        state0,
        method=method,
        rtol=rtol,
        atol=atol,
        dense_output=dense_output,
        events=list(events) if events else None,
        t_eval=t_eval,
    )
    if not result.success:
        raise RuntimeError(f"Integration did not succeed: {result.message}")
    return result


def refine_radius_crossing(dense_solution, target_radius, bracket, *, xtol=1e-12):
    """Refine the time within ``bracket`` at which position norm hits ``target_radius``.

    ``dense_solution`` is a callable ``t -> state`` such as SciPy's
    ``OdeResult.sol``. Used to pin down a grazing/shallow impact more
    precisely than the raw integration samples would.
    """
    return brentq(
        lambda t: np.linalg.norm(dense_solution(t)[:2]) - target_radius,
        *bracket,
        xtol=xtol,
    )
