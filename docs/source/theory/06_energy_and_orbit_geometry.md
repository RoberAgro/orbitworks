# Energy and orbital geometry

Energy and angular momentum connect the state of an orbiting body to geometric
quantities such as the semi-major axis and eccentricity. They also explain
circular-orbit stability and the changing speed along an ellipse.

## Mechanical energy and the effective potential

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

## Circular orbit as a minimum of the effective potential

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

## Derivation of the energy–semi-major-axis relation and the vis-viva equation

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

## Derivation of eccentricity in terms of energy and angular momentum

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

## Tangential launch above circular speed and below escape speed

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

## Why the speed changes along an elliptical orbit

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

