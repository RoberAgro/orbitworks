# From Newton's equation to conic sections

Eliminating time from the radial equation turns the dynamical problem into an
equation for the orbit's shape. Its solutions are the familiar conic sections:
circles, ellipses, parabolas, and hyperbolas.

## Reduction of the orbital equation with a change of variable

Return to the radial equation,

$$
\ddot r-r\dot\theta^2
=
-\frac{GM}{r^2}.
$$

We first eliminate time and derive an equation directly for the orbit
$r(\theta)$. The reciprocal-radius substitution will be introduced only after
that equation has been obtained.

Treat $r$ as a function of $\theta$. From conservation of angular
momentum,

$$
\dot\theta=\frac{\ell}{r^2}.
$$

The chain rule then converts the first time derivative of $r$ into an angular
derivative:

$$
\dot r
=
\frac{dr}{d\theta}\dot\theta
=
\frac{\ell}{r^2}\frac{dr}{d\theta}.
$$

For the second time derivative, apply the same rule once more:

$$
\begin{aligned}
\ddot r
&=
\frac{d}{dt}
\left(
\frac{\ell}{r^2}\frac{dr}{d\theta}
\right) \\
&=
\dot\theta\frac{d}{d\theta}
\left(
\frac{\ell}{r^2}\frac{dr}{d\theta}
\right) \\
&=
\frac{\ell^2}{r^2}
\frac{d}{d\theta}
\left(
\frac{1}{r^2}\frac{dr}{d\theta}
\right) \\
&=
\frac{\ell^2}{r^4}\frac{d^2r}{d\theta^2}
-
\frac{2\ell^2}{r^5}
\left(
\frac{dr}{d\theta}
\right)^2.
\end{aligned}
$$

The angular part of the radial acceleration is

$$
r\dot\theta^2
=
\frac{\ell^2}{r^3}.
$$

Substitute these expressions into

$$
\ddot r-r\dot\theta^2=-\frac{GM}{r^2}
$$

and multiply by $r^5/\ell^2$. The time-dependent radial equation becomes the
following differential equation for the orbit $r(\theta)$:

$$
\boxed{
r\frac{d^2r}{d\theta^2}
-
2\left(
\frac{dr}{d\theta}
\right)^2
-
r^2
=
-\frac{GM}{\ell^2}r^3
}.
$$

This is a nonlinear second-order ODE for $r(\theta)$. It is nonlinear because
the unknown function multiplies its own second derivative, the first
derivative is squared, and powers such as $r^2$ and $r^3$ appear. In a linear
ODE, the unknown function and each of its derivatives may occur only to the
first power and may not be multiplied by one another.

The structure of this equation motivates the reciprocal-radius substitution

$$
u(\theta)=\frac{1}{r(\theta)}
,
\qquad
r(\theta)=\frac{1}{u(\theta)}.
$$

The required angular derivatives are

$$
\frac{dr}{d\theta}
=
-\frac{1}{u^2}\frac{du}{d\theta}
$$

and

$$
\frac{d^2r}{d\theta^2}
=
\frac{2}{u^3}
\left(
\frac{du}{d\theta}
\right)^2
-
\frac{1}{u^2}\frac{d^2u}{d\theta^2}.
$$

Substitute these derivatives into the left-hand side of the nonlinear
equation:

$$
\begin{aligned}
r\frac{d^2r}{d\theta^2}
-2\left(\frac{dr}{d\theta}\right)^2-r^2
&=
\frac{1}{u}
\left[
\frac{2}{u^3}
\left(\frac{du}{d\theta}\right)^2
-
\frac{1}{u^2}\frac{d^2u}{d\theta^2}
\right] \\
&\quad
-
\frac{2}{u^4}
\left(\frac{du}{d\theta}\right)^2
-
\frac{1}{u^2} \\
&=
-\frac{1}{u^3}\frac{d^2u}{d\theta^2}
-
\frac{1}{u^2}.
\end{aligned}
$$

The two terms containing $(du/d\theta)^2$ cancel exactly. The right-hand side
of the nonlinear equation becomes $-(GM/\ell^2)u^{-3}$, so the transformed
equation is

$$
-\frac{1}{u^3}\frac{d^2u}{d\theta^2}
-
\frac{1}{u^2}
=
-\frac{GM}{\ell^2}\frac{1}{u^3}.
$$

Multiplying by $-u^3$ recovers Binet's linear equation,

$$
\boxed{
\frac{d^2u}{d\theta^2}+u
=
\frac{GM}{\ell^2}
}.
$$

This cancellation is the main reason the reciprocal radius $u=1/r$ is the
natural variable for an inverse-square central force. It turns the nonlinear
equation for $r(\theta)$ into a linear, constant-coefficient ODE for
$u(\theta)$.

---

## Solution of the orbital differential equation

Binet's equation is a linear differential equation with a constant
right-hand side. Its general solution is

$$
u(\theta)
=
\frac{GM}{\ell^2}
+A\cos\theta
+B\sin\theta.
$$

The two trigonometric terms can be written as a single shifted cosine,

$$
A\cos\theta+B\sin\theta
=
C\cos(\theta-\theta_0),
$$

so

$$
u(\theta)
=
\frac{GM}{\ell^2}
+C\cos(\theta-\theta_0).
$$

The angle $\theta_0$ only determines the orientation of the orbit. Choose the
angular origin at periapsis, so that $\theta_0=0$. The solution then becomes

$$
u(\theta)
=
\frac{GM}{\ell^2}
\left(
1+
\frac{C\ell^2}{GM}\cos\theta
\right).
$$

The solution contains two combinations of constants that are useful to name.
Define

$$
\boxed{
e=\frac{C\ell^2}{GM}
},
\qquad
\boxed{
p=\frac{\ell^2}{GM}
}.
$$

These definitions do not yet assume a particular orbit shape. The constant
$C$ and the quantity $GM/\ell^2$ both have dimensions of inverse length, so
$e$ is dimensionless. In contrast, $p$ has dimensions of length and sets the
radial scale of the orbit.

Since $u=1/r$, these definitions put the solution in the compact form

$$
\boxed{
r(\theta)
=
\frac{p}{1+e\cos\theta}
}.
$$

We can now identify the geometry rather than assume it. Take the central mass,
located at the origin, as a **focus**, and use $x=r\cos\theta$. Rearranging the
orbit equation gives

$$
\begin{aligned}
r(1+e\cos\theta)&=p, \\
r+ex&=p, \\
r&=e\left(\frac{p}{e}-x\right).
\end{aligned}
$$

For $e>0$, the line $x=p/e$ is the **directrix**. On the branch described by
the orbit equation, $p/e-x$ is the perpendicular distance from the orbiting
body to this line. Thus,

$$
\boxed{
\frac{\text{distance to the focus}}
{\text{distance to the directrix}}
=e
}.
$$

A conic section is precisely a curve for which this ratio is constant. This
is why $e$ is called the **eccentricity**: it is the focus-to-directrix distance
ratio that determines whether the conic is a circle, ellipse, parabola, or
hyperbola. When $e=0$, the orbit equation reduces directly to the circle
$r=p$.

The geometric meaning of $p$ follows by looking perpendicular to the orbit's
symmetry axis. At $\theta=\pm\pi/2$,

$$
\cos\theta=0,
\qquad
r=p.
$$

The two corresponding points lie on the line through the focus perpendicular
to the symmetry axis, one a distance $p$ above the focus and the other a
distance $p$ below it. The chord joining them therefore has length $2p$:

$$
\boxed{
\text{latus rectum}=2p
},
\qquad
\boxed{
\text{semi-latus rectum}=p
}.
$$

The **latus rectum** is the chord through a focus that is parallel to the
directrix, or equivalently perpendicular to the conic's symmetry axis. The
historical New Latin term means "straight side"; *semi-* indicates that $p$
is half the length of this chord.

We have therefore derived, rather than presumed, that
$r=p/(1+e\cos\theta)$ is the polar equation of a conic with the central mass
at one focus. One equation describes every possible Keplerian orbit.

---

## Classification by eccentricity

The eccentricity $e$ determines which conic section the trajectory follows.

| Eccentricity | Trajectory | Character |
| --- | --- | --- |
| $e=0$ | Circle | Bound orbit with constant radius $r=p$ |
| $0<e<1$ | Ellipse | Bound orbit |
| $e=1$ | Parabola | Boundary between bound and unbound motion |
| $e>1$ | Hyperbola | Unbound orbit |

Thus, Newton's inverse-square gravitational law naturally generates the full
family of conic sections.

---

## Conversion from polar conic form to Cartesian ellipse form

For an elliptical orbit, $0<e<1$. Starting from

$$
r=\frac{p}{1+e\cos\theta},
$$

use

$$
x=r\cos\theta,
\qquad
y=r\sin\theta,
\qquad
r=\sqrt{x^2+y^2}.
$$

Multiplying the polar equation by its denominator gives $r+ex=p$.
Substituting $r=\sqrt{x^2+y^2}$, squaring, and collecting terms produces

$$
\begin{aligned}
\sqrt{x^2+y^2}&=p-ex, \\
x^2+y^2&=(p-ex)^2, \\
(1-e^2)x^2+2epx+y^2&=p^2.
\end{aligned}
$$

Completing the square in $x$ gives

$$
(1-e^2)
\left(
x+\frac{ep}{1-e^2}
\right)^2
+y^2
=
\frac{p^2}{1-e^2}.
$$

After dividing by the right-hand side,

$$
\frac{
\left(
x+\frac{ep}{1-e^2}
\right)^2
}{
\frac{p^2}{(1-e^2)^2}
}
+
\frac{y^2}{
\frac{p^2}{1-e^2}
}
=
1.
$$

Define the semi-major axis $a$ and semi-minor axis $b$ as

$$
\boxed{
a=\frac{p}{1-e^2}
},
\qquad
\boxed{
b=\frac{p}{\sqrt{1-e^2}}
}.
$$

These definitions imply

$$
\boxed{
p=a(1-e^2)
},
\qquad
\boxed{
b=a\sqrt{1-e^2}
}.
$$

The Cartesian equation is therefore

$$
\boxed{
\frac{(x+ae)^2}{a^2}
+
\frac{y^2}{b^2}
=
1
}.
$$

The ellipse is centered at $x=-ae$, while the central mass remains at the
origin. Thus, the distance from the center to the focus is

$$
\boxed{
c=ae
}.
$$

The central mass lies at a focus rather than at the geometrical center of the
ellipse. This is Kepler's first law.

---

## Periapsis and apoapsis

For the orbit

$$
r(\theta)=\frac{p}{1+e\cos\theta},
$$

the smallest radius occurs at $\theta=0$, where $\cos\theta=1$, and the largest
radius occurs at $\theta=\pi$, where $\cos\theta=-1$. Therefore,

$$
\boxed{
r_p=\frac{p}{1+e}
},
\qquad
\boxed{
r_a=\frac{p}{1-e}
}.
$$

For an orbit around the Sun, these points are called perihelion and aphelion,
respectively. Using $p=a(1-e^2)$ makes their relation to the semi-major axis
explicit:

$$
\boxed{
r_p=a(1-e)
},
\qquad
\boxed{
r_a=a(1+e)
}.
$$

Adding these two radii gives

$$
\boxed{
a=\frac{r_p+r_a}{2}
}.
$$
