# Newtonian gravity and orbital intuition

This chapter establishes Newton's inverse-square law of gravitation and the central physical idea:
an orbiting body is always falling, but its tangential motion keeps it from
intersecting the central body.

## Overview

Planetary motion is one of the clearest examples of how a small number of physical principles can explain a wide range of natural phenomena.

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

Each term in this equation can be interpreted as follows:
- The product $Mm$ shows that the gravitational force is proportional to both masses. At a fixed separation, doubling either mass doubles the force, while doubling both masses increases the force by a factor of four. The dependence is symmetric: each body exerts a force of equal magnitude on the other.
- The factor $1/r^2$ describes how gravity weakens with distance. Because the force follows an inverse-square law, doubling the distance reduces the force to $1/4$ of its original value. At three times the distance, it becomes $1/9$ as strong, and at ten times the distance, $1/100$ as strong.
- Finally, the minus sign specifies the direction of the force. Since $\mathbf e_r$ points radially outward, $-\mathbf e_r$ points toward the central mass. Gravity is therefore an attractive force.

When $M \gg m$, it is usually an excellent approximation to regard $M$ as fixed and study the motion of $m$ in the gravitational field of $M$.

Newton's law can be used to derive Kepler's three laws. Kepler's laws were originally empirical laws: Johannes Kepler inferred them from astronomical observations, especially the very accurate planetary data collected by Tycho Brahe. Newton later showed that the laws follow naturally from inverse-square gravitation and Newtonian mechanics.

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

The acceleration field due to gravity forces can be derived as follows. From Newton's law,

$$
\mathbf F
=
-\frac{GMm}{r^2}\mathbf e_r.
$$

At the same time, Newton's second law of motion states that:

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

## The physical intuition for the inverse-square law

Newton's law of gravitation can be motivated by a few simple physical assumptions. These assumptions do not prove the law or explain why gravity exists, but they make its mathematical form plausible.

First, suppose that a mass $M$ acts as a source of a gravitational field and that the total strength of this field flowing outward through any closed surface surrounding the mass is conserved. For an isolated point mass, there is no preferred direction, so spherical symmetry requires the field to spread uniformly in all directions.

Imagine enclosing the mass by spheres of increasing radius. The surface area of such a sphere is

$$
A=4\pi r^2.
$$

If the same total gravitational flux passes through every sphere, but is distributed over an area that grows as $r^2$, then the field strength must decrease in the same proportion:

$$
g(r)\propto\frac{1}{r^2}.
$$

The inverse-square dependence can therefore be understood geometrically: it is the natural consequence of a conserved radial field spreading through three-dimensional space.

We can now ask how the strength of the interaction should depend on mass. If mass is the source of the gravitational field, and if gravitational contributions add linearly, doubling the source mass $M$ should double the field it produces. Thus,

$$
g\propto M.
$$

A second mass $m$ placed in this field experiences a force. If its response to the field is also linear in its mass, doubling $m$ doubles the force acting on it:

$$
F\propto m.
$$

Combining these two independent proportionalities gives

$$
F\propto Mm.
$$

The product $Mm$, rather than a sum such as $M+m$, follows naturally from this picture. The two masses play different roles in constructing the interaction: one determines the strength of the field, while the other determines how strongly it responds to that field. If either mass were reduced to zero, the gravitational interaction would disappear. A sum $M+m$ would not have this property: it would remain nonzero even if one of the masses vanished.

Combining the dependence on mass with the geometric spreading of the field gives

$$
F\propto\frac{Mm}{r^2}.
$$

Introducing the proportionality constant $G$ and specifying that the force is attractive gives Newton's law,

$$
\mathbf F=-\frac{GMm}{r^2}\,\mathbf e_r.
$$

This reasoning should be understood as a motivation for the structure of the law, not as a fundamental derivation of gravity. It rests on assumptions (spherical symmetry, conservation of gravitational flux, and linear dependence on mass) that are themselves physical statements about how gravity behaves.

---

## How Newton was led to the law

Newton did not arrive at the inverse-square dependence by imagining field
lines. The historical route came primarily from celestial motion. For a nearly
circular orbit, the required centripetal acceleration is

$$
a_c=\frac{4\pi^2r}{T^2}.
$$

Kepler's third law says that $T^2\propto r^3$. Combining the two relations
immediately gives

$$
a_c\propto\frac{r}{r^3}=\frac{1}{r^2}.
$$

Newton also compared the acceleration of the Moon toward Earth with
gravitational acceleration at Earth's surface. The decrease predicted from
the much greater Earth--Moon distance was consistent with the inverse-square
dependence. He subsequently developed the mathematical connection between a
central inverse-square force and Kepler's elliptical orbits.

The idea emerged from a broader seventeenth-century discussion rather than
from Newton in isolation. Robert Hooke had argued for a central attraction and
corresponded with Newton about an inverse-square dependence. In 1684, Edmond
Halley asked Newton what orbit such a force would produce; Newton's work on
that question developed into the *Principia*. Newton's decisive contribution
was the systematic mathematical synthesis: the same mechanics explained
falling bodies near Earth, the Moon's orbit, and planetary motion. See the
[Newton Project's introduction to the texts](https://newtonproject.ox.ac.uk/texts/introduction)
for a concise historical overview.



