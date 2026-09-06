# Finding the orbit from a position and a velocity vector

An orbit's shape and size come from two constants of integration — $p$ and
$e$ — together with an orientation angle fixed by where periapsis lies. In an
initial value problem, though, these are not what is actually given: what is
specified is a position and a velocity at one instant, $\mathbf r_0$ and
$\mathbf v_0$. This chapter starts from exactly that information and builds
the integration constants — and with them, the whole orbit — directly from
it.

Throughout, $\mathbf r$ and $\mathbf v$ denote the instantaneous position and
velocity vectors, $r=|\mathbf r|$, and $\mathbf e_r=\mathbf r/r$ the radial
unit vector.

## Angular momentum: one vector constant, already known

A central force conserves the specific angular momentum vector (chapter 4),

$$
\boxed{
\boldsymbol\ell=\mathbf r\times\mathbf v,
}
$$

with magnitude $\ell=|\boldsymbol\ell|$. Since $\boldsymbol\ell$ is built
entirely from $\mathbf r$ and $\mathbf v$, it is known the instant an initial
state is given. Combined with $p=\ell^2/GM$ (chapter 5),

$$
\boxed{
p=\frac{\ell^2}{GM}
}
$$

follows immediately. One of the two constants in $r(\theta)=p/(1+e\cos\theta)$
is therefore already in hand. Finding $e$ — and the orbit's orientation —
takes more work, because $e$ does not appear as a vector built from $\mathbf
r$ and $\mathbf v$ directly. The rest of this chapter constructs one.

## The eccentricity vector

Consider the vector

$$
\boxed{
\mathbf e=\frac{\mathbf v\times\boldsymbol\ell}{GM}-\mathbf e_r.
}
$$

Both terms are dimensionless, so $\mathbf e$ is a dimensionless vector built
directly from the instantaneous state. The rest of this section shows that it
is conserved, and that it is exactly the eccentricity vector: its magnitude is
the same $e$ that appears in $r(\theta)=p/(1+e\cos\theta)$, and its direction
points toward periapsis.

### Proving that $\mathbf e$ is conserved

Differentiate $\mathbf v\times\boldsymbol\ell$ with respect to time:

$$
\frac{d}{dt}(\mathbf v\times\boldsymbol\ell)
=
\dot{\mathbf v}\times\boldsymbol\ell
+
\mathbf v\times\dot{\boldsymbol\ell}.
$$

$\boldsymbol\ell$ is conserved, so $\dot{\boldsymbol\ell}=0$ and the second
term vanishes. The equation of motion gives $\dot{\mathbf v}=-GM\mathbf
r/r^3$, so

$$
\dot{\mathbf v}\times\boldsymbol\ell
=
-\frac{GM}{r^3}\left(\mathbf r\times\boldsymbol\ell\right).
$$

Expand $\mathbf r\times\boldsymbol\ell=\mathbf r\times(\mathbf r\times\mathbf
v)$ with the vector triple product $\mathbf a\times(\mathbf b\times\mathbf c)
=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b)$:

$$
\mathbf r\times(\mathbf r\times\mathbf v)
=
\mathbf r(\mathbf r\cdot\mathbf v)-\mathbf v(\mathbf r\cdot\mathbf r)
=
\mathbf r(\mathbf r\cdot\mathbf v)-\mathbf v\,r^2.
$$

Therefore,

$$
\frac{d}{dt}(\mathbf v\times\boldsymbol\ell)
=
-\frac{GM(\mathbf r\cdot\mathbf v)}{r^3}\mathbf r
+
\frac{GM}{r}\mathbf v.
$$

Now compute the same combination from $\mathbf e_r=\mathbf r/r$. Since
$\dot r=(\mathbf r\cdot\mathbf v)/r$,

$$
\frac{d}{dt}\left(\frac{\mathbf r}{r}\right)
=
\frac{\mathbf v}{r}-\frac{\mathbf r\,\dot r}{r^2}
=
\frac{\mathbf v}{r}-\frac{(\mathbf r\cdot\mathbf v)}{r^3}\mathbf r.
$$

Multiplying by $GM$ reproduces exactly the right-hand side above:

$$
\frac{d}{dt}(\mathbf v\times\boldsymbol\ell)
=
GM\,\frac{d}{dt}\left(\mathbf e_r\right).
$$

The two time derivatives are equal, so their difference is constant:

$$
\boxed{
\frac{d}{dt}\left[\frac{\mathbf v\times\boldsymbol\ell}{GM}-\mathbf e_r\right]=0.
}
$$

This is exactly $\mathbf e$. Its conservation follows purely from the
inverse-square equation of motion and the conservation of $\boldsymbol\ell$.

### Recovering the polar equation, and identifying $\mathbf e$

Take the dot product of $\mathbf r$ with the definition of $\mathbf e$:

$$
\mathbf r\cdot\mathbf e
=
\frac{\mathbf r\cdot(\mathbf v\times\boldsymbol\ell)}{GM}-\mathbf r\cdot\mathbf e_r.
$$

The scalar triple product can be cycled, $\mathbf r\cdot(\mathbf
v\times\boldsymbol\ell)=\boldsymbol\ell\cdot(\mathbf r\times\mathbf
v)=\boldsymbol\ell\cdot\boldsymbol\ell=\ell^2$, and $\mathbf r\cdot\mathbf
e_r=r$. Using $p=\ell^2/GM$,

$$
\mathbf r\cdot\mathbf e=p-r.
$$

Writing $\mathbf r\cdot\mathbf e=r\,e\cos\theta$, where $e=|\mathbf e|$ and
$\theta$ is the angle measured from the direction of $\mathbf e$, gives

$$
p-r=re\cos\theta
\quad\Longrightarrow\quad
\boxed{
r=\frac{p}{1+e\cos\theta}.
}
$$

Two conclusions follow at once, both falling out of the dot product rather
than assumed beforehand:

- $|\mathbf e|$ is the same eccentricity $e$ that classifies the conic
  (chapter 5).
- $\mathbf e$ points toward periapsis, since $r$ is smallest exactly where
  $\cos\theta=1$, i.e. where $\mathbf r$ is parallel to $\mathbf e$.

$\mathbf e$ is a scaled form of the classical **Laplace–Runge–Lenz vector**,
a conserved quantity special to the inverse-square force law (it is not
conserved for a general central force). Its existence is what makes the
Kepler orbit closed and non-precessing: a generic central force conserves
only $\boldsymbol\ell$ and $\varepsilon$, leaving the orbit's orientation
free to drift, but the inverse-square law supplies this extra conserved
direction that pins the periapsis in place.

## The recipe: from $(\mathbf r_0,\mathbf v_0)$ to the orbit

Given an initial position and velocity, the shape and orientation of the
orbit follow from three vector computations:

$$
\boxed{
\begin{aligned}
\boldsymbol\ell &= \mathbf r_0\times\mathbf v_0, \\[4pt]
\mathbf e &= \frac{\mathbf v_0\times\boldsymbol\ell}{GM}-\frac{\mathbf r_0}{r_0}, \\[4pt]
p &= \frac{\ell^2}{GM}.
\end{aligned}
}
$$

Then $e=|\mathbf e|$ classifies the conic (circle, ellipse, parabola,
hyperbola), and $\mathbf e/e$ is the unit vector toward periapsis, from which
$\theta$ — the angle of $\mathbf r_0$ measured from periapsis — can be read
off directly. The orbital plane itself is the plane perpendicular to
$\boldsymbol\ell$.

A fourth conserved quantity, the specific energy

$$
\varepsilon=\frac{v^2}{2}-\frac{GM}{r},
$$

is also computable immediately from $(\mathbf r_0,\mathbf v_0)$ (chapter 3).
It is not independent of $\boldsymbol\ell$ and $\mathbf e$: the next chapter
derives the relation between $\varepsilon$, $\ell$, and $e$ explicitly — a
second, independent route to the same eccentricity computed here — together
with what $\varepsilon$ says about the orbit's size and how speed trades off
against distance.
