# Energy, the effective potential, and vis-viva

The specific mechanical energy $\varepsilon=v^2/2-GM/r$ is a third conserved
quantity of the two-body problem, alongside the angular momentum
$\boldsymbol\ell$ and the eccentricity vector $\mathbf e$. This chapter
derives what $\varepsilon$ determines: the orbit's size, through the
semi-major axis $a$; how speed trades off against distance, through the
vis-viva equation; and a second, algebraic route to the eccentricity,
independent of the vector construction, that must agree with it.

## Mechanical energy and the effective potential

The specific mechanical energy is

$$
\varepsilon
=
\frac{v^2}{2}
-
\frac{GM}{r}.
$$

In polar coordinates, $v^2=\dot r^2+r^2\dot\theta^2$, so

$$
\varepsilon
=
\frac{1}{2}\dot r^2
+
\frac{1}{2}r^2\dot\theta^2
-
\frac{GM}{r}.
$$

Using $\ell=r^2\dot\theta$ (chapter 4), $r^2\dot\theta^2=\ell^2/r^2$, so

$$
\boxed{
\varepsilon
=
\frac{1}{2}\dot r^2
+
\frac{\ell^2}{2r^2}
-
\frac{GM}{r}
}.
$$

Define the effective potential

$$
\boxed{
V_{\mathrm{eff}}(r)
=
\frac{\ell^2}{2r^2}
-
\frac{GM}{r}
},
\qquad
\varepsilon
=
\frac{1}{2}\dot r^2
+
V_{\mathrm{eff}}(r).
$$

This converts the radial motion into an equivalent one-dimensional problem: a
particle moving in $r$ under the potential $V_{\mathrm{eff}}$, with $\dot
r^2/2$ playing the role of kinetic energy. The first term of
$V_{\mathrm{eff}}$, $\ell^2/2r^2$, is the angular-momentum barrier that
prevents the body from reaching $r=0$ whenever $\ell\ne0$; the second,
$-GM/r$, is the ordinary gravitational potential.

## Circular orbits are the minimum of the effective potential

A circular orbit has $\dot r=0$ and $\ddot r=0$ at all times, so it occurs at
a stationary point of $V_{\mathrm{eff}}$:

$$
\frac{dV_{\mathrm{eff}}}{dr}
=
-\frac{\ell^2}{r^3}+\frac{GM}{r^2}
=0
\quad\Longrightarrow\quad
\boxed{
\ell^2=GMr
}.
$$

Since $\ell=rv$ for circular motion, this reproduces $v_c=\sqrt{GM/r}$
directly from the effective-potential picture. Differentiating once more,

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{3\ell^2}{r^4}-\frac{2GM}{r^3},
$$

and substituting $\ell^2=GMr$ at the circular radius gives

$$
\frac{d^2V_{\mathrm{eff}}}{dr^2}
=
\frac{GM}{r^3}
>0.
$$

The effective potential has a minimum there, so a circular orbit is a stable
equilibrium of the radial motion: a small radial perturbation oscillates
around $r_c$ rather than growing. This stability is a feature of the
inverse-square law specifically, not of central forces in general.

## From energy to the semi-major axis

At periapsis, $\dot r=0$, so the velocity is purely tangential:
$v_p=\ell/r_p$ (from $\ell=r_pv_p$). Substituting into the energy expression,

$$
\varepsilon=\frac{v_p^2}{2}-\frac{GM}{r_p}=\frac{\ell^2}{2r_p^2}-\frac{GM}{r_p}.
$$

With $r_p=a(1-e)$ and $p=\ell^2/GM=a(1-e^2)$ (chapter 5), so that
$\ell^2=GMa(1-e^2)$, substituting both gives

$$
\varepsilon
=
\frac{GMa(1-e^2)}{2a^2(1-e)^2}-\frac{GM}{a(1-e)}
=
\frac{GM(1+e)}{2a(1-e)}-\frac{GM}{a(1-e)}.
$$

Combining the two terms over $2a(1-e)$, the numerator is $GM(1+e)-2GM=-GM(1-e)$,
so the factor $(1-e)$ cancels:

$$
\boxed{
\varepsilon=-\frac{GM}{2a}.
}
$$

The energy depends only on the semi-major axis: two orbits sharing the same
$a$ have the same energy regardless of eccentricity. This relation also
*defines* $a$ for a hyperbola (where it comes out negative) and marks the
parabolic limit, $a\to\infty$, $\varepsilon\to0^-$.

## The vis-viva equation

Substituting $\varepsilon=-GM/2a$ into the general energy expression
$\varepsilon=v^2/2-GM/r$ and solving for $v^2$,

$$
\boxed{
v^2=GM\left(\frac{2}{r}-\frac{1}{a}\right).
}
$$

This is the **vis-viva equation**: it gives the speed at any radius on a
Keplerian orbit of semi-major axis $a$, without needing to know $\theta$ or
$e$ separately. It applies everywhere along the orbit, at periapsis,
apoapsis, or in between.

**Why speed changes along an elliptical orbit.** Since $\varepsilon$ is
constant, $-GM/r$ becoming more negative as $r$ shrinks forces $v^2/2$ to
grow: the body speeds up approaching periapsis and slows approaching
apoapsis. This is consistent with $\ell=r^2\dot\theta$: as $r$ decreases,
$\dot\theta$ must increase to keep $\ell$ fixed.

## A second route to the eccentricity

The eccentricity can also be reached algebraically, from energy and angular
momentum alone, independent of the vector construction of the previous
chapter. From $\varepsilon=-GM/2a$,

$$
\frac{1}{a}=-\frac{2\varepsilon}{GM}.
$$

Since $p=\ell^2/GM=a(1-e^2)$ (chapter 5), $e^2=1-\ell^2/(GMa)$. Substituting
$1/a$,

$$
\boxed{
e^2=1+\frac{2\varepsilon\ell^2}{(GM)^2}.
}
$$

This must agree with $e=|\mathbf e|$ from the eccentricity vector for the
same initial state: two derivations, one starting from a conserved vector
and one from conserved scalars, meet at the same value. The classification
by energy sign follows immediately:

$$
\boxed{
\begin{array}{ccl}
\varepsilon<0 &\Rightarrow& 0\le e<1 \quad\text{bound (circle or ellipse)}\\[4pt]
\varepsilon=0 &\Rightarrow& e=1 \quad\text{parabolic escape}\\[4pt]
\varepsilon>0 &\Rightarrow& e>1 \quad\text{hyperbolic escape}
\end{array}
}
$$

matching the eccentricity ranges from the classification by shape (chapter 5).

## Comparing orbital speed to circular speed

The circular speed at radius $r$,

$$
v_c(r)=\sqrt{\frac{GM}{r}},
$$

depends only on $r$, not on the eccentricity of whatever orbit passes through
that radius. The vis-viva equation shows how an actual orbit's speed compares
to it: $v>v_c(r)$ whenever $a>r$, and $v<v_c(r)$ whenever $a<r$. The ratio
$v/v_c$ at one point therefore already carries information about the orbit's
energy relative to a circular orbit at that radius.

This becomes an explicit formula for $e$ in the special case of a **tangential
launch at periapsis** ($r=r_p$, $\dot r=0$). Since $\ell=r_pv$ there, and
$p=\ell^2/GM$, substituting into $r_p=p/(1+e)$ and using $v_c^2=GM/r_p$ gives,
after cancelling $r_p$,

$$
\boxed{
e=\frac{v^2}{v_c^2}-1.
}
$$

Checking the limits: $v=v_c$ gives $e=0$ (circular); $v=v_{\mathrm{esc}}
=\sqrt2\,v_c$ gives $e=1$ (parabolic, since $v^2/v_c^2=2$); speeds in between
give $0<e<1$ (elliptical); speeds above escape give $e>1$ (hyperbolic),
consistent with the energy-sign classification above.

This tangential case is special: knowing the radius and speed at a single
point fixes $e$ only because the launch direction (purely tangential) was
also specified. In general, a position and a *speed* alone are not enough to
fix an orbit: the full velocity *vector* is needed, which is exactly the
extra information a launch angle (or, equivalently, the split between $\dot
r$ and $r\dot\theta$) supplies.
