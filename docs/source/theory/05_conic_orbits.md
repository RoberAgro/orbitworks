# From Newton's equation to conic sections

Eliminating time from the radial equation turns the dynamical problem into an
equation for the orbit's shape. Its solutions are the familiar conic sections:
circles, ellipses, parabolas, and hyperbolas.

## Reduction of the orbital equation using $u=1/r$

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

## Solution of the orbital differential equation

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

## Classification by eccentricity

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

## Conversion from polar conic form to Cartesian ellipse form

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

## Periapsis and apoapsis

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

