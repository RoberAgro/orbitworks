# Newtonian gravity, planetary orbits, and Kepler's laws

## 1. Overview

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

## 2. Gravitational acceleration

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

## 3. Why an orbiting body does not simply fall into the central body

An orbiting body is in fact falling continuously toward the central body.

The difference between an impact trajectory and an orbit is that the body also has tangential velocity.

If a projectile is launched horizontally, gravity bends its path downward. As the launch speed increases, the projectile travels farther before intersecting the surface.

At a sufficiently high tangential velocity, the curvature of the projectile's trajectory can exactly match the curvature of the spherical body beneath it. The projectile then continues to fall without ever reaching the surface.

That is the geometric essence of a circular orbit.

There is no additional outward force balancing gravity in an inertial frame. Gravity itself is the force that continuously bends the inertial trajectory into a curved path.

---

## 4. Simple projectile derivation of circular orbital speed

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

## 5. Differential form of the projectile-curvature argument

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

## 6. Systematic derivation of centripetal acceleration

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

## 7. Curvature form of normal acceleration

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

## 8. Circular orbit from Newtonian gravity

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

## 9. Why closer planets have shorter years

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

## 10. Why circular orbits do not spiral inward

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

---

## 11. What happens when the tangential speed differs from circular speed

At a given radius $r$,

$$
v_c=\sqrt{\frac{\mu}{r}}.
$$

If the object has exactly this tangential speed, the orbit is circular.

If the tangential speed is larger, gravity is not strong enough to bend the path with curvature $1/r$ at that instant.

The actual curvature is

$$
\kappa
=
\frac{g}{v^2}
=
\frac{\mu/r^2}{v^2}.
$$

For circular motion,

$$
\kappa_c=\frac{1}{r}.
$$

If

$$
v>v_c,
$$

then

$$
\frac{\mu}{r^2v^2}
<
\frac{1}{r},
$$

so

$$
\boxed{
\kappa<\frac{1}{r}
}
$$

The trajectory bends less sharply than the local circular path and therefore initially moves outward.

Whether it remains bound depends on its total mechanical energy.

---

## 12. Escape velocity

The specific mechanical energy is

$$
\boxed{
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}
}
$$

where $\varepsilon$ is energy per unit mass.

At the threshold of escape, the body reaches infinity with zero remaining speed.

At infinity,

$$
\frac{\mu}{r}\rightarrow 0
$$

and

$$
v\rightarrow 0.
$$

Therefore the threshold energy is

$$
\varepsilon=0.
$$

Set

$$
\frac{v_{\mathrm{esc}}^2}{2}
-
\frac{\mu}{r}
=
0.
$$

Then

$$
\frac{v_{\mathrm{esc}}^2}{2}
=
\frac{\mu}{r}.
$$

Hence,

$$
\boxed{
v_{\mathrm{esc}}
=
\sqrt{\frac{2\mu}{r}}
}
$$

Since

$$
v_c=\sqrt{\frac{\mu}{r}},
$$

we obtain

$$
\boxed{
v_{\mathrm{esc}}
=
\sqrt{2}\,v_c
}
$$

For Earth near the surface,

$$
v_c\approx 7.9\ \mathrm{km/s},
$$

whereas

$$
v_{\mathrm{esc}}\approx 11.2\ \mathrm{km/s}.
$$

---

## 13. Basic classification by speed and energy

For a purely tangential launch at radius $r$:

$$
v=v_c
$$

gives a circular orbit.

If

$$
v_c<v<v_{\mathrm{esc}},
$$

the object initially moves outward but remains gravitationally bound. Its orbit is an ellipse.

If

$$
v=v_{\mathrm{esc}},
$$

the orbit is parabolic.

If

$$
v>v_{\mathrm{esc}},
$$

the trajectory is hyperbolic.

For tangential launch below circular speed,

$$
v<v_c,
$$

the object initially curves inward more sharply than the local circle. In an ideal point-mass problem this is also an elliptical orbit, but if the launch occurs from a planetary surface, the ellipse may intersect the body.

The exact classification becomes especially clear once the general conic solution is derived.

---

## 14. Equations of motion in polar coordinates

The full orbital problem is most naturally written in plane polar coordinates $(r,\theta)$.

The acceleration vector is

$$
\boxed{
\mathbf a
=
\left(
\ddot r-r\dot\theta^2
\right)\mathbf e_r
+
\left(
r\ddot\theta+2\dot r\dot\theta
\right)\mathbf e_\theta
}
$$

Gravity is purely radial:

$$
\mathbf a
=
-\frac{\mu}{r^2}\mathbf e_r.
$$

Therefore the radial and tangential equations are

$$
\boxed{
\ddot r-r\dot\theta^2
=
-\frac{\mu}{r^2}
}
$$

and

$$
\boxed{
r\ddot\theta+2\dot r\dot\theta=0
}
$$

These two equations contain the complete two-dimensional Newtonian orbital dynamics.

---

## 15. Angular momentum conservation

Start from the tangential equation:

$$
r\ddot\theta+2\dot r\dot\theta=0.
$$

Multiply by $r$:

$$
r^2\ddot\theta
+
2r\dot r\dot\theta
=
0.
$$

Recognize that

$$
\frac{d}{dt}
\left(
r^2\dot\theta
\right)
=
2r\dot r\dot\theta
+
r^2\ddot\theta.
$$

Therefore,

$$
\frac{d}{dt}
\left(
r^2\dot\theta
\right)
=
0.
$$

Hence,

$$
\boxed{
r^2\dot\theta=h
}
$$

where $h$ is a constant.

This is the specific angular momentum.

The ordinary angular momentum magnitude is

$$
L=mh.
$$

For planar motion,

$$
\boxed{
h=r^2\dot\theta
}
$$

is one of the central invariants of the orbital problem.

---

## 16. Kepler's second law from angular momentum conservation

The area swept by the radius vector in a small time $dt$ is approximately the area of a thin triangle:

$$
dA
=
\frac{1}{2}r^2\,d\theta.
$$

Divide by $dt$:

$$
\frac{dA}{dt}
=
\frac{1}{2}r^2\dot\theta.
$$

Using

$$
r^2\dot\theta=h,
$$

we obtain

$$
\boxed{
\frac{dA}{dt}
=
\frac{h}{2}
=
\mathrm{constant}
}
$$

Therefore equal areas are swept in equal times.

This is exactly Kepler's second law.

The result follows directly from the fact that gravity is a central force.

A central force produces zero torque:

$$
\boldsymbol\tau
=
\mathbf r\times\mathbf F
=
0.
$$

Zero torque implies angular momentum conservation, and angular momentum conservation implies constant areal velocity.

Thus,

$$
\boxed{
\text{central force}
\Rightarrow
\text{zero torque}
\Rightarrow
\text{constant angular momentum}
\Rightarrow
\text{equal areas in equal times}
}
$$

---

## 17. Reduction of the orbital equation using $u=1/r$

Return to the radial equation:

$$
\ddot r-r\dot\theta^2
=
-\frac{\mu}{r^2}.
$$

We want an equation directly for the shape of the trajectory $r(\theta)$, eliminating time.

Define

$$
\boxed{
u(\theta)=\frac{1}{r}
}
$$

so

$$
r=\frac{1}{u}.
$$

Angular momentum conservation gives

$$
r^2\dot\theta=h.
$$

Since

$$
r=\frac{1}{u},
$$

we have

$$
r^2=\frac{1}{u^2}.
$$

Hence,

$$
\frac{1}{u^2}\dot\theta=h,
$$

so

$$
\boxed{
\dot\theta=hu^2
}
$$

Now calculate $\dot r$.

Because

$$
r=\frac{1}{u},
$$

$$
\frac{dr}{d\theta}
=
-\frac{1}{u^2}\frac{du}{d\theta}.
$$

Write

$$
u'=\frac{du}{d\theta}.
$$

Then

$$
\frac{dr}{d\theta}
=
-\frac{u'}{u^2}.
$$

Using

$$
\dot r
=
\frac{dr}{d\theta}\dot\theta,
$$

we get

$$
\dot r
=
-\frac{u'}{u^2}(hu^2).
$$

Therefore,

$$
\boxed{
\dot r=-hu'
}
$$

Differentiate with respect to time:

$$
\ddot r
=
-h\frac{du'}{dt}.
$$

By the chain rule,

$$
\frac{du'}{dt}
=
\frac{du'}{d\theta}\dot\theta
=
u''\dot\theta.
$$

Since

$$
\dot\theta=hu^2,
$$

we obtain

$$
\boxed{
\ddot r
=
-h^2u^2u''
}
$$

Now evaluate the term $r\dot\theta^2$:

$$
r\dot\theta^2
=
\frac{1}{u}(hu^2)^2.
$$

Therefore,

$$
\boxed{
r\dot\theta^2
=
h^2u^3
}
$$

Substitute these results into the radial equation:

$$
-h^2u^2u''
-
h^2u^3
=
-\mu u^2.
$$

Factor the left-hand side:

$$
-h^2u^2(u''+u)
=
-\mu u^2.
$$

Assuming $u\neq 0$, divide by $-u^2$:

$$
h^2(u''+u)=\mu.
$$

Hence,

$$
\boxed{
u''+u
=
\frac{\mu}{h^2}
}
$$

This is Binet's equation for inverse-square gravity.

---

## 18. Solution of the orbital differential equation

We must solve

$$
u''+u
=
\frac{\mu}{h^2}.
$$

The homogeneous equation is

$$
u_h''+u_h=0.
$$

Its solution is

$$
u_h
=
A\cos\theta
+
B\sin\theta.
$$

A constant particular solution is

$$
u_p=\frac{\mu}{h^2}.
$$

Therefore,

$$
u
=
\frac{\mu}{h^2}
+
A\cos\theta
+
B\sin\theta.
$$

The trigonometric terms can be combined into one shifted cosine:

$$
A\cos\theta+B\sin\theta
=
C\cos(\theta-\theta_0).
$$

Thus,

$$
u
=
\frac{\mu}{h^2}
+
C\cos(\theta-\theta_0).
$$

Choose the angular origin so that periapsis occurs at

$$
\theta=0.
$$

Then $\theta_0=0$, giving

$$
u
=
\frac{\mu}{h^2}
+
C\cos\theta.
$$

Factor out $\mu/h^2$:

$$
u
=
\frac{\mu}{h^2}
\left[
1+
\frac{Ch^2}{\mu}\cos\theta
\right].
$$

Define the eccentricity

$$
\boxed{
e=\frac{Ch^2}{\mu}
}
$$

and define the semi-latus rectum

$$
\boxed{
p=\frac{h^2}{\mu}
}
$$

Then

$$
u
=
\frac{1}{p}
(1+e\cos\theta).
$$

Since

$$
u=\frac{1}{r},
$$

we obtain

$$
\boxed{
r(\theta)
=
\frac{p}{1+e\cos\theta}
}
$$

This is the polar equation of a conic section with the central mass at one focus.

This single equation contains circular, elliptical, parabolic, and hyperbolic trajectories.

---

## 19. Classification by eccentricity

The orbit

$$
r(\theta)
=
\frac{p}{1+e\cos\theta}
$$

is classified by the eccentricity $e$.

For

$$
\boxed{
e=0
}
$$

the radius is constant:

$$
r=p.
$$

The orbit is a circle.

For

$$
\boxed{
0<e<1
}
$$

the orbit is an ellipse.

For

$$
\boxed{
e=1
}
$$

the orbit is a parabola.

For

$$
\boxed{
e>1
}
$$

the orbit is a hyperbola.

Thus the inverse-square gravitational law naturally generates the family of conic sections.

---

## 20. Conversion from polar conic form to Cartesian ellipse form

For an elliptical orbit,

$$
0<e<1.
$$

Begin with

$$
r
=
\frac{p}{1+e\cos\theta}.
$$

Use

$$
x=r\cos\theta,
\qquad
y=r\sin\theta,
\qquad
r=\sqrt{x^2+y^2}.
$$

From

$$
r(1+e\cos\theta)=p,
$$

and

$$
r\cos\theta=x,
$$

we obtain

$$
r+ex=p.
$$

Thus,

$$
r=p-ex.
$$

Square both sides:

$$
x^2+y^2
=
(p-ex)^2.
$$

Expand:

$$
x^2+y^2
=
p^2-2epx+e^2x^2.
$$

Rearrange:

$$
(1-e^2)x^2
+
2epx
+
y^2
-
p^2
=
0.
$$

Complete the square in $x$.

Factor $1-e^2$:

$$
(1-e^2)
\left[
x^2
+
\frac{2ep}{1-e^2}x
\right]
+
y^2
-
p^2
=
0.
$$

Inside the brackets,

$$
x^2
+
\frac{2ep}{1-e^2}x
=
\left(
x+\frac{ep}{1-e^2}
\right)^2
-
\left(
\frac{ep}{1-e^2}
\right)^2.
$$

Substitute:

$$
(1-e^2)
\left(
x+\frac{ep}{1-e^2}
\right)^2
-
(1-e^2)
\left(
\frac{ep}{1-e^2}
\right)^2
+
y^2
-p^2
=
0.
$$

The constant term becomes

$$
-\frac{e^2p^2}{1-e^2}-p^2
=
-\frac{p^2}{1-e^2}.
$$

Hence,

$$
(1-e^2)
\left(
x+\frac{ep}{1-e^2}
\right)^2
+
y^2
=
\frac{p^2}{1-e^2}.
$$

Divide through by $p^2/(1-e^2)$:

$$
\frac{
\left(
x+\frac{ep}{1-e^2}
\right)^2
}{
\frac{p^2}{(1-e^2)^2}
}
+
\frac{
y^2
}{
\frac{p^2}{1-e^2}
}
=
1.
$$

Define

$$
\boxed{
a=\frac{p}{1-e^2}
}
$$

and

$$
\boxed{
b=\frac{p}{\sqrt{1-e^2}}
}
$$

Then

$$
b^2=a^2(1-e^2),
$$

so

$$
\boxed{
b=a\sqrt{1-e^2}
}
$$

and

$$
\boxed{
p=a(1-e^2)
}
$$

The Cartesian equation becomes

$$
\boxed{
\frac{(x+ae)^2}{a^2}
+
\frac{y^2}{b^2}
=
1
}
$$

The center of the ellipse is displaced from the focus by the distance

$$
\boxed{
c=ae
}
$$

The central mass lies at one focus, not at the geometrical center of the ellipse.

This is Kepler's first law.

---

## 21. Periapsis and apoapsis

For

$$
r(\theta)
=
\frac{p}{1+e\cos\theta},
$$

the minimum radius occurs at

$$
\theta=0,
$$

where

$$
\cos\theta=1.
$$

Thus,

$$
\boxed{
r_p=\frac{p}{1+e}
}
$$

This is the periapsis radius.

For an orbit around the Sun, this is called perihelion.

The maximum radius occurs at

$$
\theta=\pi,
$$

where

$$
\cos\theta=-1.
$$

Therefore,

$$
\boxed{
r_a=\frac{p}{1-e}
}
$$

This is the apoapsis radius.

For an orbit around the Sun, this is called aphelion.

Using

$$
p=a(1-e^2),
$$

we get

$$
r_p
=
\frac{a(1-e^2)}{1+e}
=
a(1-e),
$$

so

$$
\boxed{
r_p=a(1-e)
}
$$

Similarly,

$$
r_a
=
\frac{a(1-e^2)}{1-e}
=
a(1+e),
$$

so

$$
\boxed{
r_a=a(1+e)
}
$$

Therefore,

$$
\boxed{
a=\frac{r_p+r_a}{2}
}
$$

---

## 22. Mechanical energy and the effective potential

The specific mechanical energy is

$$
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}.
$$

In polar coordinates,

$$
v^2
=
\dot r^2
+
r^2\dot\theta^2.
$$

Thus,

$$
\varepsilon
=
\frac{1}{2}\dot r^2
+
\frac{1}{2}r^2\dot\theta^2
-
\frac{\mu}{r}.
$$

Using

$$
h=r^2\dot\theta,
$$

we have

$$
\dot\theta=\frac{h}{r^2}.
$$

Therefore,

$$
r^2\dot\theta^2
=
\frac{h^2}{r^2}.
$$

Hence,

$$
\boxed{
\varepsilon
=
\frac{1}{2}\dot r^2
+
\frac{h^2}{2r^2}
-
\frac{\mu}{r}
}
$$

Define the effective potential

$$
\boxed{
V_{\mathrm{eff}}(r)
=
\frac{h^2}{2r^2}
-
\frac{\mu}{r}
}
$$

Then,

$$
\boxed{
\varepsilon
=
\frac{1}{2}\dot r^2
+
V_{\mathrm{eff}}(r)
}
$$

This converts the radial part of the orbital problem into a one-dimensional energy problem.

The first term in the effective potential,

$$
\frac{h^2}{2r^2},
$$

acts as an angular-momentum barrier at small $r$.

The second term,

$$
-\frac{\mu}{r},
$$

is the gravitational potential.

---

## 23. Circular orbit as a minimum of the effective potential

A circular orbit has constant radius, so

$$
\dot r=0
$$

and

$$
\ddot r=0.
$$

It occurs at a stationary point of the effective potential:

$$
\frac{dV_{\mathrm{eff}}}{dr}=0.
$$

Differentiate:

$$
\frac{dV_{\mathrm{eff}}}{dr}
=
-\frac{h^2}{r^3}
+
\frac{\mu}{r^2}.
$$

Set equal to zero:

$$
-\frac{h^2}{r^3}
+
\frac{\mu}{r^2}
=
0.
$$

Multiply by $r^3$:

$$
-h^2+\mu r=0.
$$

Hence,

$$
\boxed{
h^2=\mu r
}
$$

For a circular orbit,

$$
h=rv.
$$

Therefore,

$$
r^2v^2=\mu r.
$$

Cancel $r$:

$$
v^2=\frac{\mu}{r}.
$$

Thus,

$$
\boxed{
v_c=\sqrt{\frac{\mu}{r}}
}
$$

as before.

To examine stability, calculate the second derivative:

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{3h^2}{r^4}
-
\frac{2\mu}{r^3}.
$$

At the circular orbit,

$$
h^2=\mu r.
$$

Therefore,

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{3\mu r}{r^4}
-
\frac{2\mu}{r^3}
=
\frac{\mu}{r^3}>0.
$$

Thus the circular orbit is a local minimum of the effective potential and is stable in Newtonian gravity.

---

## 24. Derivation of the energy–semi-major-axis relation and the vis-viva equation

For an ellipse, we can derive the energy relation directly from quantities already obtained.

At periapsis,

$$
r=r_p=a(1-e)
$$

and the radial velocity vanishes:

$$
\dot r=0.
$$

Therefore the velocity is purely tangential at that point.

Since

$$
h=rv_\theta,
$$

the periapsis speed is

$$
v_p=\frac{h}{r_p}.
$$

The specific energy at periapsis is therefore

$$
\varepsilon
=
\frac{v_p^2}{2}
-
\frac{\mu}{r_p}.
$$

Substitute

$$
v_p=\frac{h}{r_p}:
$$

$$
\varepsilon
=
\frac{h^2}{2r_p^2}
-
\frac{\mu}{r_p}.
$$

We previously found

$$
p=\frac{h^2}{\mu}
$$

and

$$
p=a(1-e^2).
$$

Therefore,

$$
h^2
=
\mu a(1-e^2).
$$

Also,

$$
r_p=a(1-e).
$$

Substitute both into the energy expression:

$$
\varepsilon
=
\frac{
\mu a(1-e^2)
}{
2a^2(1-e)^2
}
-
\frac{\mu}{a(1-e)}.
$$

Simplify the first term:

$$
\frac{
\mu a(1-e^2)
}{
2a^2(1-e)^2
}
=
\frac{
\mu(1-e^2)
}{
2a(1-e)^2
}.
$$

Because

$$
1-e^2=(1-e)(1+e),
$$

this becomes

$$
\frac{
\mu(1+e)
}{
2a(1-e)
}.
$$

Hence,

$$
\varepsilon
=
\frac{
\mu(1+e)
}{
2a(1-e)
}
-
\frac{\mu}{a(1-e)}.
$$

Put both terms over the common denominator $2a(1-e)$:

$$
\varepsilon
=
\frac{
\mu(1+e)-2\mu
}{
2a(1-e)
}.
$$

The numerator is

$$
\mu(1+e)-2\mu
=
\mu(e-1)
=
-\mu(1-e).
$$

Therefore,

$$
\varepsilon
=
-\frac{
\mu(1-e)
}{
2a(1-e)
}.
$$

Cancel $1-e$:

$$
\boxed{
\varepsilon
=
-\frac{\mu}{2a}
}
$$

Thus the specific orbital energy of an ellipse depends only on its semi-major axis, not on its eccentricity.

This relation can now be combined with the general energy equation

$$
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}.
$$

Substitute

$$
\varepsilon=-\frac{\mu}{2a}:
$$

$$
-\frac{\mu}{2a}
=
\frac{v^2}{2}
-
\frac{\mu}{r}.
$$

Move the potential term to the other side:

$$
\frac{v^2}{2}
=
\frac{\mu}{r}
-
\frac{\mu}{2a}.
$$

Multiply by $2$:

$$
v^2
=
\frac{2\mu}{r}
-
\frac{\mu}{a}.
$$

Factor out $\mu$:

$$
\boxed{
v^2
=
\mu
\left(
\frac{2}{r}
-
\frac{1}{a}
\right)
}
$$

This is the vis-viva equation.

It applies everywhere along a Keplerian ellipse.

As

$$
a\rightarrow\infty,
$$

the bound-orbit energy approaches

$$
\varepsilon\rightarrow0^{-},
$$

which is the parabolic escape threshold.

---

## 25. Derivation of eccentricity in terms of energy and angular momentum

We can derive the relation between eccentricity, energy, and angular momentum without introducing any new orbital law.

Start from

$$
p=a(1-e^2)
$$

and

$$
p=\frac{h^2}{\mu}.
$$

Therefore,

$$
\frac{h^2}{\mu}
=
a(1-e^2).
$$

Divide by $a$:

$$
\frac{h^2}{\mu a}
=
1-e^2.
$$

Rearrange:

$$
e^2
=
1-\frac{h^2}{\mu a}.
$$

From the energy relation,

$$
\varepsilon
=
-\frac{\mu}{2a}.
$$

Solve this for $1/a$:

$$
\frac{1}{a}
=
-\frac{2\varepsilon}{\mu}.
$$

Substitute into the eccentricity expression:

$$
e^2
=
1
-
\frac{h^2}{\mu}
\left(
-\frac{2\varepsilon}{\mu}
\right).
$$

Therefore,

$$
\boxed{
e^2
=
1+
\frac{2\varepsilon h^2}{\mu^2}
}
$$

This equation connects the geometry of the conic directly to its mechanical invariants.

The classification now follows immediately.

If

$$
\varepsilon<0,
$$

then

$$
e^2<1.
$$

For a nondegenerate orbit,

$$
0\le e<1,
$$

so the orbit is a circle or ellipse.

If

$$
\varepsilon=0,
$$

then

$$
e=1,
$$

so the orbit is parabolic.

If

$$
\varepsilon>0,
$$

then

$$
e>1,
$$

so the orbit is hyperbolic.

Thus,

$$
\boxed{
\begin{array}{ccl}
\varepsilon<0 &\Rightarrow& 0\le e<1 \quad \text{bound orbit}\\[4pt]
\varepsilon=0 &\Rightarrow& e=1 \quad \text{parabolic escape}\\[4pt]
\varepsilon>0 &\Rightarrow& e>1 \quad \text{hyperbolic escape}
\end{array}
}
$$

The circular orbit is the special bound case

$$
e=0.
$$

## 26. Tangential launch above circular speed and below escape speed

Suppose an object is launched tangentially at radius $r_p$, with speed satisfying

$$
v_c<v<v_{\mathrm{esc}}.
$$

Because the radial velocity is initially zero,

$$
\dot r=0.
$$

Since the speed exceeds circular velocity, the trajectory initially bends less sharply than the local circle, so the object moves outward after launch.

The launch point is therefore the periapsis.

At periapsis,

$$
\theta=0.
$$

The orbit equation gives

$$
r_p
=
\frac{p}{1+e}.
$$

Since

$$
p=\frac{h^2}{\mu},
$$

and for tangential launch,

$$
h=r_pv,
$$

we have

$$
p
=
\frac{r_p^2v^2}{\mu}.
$$

Therefore,

$$
r_p
=
\frac{r_p^2v^2/\mu}{1+e}.
$$

Multiply by $1+e$:

$$
r_p(1+e)
=
\frac{r_p^2v^2}{\mu}.
$$

Cancel $r_p$:

$$
1+e
=
\frac{r_pv^2}{\mu}.
$$

The circular velocity at $r_p$ satisfies

$$
v_c^2=\frac{\mu}{r_p}.
$$

Therefore,

$$
\frac{r_p}{\mu}
=
\frac{1}{v_c^2}.
$$

Hence,

$$
1+e
=
\frac{v^2}{v_c^2}.
$$

Thus,

$$
\boxed{
e
=
\frac{v^2}{v_c^2}
-
1
}
$$

This result immediately gives the orbital classification.

If

$$
v=v_c,
$$

then

$$
e=0,
$$

so the orbit is circular.

If

$$
v_c<v<v_{\mathrm{esc}},
$$

then

$$
1<
\frac{v^2}{v_c^2}
<
2,
$$

because

$$
v_{\mathrm{esc}}^2=2v_c^2.
$$

Therefore,

$$
0<e<1,
$$

which proves that the orbit is elliptical.

If

$$
v=v_{\mathrm{esc}},
$$

then

$$
e
=
\frac{2v_c^2}{v_c^2}-1
=
1,
$$

so the orbit is parabolic.

If

$$
v>v_{\mathrm{esc}},
$$

then

$$
e>1,
$$

so the orbit is hyperbolic.

---

## 27. Why the speed changes along an elliptical orbit

For an elliptical orbit, the total specific energy is constant:

$$
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}.
$$

As the planet moves closer to the central body, $r$ decreases and

$$
-\frac{\mu}{r}
$$

becomes more negative.

To keep $\varepsilon$ constant, the kinetic term must increase.

Therefore $v$ increases as $r$ decreases.

Conversely, the object slows as it moves outward.

The vis-viva equation makes this explicit:

$$
\boxed{
v^2
=
\mu
\left(
\frac{2}{r}
-
\frac{1}{a}
\right)
}
$$

At periapsis, $r$ is smallest, so $v$ is largest.

At apoapsis, $r$ is largest, so $v$ is smallest.

This behavior is also consistent with angular momentum conservation:

$$
h=r^2\dot\theta.
$$

The angular speed must increase when the radius decreases.

---

## 28. Kepler's first law from Newton's law

Newtonian gravity gives the orbital differential equation

$$
u''+u
=
\frac{\mu}{h^2}.
$$

Its solution is

$$
r(\theta)
=
\frac{p}{1+e\cos\theta}.
$$

This is the equation of a conic section with the attracting body at a focus.

For bound planetary motion,

$$
\varepsilon<0,
$$

which implies

$$
0\le e<1.
$$

Therefore the orbit is an ellipse, with the circular orbit as the special case $e=0$.

Hence Newtonian gravitation yields Kepler's first law:

$$
\boxed{
\text{bound planets move in ellipses with the Sun at one focus}
}
$$

---

## 29. Kepler's second law from Newton's law

Because gravity is central,

$$
\mathbf F\parallel\mathbf r.
$$

Therefore,

$$
\boldsymbol\tau
=
\mathbf r\times\mathbf F
=
0.
$$

Hence angular momentum is constant:

$$
h=r^2\dot\theta.
$$

The areal velocity is

$$
\frac{dA}{dt}
=
\frac{1}{2}r^2\dot\theta.
$$

Therefore,

$$
\boxed{
\frac{dA}{dt}
=
\frac{h}{2}
=
\mathrm{constant}
}
$$

Thus equal areas are swept in equal times.

This is Kepler's second law.

---

## 30. Kepler's third law for an ellipse

For an ellipse with semi-major axis $a$ and semi-minor axis $b$, the total area is

$$
A=\pi ab.
$$

From Kepler's second law,

$$
\frac{dA}{dt}
=
\frac{h}{2}.
$$

Over one complete orbital period $T$, the entire ellipse is swept out.

Thus,

$$
\pi ab
=
\frac{h}{2}T.
$$

Therefore,

$$
T
=
\frac{2\pi ab}{h}.
$$

For an ellipse,

$$
b=a\sqrt{1-e^2}.
$$

Thus,

$$
T
=
\frac{
2\pi a^2\sqrt{1-e^2}
}{h}.
$$

We also have

$$
p=\frac{h^2}{\mu}
$$

and

$$
p=a(1-e^2).
$$

Therefore,

$$
\frac{h^2}{\mu}
=
a(1-e^2).
$$

Hence,

$$
h^2
=
\mu a(1-e^2).
$$

Taking the positive root,

$$
h
=
\sqrt{
\mu a(1-e^2)
}.
$$

Substitute into the period expression:

$$
T
=
\frac{
2\pi a^2\sqrt{1-e^2}
}{
\sqrt{
\mu a(1-e^2)
}
}.
$$

Cancel $\sqrt{1-e^2}$:

$$
T
=
\frac{
2\pi a^2
}{
\sqrt{\mu a}
}.
$$

Since

$$
\sqrt{\mu a}
=
\sqrt{\mu}\sqrt{a},
$$

we obtain

$$
T
=
2\pi
\frac{a^{3/2}}{\sqrt{\mu}}.
$$

Therefore,

$$
\boxed{
T
=
2\pi\sqrt{\frac{a^3}{\mu}}
}
$$

and hence

$$
\boxed{
T^2
=
\frac{4\pi^2}{\mu}a^3
}
$$

Since

$$
\mu=GM,
$$

$$
\boxed{
T^2
=
\frac{4\pi^2}{GM}a^3
}
$$

This is Kepler's third law in its general elliptical form.

A notable feature is that the eccentricity cancels completely.

The orbital period depends only on the semi-major axis $a$, not directly on the eccentricity.

---

## 31. Why the mathematics is so compact

The structure of the problem can be summarized as a chain of consequences:

$$
\boxed{
\text{inverse-square gravity}
\rightarrow
\text{central force}
\rightarrow
\text{angular momentum conservation}
}
$$

Angular momentum conservation gives

$$
\boxed{
\text{constant areal velocity}
}
$$

which is Kepler's second law.

The inverse-square form also makes the substitution

$$
u=\frac{1}{r}
$$

especially powerful, reducing the radial equation to

$$
\boxed{
u''+u=\mathrm{constant}
}
$$

whose solution is

$$
\boxed{
r=\frac{p}{1+e\cos\theta}
}
$$

the equation of a conic section.

For negative energy, the conic is an ellipse, giving Kepler's first law.

Finally, combining the ellipse geometry with constant areal velocity gives

$$
\boxed{
T^2\propto a^3
}
$$

which is Kepler's third law.

Thus the three empirical Kepler laws are not independent statements within Newtonian mechanics. They are consequences of a single force law together with Newton's laws of motion.

---

## 32. Summary of central results

Newtonian gravity:

$$
\boxed{
\mathbf F
=
-\frac{GMm}{r^2}\mathbf e_r
}
$$

Gravitational acceleration:

$$
\boxed{
\mathbf a
=
-\frac{GM}{r^2}\mathbf e_r
}
$$

Circular orbital speed:

$$
\boxed{
v_c
=
\sqrt{\frac{GM}{r}}
}
$$

Escape speed:

$$
\boxed{
v_{\mathrm{esc}}
=
\sqrt{\frac{2GM}{r}}
=
\sqrt{2}\,v_c
}
$$

Centripetal acceleration:

$$
\boxed{
a_c
=
\frac{v^2}{r}
}
$$

Curvature form:

$$
\boxed{
a_n=v^2\kappa
}
$$

Specific angular momentum:

$$
\boxed{
h=r^2\dot\theta
}
$$

Areal velocity:

$$
\boxed{
\frac{dA}{dt}
=
\frac{h}{2}
}
$$

Specific energy:

$$
\boxed{
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}
}
$$

Effective potential:

$$
\boxed{
V_{\mathrm{eff}}(r)
=
\frac{h^2}{2r^2}
-
\frac{\mu}{r}
}
$$

Binet equation for Newtonian gravity:

$$
\boxed{
u''+u
=
\frac{\mu}{h^2}
}
$$

Conic orbit equation:

$$
\boxed{
r(\theta)
=
\frac{p}{1+e\cos\theta}
}
$$

Semi-latus rectum:

$$
\boxed{
p
=
\frac{h^2}{\mu}
=
a(1-e^2)
}
$$

Periapsis and apoapsis:

$$
\boxed{
r_p=a(1-e)
}
$$

$$
\boxed{
r_a=a(1+e)
}
$$

Vis-viva equation:

$$
\boxed{
v^2
=
\mu
\left(
\frac{2}{r}
-
\frac{1}{a}
\right)
}
$$

Energy of an ellipse:

$$
\boxed{
\varepsilon
=
-\frac{\mu}{2a}
}
$$

Eccentricity-energy relation:

$$
\boxed{
e^2
=
1+\frac{2\varepsilon h^2}{\mu^2}
}
$$

Tangential launch from periapsis:

$$
\boxed{
e
=
\frac{v^2}{v_c^2}-1
}
$$

Kepler's third law:

$$
\boxed{
T^2
=
\frac{4\pi^2}{GM}a^3
}
$$

The orbit classification is

$$
\boxed{
\begin{array}{ccl}
e=0 &:& \text{circle}\\
0<e<1 &:& \text{ellipse}\\
e=1 &:& \text{parabola}\\
e>1 &:& \text{hyperbola}
\end{array}
}
$$

or, equivalently,

$$
\boxed{
\begin{array}{ccl}
\varepsilon<0 &:& \text{bound ellipse}\\
\varepsilon=0 &:& \text{parabolic escape}\\
\varepsilon>0 &:& \text{hyperbolic escape}
\end{array}
}
$$

The complete conceptual chain is therefore

$$
\boxed{
\text{Newtonian gravitation}
\rightarrow
\text{central-force dynamics}
\rightarrow
\text{conservation laws}
\rightarrow
\text{conic trajectories}
\rightarrow
\text{Kepler's laws}
}
$$
