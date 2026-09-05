# Kepler's laws and synthesis

The preceding results now combine into Newtonian derivations of all three of
Kepler's laws. The final sections collect the logical chain and the formulas
that will recur throughout OrbitWorks.

## Kepler's first law from Newton's law

Newtonian gravity gives the orbital differential equation

$$
u''+u
=
\frac{GM}{\ell^2}.
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

## Kepler's second law from Newton's law

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
\ell=r^2\dot\theta.
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
\frac{\ell}{2}
=
\mathrm{constant}
}
$$

Thus equal areas are swept in equal times.

This is Kepler's second law.

---

## Kepler's third law for an ellipse

For an ellipse with semi-major axis $a$ and semi-minor axis $b$, the total area is

$$
A=\pi ab.
$$

From Kepler's second law,

$$
\frac{dA}{dt}
=
\frac{\ell}{2}.
$$

Over one complete orbital period $T$, the entire ellipse is swept out.

Thus,

$$
\pi ab
=
\frac{\ell}{2}T.
$$

Therefore,

$$
T
=
\frac{2\pi ab}{\ell}.
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
}{\ell}.
$$

We also have

$$
p=\frac{\ell^2}{GM}
$$

and

$$
p=a(1-e^2).
$$

Therefore,

$$
\frac{\ell^2}{GM}
=
a(1-e^2).
$$

Hence,

$$
\ell^2
=
GM a(1-e^2).
$$

Taking the positive root,

$$
\ell
=
\sqrt{
GM a(1-e^2)
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
GM a(1-e^2)
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
\sqrt{GM a}
}.
$$

Since

$$
\sqrt{GM a}
=
\sqrt{GM}\sqrt{a},
$$

we obtain

$$
T
=
2\pi
\frac{a^{3/2}}{\sqrt{GM}}.
$$

Therefore,

$$
\boxed{
T
=
2\pi\sqrt{\frac{a^3}{GM}}
}
$$

and hence

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

## Why the mathematics is so compact

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

## Summary of central results

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
\ell=r^2\dot\theta
}
$$

Areal velocity:

$$
\boxed{
\frac{dA}{dt}
=
\frac{\ell}{2}
}
$$

Specific energy:

$$
\boxed{
\varepsilon
=
\frac{v^2}{2}
-
\frac{GM}{r}
}
$$

Effective potential:

$$
\boxed{
V_{\mathrm{eff}}(r)
=
\frac{\ell^2}{2r^2}
-
\frac{GM}{r}
}
$$

Binet equation for Newtonian gravity:

$$
\boxed{
u''+u
=
\frac{GM}{\ell^2}
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
\frac{\ell^2}{GM}
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
GM
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
-\frac{GM}{2a}
}
$$

Eccentricity-energy relation:

$$
\boxed{
e^2
=
1+\frac{2\varepsilon \ell^2}{(GM)^2}
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
