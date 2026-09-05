# Newtonian gravity and orbital intuition

This chapter establishes the inverse-square law and the central physical idea:
an orbiting body is always falling, but its tangential motion keeps it from
intersecting the central body.

## Overview

Planetary motion is one of the clearest examples of how a small number of physical principles can generate a large amount of structure.

The starting point is Newton's law of universal gravitation,

$$
\boxed{
\mathbf F
=
-\frac{GMm}{r^2}\,\mathbf e_r
}
$$

where:

- $G$ is the gravitational constant,
- $M$ is the central mass,
- $m$ is the orbiting mass,
- $r$ is the distance between the two bodies,
- $\mathbf e_r$ is the outward radial unit vector.

The minus sign indicates that gravity is attractive: the force points toward the central body.

When $M \gg m$, it is usually an excellent approximation to regard $M$ as fixed and study the motion of $m$ in the gravitational field of $M$.

Newton's law can be used to derive Kepler's three laws.

Kepler's laws were originally empirical laws: Johannes Kepler inferred them from astronomical observations, especially the very accurate planetary data collected by Tycho Brahe. Newton later showed that the laws follow naturally from inverse-square gravitation and Newtonian mechanics.

The three Kepler laws are:

1. Planets move in ellipses with the Sun at one focus.
2. The line joining a planet and the Sun sweeps out equal areas in equal times.
3. The square of the orbital period is proportional to the cube of the semi-major axis:

$$
\boxed{
T^2 \propto a^3
}
$$

The aim of this document is to derive these results in a logical progression, beginning with simple algebraic arguments and ending with the differential equation of the orbit.

---

## Gravitational acceleration

From Newton's law,

$$
\mathbf F
=
-\frac{GMm}{r^2}\mathbf e_r.
$$

Newton's second law is

$$
\mathbf F=m\mathbf a.
$$

Therefore,

$$
m\mathbf a
=
-\frac{GMm}{r^2}\mathbf e_r.
$$

Cancel $m$:

$$
\boxed{
\mathbf a
=
-\frac{GM}{r^2}\mathbf e_r
}
$$

so the magnitude of the gravitational acceleration is

$$
\boxed{
g(r)=\frac{GM}{r^2}
}
$$

At the surface of a spherical body of radius $R$,

$$
\boxed{
g=\frac{GM}{R^2}
}
$$

This relation will be useful when connecting surface gravity with orbital velocity.

---

## Why an orbiting body does not simply fall into the central body

An orbiting body is in fact falling continuously toward the central body.

The difference between an impact trajectory and an orbit is that the body also has tangential velocity.

If a projectile is launched horizontally, gravity bends its path downward. As the launch speed increases, the projectile travels farther before intersecting the surface.

At a sufficiently high tangential velocity, the curvature of the projectile's trajectory can exactly match the curvature of the spherical body beneath it. The projectile then continues to fall without ever reaching the surface. That is the geometric essence of a circular orbit.

There is no additional outward force balancing gravity in an inertial frame. Gravity itself is the force that continuously bends the inertial trajectory into a curved path.

