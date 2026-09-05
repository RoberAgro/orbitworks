# Circular motion and circular orbits

Circular motion provides the simplest bridge between local gravitational
acceleration and a complete orbit. We approach it geometrically first, then
recover the same result from kinematics and Newton's law.

## Why an orbiting body does not simply fall into the central body

An orbiting body is in fact falling continuously toward the central body. The difference between an impact trajectory and an orbit is that the body also has tangential velocity. If a projectile is launched horizontally, gravity bends its path downward. As the launch speed increases, the projectile travels farther before intersecting the surface. At a sufficiently high tangential velocity, the curvature of the projectile's trajectory can exactly match the curvature of the spherical body beneath it. The projectile then continues to fall without ever reaching the surface. That is the geometric essence of a circular orbit.



## Simple projectile derivation of circular orbital speed

Consider a spherical body of radius $R$. A projectile is launched horizontally from near its surface with speed $v$. For a short time interval $\Delta t$, assume the local gravitational
acceleration $g$ is approximately constant.

The horizontal displacement is

$$
\Delta x=v\,\Delta t.
$$

The vertical distance fallen under gravity is

$$
\Delta y
=
\frac{1}{2}g(\Delta t)^2.
$$

Since

$$
\Delta t=\frac{\Delta x}{v},
$$

we obtain

$$
\Delta y
=
\frac{1}{2}g\left(\frac{\Delta x}{v}\right)^2
$$

and therefore

$$
\boxed{
\Delta y
=
\frac{g(\Delta x)^2}{2v^2}
}
$$

Now calculate the vertical distance $\Delta y_{\mathrm{s}}$ by which the
spherical surface curves away over the same horizontal increment $\Delta x$.

From circle geometry,

$$
R^2=(\Delta x)^2+(R-\Delta y_{\mathrm{s}})^2.
$$

Expanding,

$$
R^2
=
(\Delta x)^2+R^2-2R\Delta y_{\mathrm{s}}
+(\Delta y_{\mathrm{s}})^2.
$$

Cancel $R^2$:

$$
0=(\Delta x)^2-2R\Delta y_{\mathrm{s}}
+(\Delta y_{\mathrm{s}})^2.
$$

Rearrange:

$$
2R\Delta y_{\mathrm{s}}-(\Delta y_{\mathrm{s}})^2
=(\Delta x)^2.
$$

For a short distance,

$$
\Delta y_{\mathrm{s}}\ll R.
$$

In the local limit $\Delta x/R\rightarrow 0$, the surface drop
$\Delta y_{\mathrm{s}}$ is of order $(\Delta x)^2/R$. Its square is therefore
of fourth order in $\Delta x$ and vanishes faster than the remaining terms.
Neglecting $(\Delta y_{\mathrm{s}})^2$ gives

$$
2R\Delta y_{\mathrm{s}}\approx(\Delta x)^2.
$$

Thus,

$$
\boxed{
\Delta y_{\mathrm{s}}
\approx
\frac{(\Delta x)^2}{2R}
}
$$

For the projectile to fall at exactly the same local rate as the surface curves away,

$$
\Delta y=\Delta y_{\mathrm{s}}.
$$

Therefore,

$$
\frac{g(\Delta x)^2}{2v^2}
=
\frac{(\Delta x)^2}{2R}.
$$

For any nonzero $\Delta x$, cancel $(\Delta x)^2/2$:

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

Unlike $\Delta x$ and $\Delta y$ in the finite-increment argument above,
$x$ and $y$ here denote coordinates measured from the launch point.

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

## Derivation of centripetal acceleration for a circular trajectory

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
+\cos\omega t
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

---


## General derivation of centripetal acceleration


The familiar expression

$$
a_c=\frac{v^2}{R}
$$

is usually introduced for circular motion, but it is a special case of a more general result. Any object moving along a curved trajectory has an acceleration associated with the change in direction of its velocity, even if its speed remains constant.

Consider an arbitrary smooth trajectory. Let $s$ denote the arc length measured along the trajectory and let $\mathbf e_t$ be the unit vector tangent to it.

The velocity can be written as

$$
\mathbf v=v\,\mathbf e_t,
$$

where

$$
v=\frac{ds}{dt}
$$

is the speed.

Differentiating the velocity with respect to time gives

$$
\mathbf a
=
\frac{d\mathbf v}{dt}
=
\frac{d}{dt}
\left(
v\,\mathbf e_t
\right).
$$

Applying the product rule,

$$
\mathbf a
=
\frac{dv}{dt}\mathbf e_t
+
v\frac{d\mathbf e_t}{dt}.
$$

This expression already reveals two distinct ways in which the velocity can change:

* its **magnitude** can change, through $dv/dt$;
* its **direction** can change, through $d\mathbf e_t/dt$.

The first contribution is straightforward. To understand the second, we need to determine how the tangent vector changes as we move along a curved trajectory.

### Change in the tangent direction

Because $\mathbf e_t$ is a unit vector,

$$
\mathbf e_t\cdot\mathbf e_t=1.
$$

Differentiating with respect to arc length $s$,

$$
\frac{d}{ds}
\left(
\mathbf e_t\cdot\mathbf e_t
\right)
=
0.
$$

Using the product rule,

$$
2\mathbf e_t\cdot
\frac{d\mathbf e_t}{ds}
=
0,
$$

and therefore

$$
\boxed{
\mathbf e_t\cdot
\frac{d\mathbf e_t}{ds}
=
0
}
$$

Thus, $d\mathbf e_t/ds$ is perpendicular to $\mathbf e_t$.

This has a simple geometric interpretation. Since $\mathbf e_t$ always has magnitude one, it cannot change by becoming longer or shorter. It can only change by rotating. Its derivative must therefore point perpendicular to the tangent.

Define the unit normal vector $\mathbf e_n$ to point in the direction in which the tangent vector is turning. We can then write

$$
\frac{d\mathbf e_t}{ds}
=
\left|
\frac{d\mathbf e_t}{ds}
\right|
\mathbf e_n.
$$

The magnitude

$$
\left|
\frac{d\mathbf e_t}{ds}
\right|
$$

measures how rapidly the direction of the trajectory changes per unit distance traveled. This quantity is defined as the **curvature**,

$$
\boxed{
\kappa
=
\left|
\frac{d\mathbf e_t}{ds}
\right|
}
$$

so that

$$
\boxed{
\frac{d\mathbf e_t}{ds}
=
\kappa\,\mathbf e_n
}
$$

A trajectory with large curvature turns rapidly, whereas a trajectory with small curvature turns gradually. A straight line has

$$
\kappa=0.
$$

### Radius of curvature

It is often more intuitive to describe curvature in terms of a radius. The **radius of curvature** $\rho$ is defined as

$$
\boxed{
\rho=\frac{1}{\kappa}
}
$$

and therefore

$$
\boxed{
\frac{d\mathbf e_t}{ds}
=
\frac{1}{\rho}\mathbf e_n
}
$$

The meaning of $\rho$ becomes particularly clear by considering a circle.

For a circle of radius $R$, an infinitesimal displacement along the circumference satisfies

$$
ds=R\,d\theta.
$$

Over the same displacement, the tangent vector rotates through the same infinitesimal angle $d\theta$. Since $\mathbf e_t$ is a unit vector, the magnitude of its infinitesimal change is

$$
|d\mathbf e_t|=d\theta.
$$

Therefore,

$$
\kappa
=
\left|
\frac{d\mathbf e_t}{ds}
\right|
=
\frac{d\theta}{R\,d\theta}
=
\frac{1}{R}.
$$

Thus, for a circle,

$$
\rho=R.
$$

For a general smooth trajectory, $\rho$ can therefore be interpreted as the radius of the circle that locally best matches the curvature of the trajectory: the **osculating circle**.

### Normal and tangential acceleration

We can now return to the acceleration.

Using the chain rule,

$$
\frac{d\mathbf e_t}{dt}
=
\frac{d\mathbf e_t}{ds}
\frac{ds}{dt}.
$$

Since

$$
\frac{ds}{dt}=v
$$

and

$$
\frac{d\mathbf e_t}{ds}
=
\frac{1}{\rho}\mathbf e_n,
$$

we obtain

$$
\frac{d\mathbf e_t}{dt}
=
\frac{v}{\rho}\mathbf e_n.
$$

Substituting this result into

$$
\mathbf a
=
\frac{dv}{dt}\mathbf e_t
+
v\frac{d\mathbf e_t}{dt}
$$

gives

$$
\boxed{
\mathbf a
=
\frac{dv}{dt}\mathbf e_t
+
\frac{v^2}{\rho}\mathbf e_n
}
$$

The acceleration therefore consists of two mutually perpendicular components.

The **tangential acceleration**

$$
\boxed{
a_t=\frac{dv}{dt}
}
$$

changes the magnitude of the velocity and therefore the speed of the object.

The **normal acceleration**

$$
\boxed{
a_n=\frac{v^2}{\rho}
}
$$

changes the direction of the velocity and points toward the local center of curvature.

Thus, an object can accelerate even while moving at constant speed. If the trajectory is curved, the direction of the velocity changes continuously and a normal acceleration is required.

---

## Why closer planets have shorter years


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
v_
=
\sqrt{\frac{GM}{r}}
}
$$

At the same time, the period of the orbit is given by

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

Gravity changes the direction of velocity but not its magnitude in a circular orbit. Therefore the mechanical energy remains constant. A planet does not spiral inward because there is essentially no dissipative drag in an ideal two-body orbital problem.

If a dissipative force were present, mechanical energy would decrease. The orbit would then evolve, typically inward. This is why satellites in low Earth orbit can gradually lose altitude due to atmospheric drag.

