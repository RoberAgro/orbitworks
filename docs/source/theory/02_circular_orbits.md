# Circular motion and circular orbits

Circular motion provides the simplest bridge between local gravitational
acceleration and a complete orbit. We approach it geometrically first, then
recover the same result from kinematics and Newton's law.

## Simple projectile derivation of circular orbital speed

Consider a spherical body of radius $R$. A projectile is launched horizontally from near its surface with speed $v$.

For a short interval $t$, assume the local gravitational acceleration $g$ is approximately constant.

The horizontal displacement is

$$
x=vt.
$$

The vertical distance fallen under gravity is

$$
y_{\mathrm{fall}}
=
\frac{1}{2}gt^2.
$$

Since

$$
t=\frac{x}{v},
$$

we obtain

$$
y_{\mathrm{fall}}
=
\frac{1}{2}g\left(\frac{x}{v}\right)^2
$$

and therefore

$$
\boxed{
y_{\mathrm{fall}}
=
\frac{gx^2}{2v^2}
}
$$

Now calculate how much the spherical surface curves away over the same horizontal distance $x$.

From circle geometry,

$$
R^2=x^2+(R-y)^2.
$$

Expanding,

$$
R^2
=
x^2+R^2-2Ry+y^2.
$$

Cancel $R^2$:

$$
0=x^2-2Ry+y^2.
$$

Rearrange:

$$
2Ry-y^2=x^2.
$$

For a short distance,

$$
y\ll R,
$$

so $y^2$ is negligible compared with $2Ry$. Hence,

$$
2Ry\approx x^2.
$$

Thus,

$$
\boxed{
y_{\mathrm{surface}}
\approx
\frac{x^2}{2R}
}
$$

For the projectile to fall at exactly the same local rate as the surface curves away,

$$
y_{\mathrm{fall}}
=
y_{\mathrm{surface}}.
$$

Therefore,

$$
\frac{gx^2}{2v^2}
=
\frac{x^2}{2R}.
$$

Cancel $x^2/2$:

$$
\frac{g}{v^2}
=
\frac{1}{R}.
$$

Hence,

$$
\boxed{
v^2=gR
}
$$

and

$$
\boxed{
v=\sqrt{gR}
}
$$

Using

$$
g=\frac{GM}{R^2},
$$

we get

$$
v
=
\sqrt{\frac{GM}{R^2}R}
$$

so

$$
\boxed{
v=\sqrt{\frac{GM}{R}}
}
$$

This is the circular orbital velocity at radius $R$.

For Earth,

$$
g\approx 9.81\ \mathrm{m/s^2},
\qquad
R\approx 6.371\times10^6\ \mathrm{m},
$$

so

$$
v
=
\sqrt{9.81(6.371\times10^6)}
\approx
7.91\times10^3\ \mathrm{m/s}.
$$

Thus,

$$
\boxed{
v\approx 7.9\ \mathrm{km/s}
}
$$

ignoring atmosphere and Earth's rotation.

---

## Differential form of the projectile-curvature argument

The previous derivation compares small finite displacements. A cleaner formulation compares local curvature directly.

Take a local coordinate system tangent to the surface at launch:

- $x$: tangential coordinate,
- $y$: inward coordinate toward the center.

At the instant of launch,

$$
\dot x=v,
\qquad
\dot y=0,
$$

and locally,

$$
\ddot y=g,
\qquad
\ddot x=0.
$$

We want the shape $y(x)$.

By the chain rule,

$$
\frac{dy}{dx}
=
\frac{\dot y}{\dot x}.
$$

Differentiate again with respect to $x$:

$$
\frac{d^2y}{dx^2}
=
\frac{1}{\dot x}
\frac{d}{dt}
\left(
\frac{\dot y}{\dot x}
\right).
$$

Using the quotient rule,

$$
\frac{d}{dt}
\left(
\frac{\dot y}{\dot x}
\right)
=
\frac{
\ddot y\dot x-\dot y\ddot x
}{
\dot x^2
}.
$$

Therefore,

$$
\frac{d^2y}{dx^2}
=
\frac{
\ddot y\dot x-\dot y\ddot x
}{
\dot x^3
}.
$$

At launch,

$$
\dot y=0,
\qquad
\ddot x=0,
\qquad
\dot x=v,
\qquad
\ddot y=g.
$$

Hence,

$$
\boxed{
\left.
\frac{d^2y}{dx^2}
\right|_0
=
\frac{g}{v^2}
}
$$

The curvature of a planar curve $y(x)$ is

$$
\kappa
=
\frac{|y''|}
{\left(1+y'^2\right)^{3/2}}.
$$

At launch,

$$
y'=0,
$$

so

$$
\boxed{
\kappa_{\mathrm{projectile}}
=
\frac{g}{v^2}
}
$$

For a circle of radius $R$,

$$
\boxed{
\kappa_{\mathrm{circle}}
=
\frac{1}{R}
}
$$

Matching the two curvatures gives

$$
\frac{g}{v^2}
=
\frac{1}{R}.
$$

Hence,

$$
\boxed{
v=\sqrt{gR}
}
$$

This formulation makes the geometry explicit: a circular orbit occurs when gravity bends the trajectory with exactly the curvature $1/R$.

---

## Systematic derivation of centripetal acceleration

Consider uniform circular motion of radius $R$ with constant angular speed $\omega$.

The position vector is

$$
\mathbf r(t)
=
R
\begin{bmatrix}
\cos\omega t\\
\sin\omega t
\end{bmatrix}.
$$

Differentiate once:

$$
\mathbf v(t)
=
\frac{d\mathbf r}{dt}
=
R\omega
\begin{bmatrix}
-\sin\omega t\\
\cos\omega t
\end{bmatrix}.
$$

Its magnitude is

$$
|\mathbf v|
=
R\omega
\sqrt{
\sin^2\omega t+\cos^2\omega t
}.
$$

Therefore,

$$
\boxed{
v=R\omega
}
$$

The velocity is tangent to the circle because

$$
\mathbf r\cdot\mathbf v=0.
$$

Differentiate again:

$$
\mathbf a(t)
=
\frac{d\mathbf v}{dt}
=
-R\omega^2
\begin{bmatrix}
\cos\omega t\\
\sin\omega t
\end{bmatrix}.
$$

Since

$$
\mathbf r(t)
=
R
\begin{bmatrix}
\cos\omega t\\
\sin\omega t
\end{bmatrix},
$$

we obtain

$$
\boxed{
\mathbf a
=
-\omega^2\mathbf r
}
$$

The acceleration is therefore directed toward the center.

Its magnitude is

$$
a_c=\omega^2R.
$$

Using

$$
v=\omega R,
$$

we have

$$
\omega=\frac{v}{R}.
$$

Hence,

$$
a_c
=
R\left(\frac{v}{R}\right)^2
$$

and therefore

$$
\boxed{
a_c=\frac{v^2}{R}
}
$$

This is the centripetal acceleration.

---

## Curvature form of normal acceleration

For any trajectory followed at speed $v$, the normal component of acceleration is

$$
\boxed{
a_n=v^2\kappa
}
$$

where $\kappa$ is the local curvature of the trajectory.

For a circle,

$$
\kappa=\frac{1}{R},
$$

so

$$
\boxed{
a_n=\frac{v^2}{R}
}
$$

This is the general geometric interpretation of centripetal acceleration.

The same relation appears in fluid mechanics for a fluid particle moving along a curved streamline:

$$
\boxed{
a_n=\frac{V^2}{R_c}
}
$$

where $R_c$ is the local radius of curvature of the streamline.

---

## Circular orbit from Newtonian gravity

For a circular orbit of radius $r$, gravity provides the centripetal acceleration.

Thus,

$$
\frac{GM}{r^2}
=
\frac{v^2}{r}.
$$

Multiply by $r$:

$$
\frac{GM}{r}
=
v^2.
$$

Therefore,

$$
\boxed{
v_c
=
\sqrt{\frac{GM}{r}}
}
$$

If we define

$$
\mu=GM,
$$

then

$$
\boxed{
v_c=\sqrt{\frac{\mu}{r}}
}
$$

This immediately shows that planets closer to the Sun move faster:

$$
\boxed{
v_c\propto r^{-1/2}
}
$$

A smaller orbital radius implies a larger orbital speed.

---

## Why closer planets have shorter years

For a circular orbit,

$$
T
=
\frac{2\pi r}{v}.
$$

Substitute

$$
v=\sqrt{\frac{GM}{r}}.
$$

Then

$$
T
=
\frac{2\pi r}
{\sqrt{GM/r}}.
$$

Rewrite:

$$
T
=
2\pi
\frac{r^{3/2}}{\sqrt{GM}}.
$$

Thus,

$$
\boxed{
T
=
2\pi\sqrt{\frac{r^3}{GM}}
}
$$

and therefore

$$
\boxed{
T^2
=
\frac{4\pi^2}{GM}r^3
}
$$

so

$$
\boxed{
T^2\propto r^3
}
$$

This is Kepler's third law for circular orbits.

There are two reasons closer planets have shorter years:

1. They travel around a smaller orbit.
2. They move faster because $v\propto r^{-1/2}$.

Both effects shorten the orbital period.

For elliptical orbits, the same law holds with $r$ replaced by the semi-major axis $a$:

$$
\boxed{
T^2
=
\frac{4\pi^2}{GM}a^3
}
$$

This will be derived later from the general orbital solution.

---

## Why circular orbits do not spiral inward

For a circular orbit, gravitational force is radial while velocity is tangential.

Therefore,

$$
\mathbf F\cdot\mathbf v=0.
$$

The instantaneous power delivered by a force is

$$
P=\mathbf F\cdot\mathbf v.
$$

Hence,

$$
\boxed{
P=0
}
$$

for an ideal circular gravitational orbit.

Gravity changes the direction of velocity but not its magnitude in a circular orbit.

Therefore the mechanical energy remains constant.

A planet does not spiral inward because there is essentially no dissipative drag in an ideal two-body orbital problem.

If a dissipative force were present, mechanical energy would decrease. The orbit would then evolve, typically inward. This is why satellites in low Earth orbit can gradually lose altitude due to atmospheric drag.

