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
\frac{GM}{r}.
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
\frac{GM}{r}.
$$

Using

$$
\ell=r^2\dot\theta,
$$

we have

$$
\dot\theta=\frac{\ell}{r^2}.
$$

Therefore,

$$
r^2\dot\theta^2
=
\frac{\ell^2}{r^2}.
$$

Hence,

$$
\boxed{
\varepsilon
=
\frac{1}{2}\dot r^2
+
\frac{\ell^2}{2r^2}
-
\frac{GM}{r}
}
$$

Define the effective potential

$$
\boxed{
V_{\mathrm{eff}}(r)
=
\frac{\ell^2}{2r^2}
-
\frac{GM}{r}
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
\frac{\ell^2}{2r^2},
$$

acts as an angular-momentum barrier at small $r$.

The second term,

$$
-\frac{GM}{r},
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
-\frac{\ell^2}{r^3}
+
\frac{GM}{r^2}.
$$

Set equal to zero:

$$
-\frac{\ell^2}{r^3}
+
\frac{GM}{r^2}
=
0.
$$

Multiply by $r^3$:

$$
-\ell^2+GM r=0.
$$

Hence,

$$
\boxed{
\ell^2=GM r
}
$$

For a circular orbit,

$$
\ell=rv.
$$

Therefore,

$$
r^2v^2=GM r.
$$

Cancel $r$:

$$
v^2=\frac{GM}{r}.
$$

Thus,

$$
\boxed{
v_c=\sqrt{\frac{GM}{r}}
}
$$

as before.

To examine stability, calculate the second derivative:

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{3h^2}{r^4}
-
\frac{2GM}{r^3}.
$$

At the circular orbit,

$$
\ell^2=GM r.
$$

Therefore,

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{3GM r}{r^4}
-
\frac{2GM}{r^3}
=
\frac{GM}{r^3}>0.
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
\ell=rv_\theta,
$$

the periapsis speed is

$$
v_p=\frac{\ell}{r_p}.
$$

The specific energy at periapsis is therefore

$$
\varepsilon
=
\frac{v_p^2}{2}
-
\frac{GM}{r_p}.
$$

Substitute

$$
v_p=\frac{\ell}{r_p}:
$$

$$
\varepsilon
=
\frac{\ell^2}{2r_p^2}
-
\frac{GM}{r_p}.
$$

We previously found

$$
p=\frac{\ell^2}{GM}
$$

and

$$
p=a(1-e^2).
$$

Therefore,

$$
\ell^2
=
GM a(1-e^2).
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
GM a(1-e^2)
}{
2a^2(1-e)^2
}
-
\frac{GM}{a(1-e)}.
$$

Simplify the first term:

$$
\frac{
GM a(1-e^2)
}{
2a^2(1-e)^2
}
=
\frac{
GM(1-e^2)
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
GM(1+e)
}{
2a(1-e)
}.
$$

Hence,

$$
\varepsilon
=
\frac{
GM(1+e)
}{
2a(1-e)
}
-
\frac{GM}{a(1-e)}.
$$

Put both terms over the common denominator $2a(1-e)$:

$$
\varepsilon
=
\frac{
GM(1+e)-2GM
}{
2a(1-e)
}.
$$

The numerator is

$$
GM(1+e)-2GM
=
GM(e-1)
=
-GM(1-e).
$$

Therefore,

$$
\varepsilon
=
-\frac{
GM(1-e)
}{
2a(1-e)
}.
$$

Cancel $1-e$:

$$
\boxed{
\varepsilon
=
-\frac{GM}{2a}
}
$$

Thus the specific orbital energy of an ellipse depends only on its semi-major axis, not on its eccentricity.

This relation can now be combined with the general energy equation

$$
\varepsilon
=
\frac{v^2}{2}
-
\frac{GM}{r}.
$$

Substitute

$$
\varepsilon=-\frac{GM}{2a}:
$$

$$
-\frac{GM}{2a}
=
\frac{v^2}{2}
-
\frac{GM}{r}.
$$

Move the potential term to the other side:

$$
\frac{v^2}{2}
=
\frac{GM}{r}
-
\frac{GM}{2a}.
$$

Multiply by $2$:

$$
v^2
=
\frac{2GM}{r}
-
\frac{GM}{a}.
$$

Factor out $GM$:

$$
\boxed{
v^2
=
GM
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
p=\frac{\ell^2}{GM}.
$$

Therefore,

$$
\frac{\ell^2}{GM}
=
a(1-e^2).
$$

Divide by $a$:

$$
\frac{\ell^2}{GM a}
=
1-e^2.
$$

Rearrange:

$$
e^2
=
1-\frac{\ell^2}{GM a}.
$$

From the energy relation,

$$
\varepsilon
=
-\frac{GM}{2a}.
$$

Solve this for $1/a$:

$$
\frac{1}{a}
=
-\frac{2\varepsilon}{GM}.
$$

Substitute into the eccentricity expression:

$$
e^2
=
1
-
\frac{\ell^2}{GM}
\left(
-\frac{2\varepsilon}{GM}
\right).
$$

Therefore,

$$
\boxed{
e^2
=
1+
\frac{2\varepsilon \ell^2}{(GM)^2}
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
p=\frac{\ell^2}{GM},
$$

and for tangential launch,

$$
\ell=r_pv,
$$

we have

$$
p
=
\frac{r_p^2v^2}{GM}.
$$

Therefore,

$$
r_p
=
\frac{r_p^2v^2/GM}{1+e}.
$$

Multiply by $1+e$:

$$
r_p(1+e)
=
\frac{r_p^2v^2}{GM}.
$$

Cancel $r_p$:

$$
1+e
=
\frac{r_pv^2}{GM}.
$$

The circular velocity at $r_p$ satisfies

$$
v_c^2=\frac{GM}{r_p}.
$$

Therefore,

$$
\frac{r_p}{GM}
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
\frac{GM}{r}.
$$

As the planet moves closer to the central body, $r$ decreases and

$$
-\frac{GM}{r}
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
GM
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
\ell=r^2\dot\theta.
$$

The angular speed must increase when the radius decreases.

