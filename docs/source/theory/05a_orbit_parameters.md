# Orbit parameters and their relations

The conic orbit equation and the energy relations derived so far introduce a
growing list of quantities — $e$, $p$, $a$, $b$, $c$, $r_p$, $r_a$, $\ell$,
$\varepsilon$ — many of which are not independent. Before relating them
algebraically, this note first rebuilds the geometric picture from scratch:
what the ellipse and hyperbola actually look like as curves, what the
eccentricity means, and how the periapsis and apoapsis distances follow from
elementary geometry rather than from the polar orbit equation alone.

## The geometry of the ellipse and hyperbola

![Ellipse and hyperbola geometry, showing the center, foci, semi-axes, and periapsis/apoapsis distances](conic_geometry.svg)

**The ellipse.** Centered on its own geometric center (not on a focus), an
ellipse with semi-major axis $a$ (half the longest diameter) and semi-minor
axis $b$ (half the shortest diameter) satisfies

$$
\boxed{
\frac{X^2}{a^2}+\frac{y^2}{b^2}=1.
}
$$

An ellipse has **two foci**, located on the major axis a distance $c$ from
the center, defined by the property that the *sum* of the distances from any
point on the curve to the two foci is constant, equal to $2a$. Applying this
to the point directly above the center, at $(0,b)$, both foci are equidistant
from it, so each distance must be $a$; by the Pythagorean theorem on the
right triangle formed by the center, a focus, and that point,

$$
\boxed{
c^2=a^2-b^2.
}
$$

**The hyperbola.** In the analogous center-based picture, a hyperbola with
semi-transverse axis $a$ satisfies

$$
\boxed{
\frac{X^2}{a^2}-\frac{y^2}{b^2}=1,
}
$$

where $b$ now sets the slope $b/a$ of the asymptotes rather than a physical
half-width of the curve. A hyperbola also has two foci on its axis, a
distance $c$ from the center, but now defined by the property that the
*difference* of the distances from any point on either branch to the two foci
is constant, equal to $2a$. The same right-triangle construction (center,
focus, and the point on the asymptote directly above the vertex) now gives

$$
\boxed{
c^2=a^2+b^2.
}
$$

**Eccentricity.** For both curves, the eccentricity is the ratio of the
focal distance to the semi-axis,

$$
\boxed{
e=\frac{c}{a}.
}
$$

Since $c<a$ for an ellipse, $0\le e<1$; since $c>a$ for a hyperbola, $e>1$.
This is consistent with, and equivalent to, the more general focus-directrix
definition used for the orbit equation in {doc}`05_conic_orbits` and needed
for the parabola (which has no center and no second focus at finite
distance):

$$
\boxed{
e=\frac{\text{distance to focus}}{\text{distance to directrix}},
}
$$

a ratio that is the same for every point on the curve. The parabola is
exactly the boundary case $e=1$, reached as $a\to\infty$ with $c/a\to1$.

## Periapsis and apoapsis from the center-based geometry

Only one focus is physical — it is where the central body sits. The
periapsis and apoapsis are simply the distances from *that* focus to the two
vertices of the curve, which lie a distance $a$ from the center along the
axis.

**Ellipse.** The near focus is a distance $c$ from the center, on the same
side as the near vertex. The distance from that focus to the near vertex is
therefore $a-c$, and to the far vertex, $a+c$:

$$
\boxed{
r_p=a-c=a(1-e),
\qquad
r_a=a+c=a(1+e).
}
$$

Both vertices are reachable — the orbit is bound — and $a$ is their average,
$a=(r_p+r_a)/2$.

**Hyperbola.** Only the branch nearer the occupied focus is physical. The
focus is a distance $c$ from the center, beyond the near vertex (since
$c>a$), so the periapsis distance is

$$
\boxed{
r_p=c-a=a(e-1).
}
$$

There is no apoapsis: the branch extends to infinity, and the distance from
the focus grows without bound as the body recedes along the asymptote — the
orbit is unbound.

These are exactly the periapsis/apoapsis relations obtained in
{doc}`05_conic_orbits` from the focus-based polar equation
$r=p/(1+e\cos\theta)$; here they follow directly from the shape of the curve
itself, which is why the figure above is worth keeping in mind through the
rest of this note.

## Glossary of symbols

With the geometry established, here is what each symbol refers to going
forward:

$$
\boxed{
\begin{array}{c|l|l}
\text{Symbol} & \text{Name} & \text{Meaning} \\
\hline
e & \text{eccentricity} & c/a;\ \text{shape of the conic: how elongated it is} \\
a & \text{semi-major/transverse axis} & \text{half the curve's own axis length, measured from its center} \\
b & \text{semi-minor/conjugate axis} & \text{ellipse: half-width; hyperbola: sets asymptote slope } b/a \\
c & \text{focal distance} & \text{distance from the center to either focus} \\
p & \text{semi-latus rectum} & \text{half the chord through the focus, perpendicular to the major axis} \\
r_p & \text{periapsis distance} & \text{closest distance from the occupied focus (central body) to the orbit} \\
r_a & \text{apoapsis distance} & \text{farthest distance from the occupied focus to the orbit (ellipse only)} \\
\ell & \text{specific angular momentum} & r^2\dot\theta,\ \text{conserved; magnitude of }\mathbf r\times\mathbf v \\
\varepsilon & \text{specific mechanical energy} & v^2/2-GM/r,\ \text{conserved} \\
v_c & \text{circular speed} & \text{speed of a circular orbit at a given radius}, \sqrt{GM/r} \\
v_{\mathrm{esc}} & \text{escape speed} & \text{minimum speed to reach }r\to\infty\text{ with zero energy left}
\end{array}
}
$$

Note that $a$ and $b$ describe the curve's own size and shape, measured from
its center, while $r_p$ and $r_a$ describe distances measured from the
occupied focus (the central body) — the two are related but not equal, as
just derived.

Many of these quantities are not independent. This note now asks a single
question directly: **how many numbers are actually needed to pin down a
Keplerian orbit, and how do all the others follow from them?**

## Why the shape and size of the orbit need only two numbers

Binet's equation,

$$
u''+u=\frac{GM}{\ell^2},
$$

has the general solution

$$
u(\theta)=\frac{GM}{\ell^2}+C\cos(\theta-\theta_0).
$$

This solution contains exactly three constants of integration: $\ell$ (which
enters through the equation itself), $C$, and $\theta_0$. Of these, $\theta_0$
only rotates the orbit rigidly about the focus — it fixes *where* periapsis
points, not the *shape* of the curve. Once $\theta_0$ is set aside, the shape
and size of the conic are determined by the remaining two constants, $\ell$
and $C$, equivalently repackaged as $p$ and $e$:

$$
\boxed{
p=\frac{\ell^2}{GM},
\qquad
e=\frac{C\ell^2}{GM}.
}
$$

This is the key structural fact: **for a given central mass $GM$, exactly two
independent parameters fix the size and shape of a Keplerian orbit.** Every
other geometric or dynamical quantity attached to the orbit as a whole (as
opposed to quantities that depend on where the body currently is along the
orbit) can be written in terms of any two of them.

## A catalogue of equivalent parameter pairs

The pair $(a,e)$ is the most common choice, but several other pairs are
equally valid and appear naturally depending on how an orbit is specified.
The conversions below follow directly from results already derived for the
conic orbit ({doc}`05_conic_orbits`) and the orbital energy
({doc}`06_energy_and_orbit_geometry`).

**From $(a,e)$ to periapsis and apoapsis.** Already derived:

$$
\boxed{
r_p=a(1-e),
\qquad
r_a=a(1+e).
}
$$

**From $(r_p,r_a)$ back to $(a,e)$.** Adding and subtracting the two relations
above,

$$
r_p+r_a=2a,
\qquad
r_a-r_p=2ae,
$$

so

$$
\boxed{
a=\frac{r_p+r_a}{2},
\qquad
e=\frac{r_a-r_p}{r_a+r_p}.
}
$$

Thus an orbit can equally well be specified by its two extreme radii instead
of $(a,e)$.

**From $(a,e)$ to the semi-latus rectum and angular momentum.** Already
derived,

$$
p=a(1-e^2),
\qquad
\ell^2=GMp=GMa(1-e^2).
$$

**From $(a,e)$ to energy.** A short derivation, independent of the effective-potential
treatment: at periapsis $\dot r=0$, so the velocity is purely tangential,
$v_p=\ell/r_p$. Using $\ell^2=GMa(1-e^2)$ and $r_p=a(1-e)$,

$$
\varepsilon=\frac{v_p^2}{2}-\frac{GM}{r_p}
=\frac{GMa(1-e^2)}{2a^2(1-e)^2}-\frac{GM}{a(1-e)}
=\frac{GM(1+e)}{2a(1-e)}-\frac{GM}{a(1-e)}.
$$

Combining the two terms over $2a(1-e)$ and simplifying the numerator,
$GM(1+e)-2GM=-GM(1-e)$, gives

$$
\boxed{
\varepsilon=-\frac{GM}{2a}.
}
$$

Remarkably, the energy depends only on $a$: two orbits with the same
semi-major axis but different eccentricities have exactly the same specific
energy. This relation also *defines* $a$ for hyperbolic orbits ($a<0$) and
signals the parabolic limit ($a\to\infty$, $\varepsilon\to0$).

**From $(\varepsilon,\ell)$ to $(a,e)$.** Inverting the relation above gives
$1/a=-2\varepsilon/GM$. Substituting into $\ell^2=GMa(1-e^2)$ and solving for
$e^2$ gives

$$
\boxed{
e^2=1+\frac{2\varepsilon\ell^2}{(GM)^2}.
}
$$

So $(\varepsilon,\ell)$ is another valid pair: energy and angular momentum
alone fix the orbit's shape and size, without ever referring to $\theta$.
This is the pair most directly tied to an initial Cartesian state
$(\mathbf r_0,\mathbf v_0)$, since $\varepsilon$ and $\ell$ are computed from
it immediately.

## Summary of the parameter web

$$
\boxed{
\begin{array}{c|c}
\text{Pair} & \text{Determines} \\
\hline
(a,e) & \text{most common; direct geometric meaning} \\
(r_p,r_a) & \text{extreme distances, e.g. from mission requirements} \\
(p,e) & \text{natural output of the Binet-equation solution} \\
(\varepsilon,\ell) & \text{natural output of an initial state } (\mathbf r_0,\mathbf v_0)
\end{array}
}
$$

Any one pair determines every other quantity in this note: $a$, $e$, $p$,
$r_p$, $r_a$, $\ell$, $\varepsilon$. None of these can be chosen
independently of the other six once two of them are fixed.

## Relating orbital speed to circular speed

The circular speed at radius $r$,

$$
v_c(r)=\sqrt{\frac{GM}{r}},
$$

is a property of the radius alone — it says nothing about eccentricity. The
*actual* speed on an orbit of semi-major axis $a$ at that same radius is given
by the vis-viva equation,

$$
v^2=GM\left(\frac{2}{r}-\frac{1}{a}\right).
$$

Comparing the two, $v>v_c(r)$ whenever $a>r$ (the body is below apoapsis of a
larger, more energetic orbit) and $v<v_c(r)$ whenever $a<r$. The ratio
$v/v_c$ at a single point therefore already encodes information about the
orbit's energy relative to a circular orbit at that radius.

For the special case of a tangential launch at periapsis (so that $r=r_p$ and
$\dot r=0$), this comparison gives eccentricity directly. Since
$\ell=r_pv$ and $p=\ell^2/GM$, substituting into $r_p=p/(1+e)$ and using
$v_c^2=GM/r_p$ gives, after cancellation,

$$
\boxed{
e=\frac{v^2}{v_c^2}-1.
}
$$

This confirms the general picture: knowing the radius and speed at a single
point is *not* enough to fix the orbit in general — a launch angle
(equivalently, the split between $\dot r$ and $r\dot\theta$) is also needed.
Only for the special tangential case does speed alone, combined with the
launch radius, supply the second independent number. In general, one needs
two independent numbers, e.g. $(r,v)$ *and* the flight-path angle, or
equivalently $\mathbf r$ and $\mathbf v$ as vectors — which is exactly two
scalars beyond position, consistent with the two-parameter count established
above.

## The full parameter count for an orbital state

The two numbers above (any pair from the table) fix only the **shape and
size** of the orbit. Fully specifying where a body is, in three-dimensional
space, at a given instant requires more information:

$$
\boxed{
\begin{array}{c|c|l}
\text{Count} & \text{Parameters} & \text{Role} \\
\hline
2 & (a,e)\ \text{or equivalent} & \text{shape and size} \\
2 & (i,\Omega) & \text{orientation of the orbital plane in space} \\
1 & \omega & \text{orientation of periapsis within that plane} \\
1 & \theta_0\ \text{or}\ M_0\ \text{(at a reference epoch } t_0) & \text{position of the body along the orbit}
\end{array}
}
$$

This totals **six** independent numbers, matching the six classical Keplerian
orbital elements $(a,e,i,\Omega,\omega,M_0)$ and the six components of an
initial Cartesian state $(\mathbf r_0,\mathbf v_0)$. The two representations
are two different bases for the same six-dimensional space of possible
two-body states — the algebra connecting them (angular momentum vector,
energy, eccentricity vector, true anomaly) is developed in
{doc}`06a_time_dependent_motion`.

With the geometry of the trajectory now fully parameterized, the remaining
question is how the body moves along it as a function of time — the subject
of that same note.
