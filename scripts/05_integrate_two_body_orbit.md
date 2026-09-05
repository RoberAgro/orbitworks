# Mathematics used by `05_integrate_two_body_orbit.py`

This note records the equations used by the numerical Earth--Sun example and
clarifies what is meant by the *analytical orbit* in its plots.

## Numerical dynamics

Let $\mathbf r$ be the position of Earth relative to the Sun and let
$\mathbf v=d\mathbf r/dt$. The relative two-body equations in Cartesian
coordinates are

$$
\frac{d\mathbf r}{dt}=\mathbf v,
\qquad
\frac{d\mathbf v}{dt}
=
-\frac{G(M_\odot+M_\oplus)}{|\mathbf r|^3}\mathbf r.
$$

The script integrates these equations in time. No analytical expression for
Earth's position as a function of time is used in the numerical solution.

## Velocity-Verlet discretization

For a time step $\Delta t$, velocity Verlet advances the Cartesian state with

$$
\mathbf r_{n+1}
=
\mathbf r_n
+\mathbf v_n\Delta t
+\frac{1}{2}\mathbf a_n(\Delta t)^2
$$

and

$$
\mathbf v_{n+1}
=
\mathbf v_n
+\frac{1}{2}
\left(
\mathbf a_n+\mathbf a_{n+1}
\right)\Delta t.
$$

Here $\mathbf a_{n+1}$ is evaluated from the newly calculated position
$\mathbf r_{n+1}$. This is the only approximation used to evolve the orbit.

## Initial state at perihelion

The example specifies the semi-major axis $a$ and eccentricity $e$ of Earth's
orbit. It starts the numerical integration at perihelion, where

$$
r_p=a(1-e)
$$

and the velocity is perpendicular to the radius. The perihelion speed follows
from the vis-viva equation:

$$
v_p
=
\sqrt{
G(M_\odot+M_\oplus)
\left(
\frac{2}{r_p}-\frac{1}{a}
\right)
}
=
\sqrt{
\frac{G(M_\odot+M_\oplus)(1+e)}{a(1-e)}
}.
$$

The period used to select the integration duration is

$$
T
=
2\pi
\sqrt{
\frac{a^3}{G(M_\odot+M_\oplus)}
}.
$$

## Analytical comparison: shape only

The analytical curve shown in the plot is the conic derived from Binet's
equation:

$$
r(\theta)
=
\frac{p}{1+e\cos\theta},
\qquad
p=a(1-e^2).
$$

The script samples $\theta$ uniformly only to draw this curve. This tells us
the geometrical path of the orbit but does not say when Earth reaches each
point. The numerical solution alone supplies the time-dependent motion in the
animation.

At every numerical position, the script also compares the calculated radius
with the analytical radius at the same polar angle:

$$
\delta_r
=
\frac{
r_{\mathrm{numerical}}-r_{\mathrm{conic}}(\theta)
}{
r_{\mathrm{conic}}(\theta)
}.
$$

This is a comparison of orbit shapes, not orbital timing.

## Conservation diagnostics

The exact two-body problem conserves the specific orbital energy

$$
\varepsilon
=
\frac{|\mathbf v|^2}{2}
-
\frac{G(M_\odot+M_\oplus)}{|\mathbf r|},
$$

the specific angular momentum

$$
\boldsymbol\ell
=
\mathbf r\times\mathbf v,
$$

and the eccentricity vector

$$
\mathbf e
=
\frac{
\left(
|\mathbf v|^2-rac{G(M_\odot+M_\oplus)}{|\mathbf r|}
\right)\mathbf r
-
(\mathbf r\cdot\mathbf v)\mathbf v
}{
G(M_\odot+M_\oplus)
}.
$$

Their exact values should not change with time. The script plots the absolute
relative numerical deviation in percent,

$$
100
\left|
\frac{q(t)-q(0)}{q(0)}
\right|,
$$

for each scalar conserved quantity.

## Kepler's time equation: not used in the current comparison

An earlier version calculated an analytical position at each time. It used
the mean anomaly $\mathcal M$, eccentric anomaly $E$, and Kepler's equation,

$$
\mathcal M
=
n(t-\tau),
\qquad
n=\sqrt{\frac{G(M_\odot+M_\oplus)}{a^3}},
$$

$$
\boxed{
\mathcal M=E-e\sin E
},
$$

together with

$$
x=a(\cos E-e),
\qquad
y=a\sqrt{1-e^2}\sin E.
$$

These equations provide the analytical kinematics: they determine position
as a function of time. They are useful, but they answer a different question
from the current example and are no longer used by the Python script.
