# From orbit shape to motion in time

The conic equation

$$
r(\theta)=\frac{p}{1+e\cos\theta}
$$

determines the **shape** of the trajectory: the radius at every angle. It says
nothing about *when* the body is at a given angle. This note closes that gap
in two complementary ways: an exact analytic route through an auxiliary
"anomaly" angle and a transcendental time equation, and a direct numerical
route that integrates the Cartesian equations of motion. Both answer the same
question, $\mathbf r(t)$, but they trade off differently between analytic
insight and ease of implementation.

## From angular position to time

Conservation of specific angular momentum, $r^2\dot\theta=\ell$, gives

$$
\boxed{
dt=\frac{r^2}{\ell}\,d\theta.
}
$$

This is the bridge between the geometric orbit and its time evolution: once
$r(\theta)$ is known, the elapsed time between two angles is a definite
integral of $r(\theta)^2/\ell$. Substituting $r(\theta)=p/(1+e\cos\theta)$
gives

$$
t-\tau=\frac{p^2}{\ell}\int_0^{\theta}\frac{d\vartheta}{(1+e\cos\vartheta)^2},
$$

where $\tau$ is the time of periapsis passage ($\theta=0$). The integral is
elementary but its closed form depends on whether $e<1$, $e=1$, or $e>1$ —
which motivates introducing a different substitution, or **anomaly**, for
each case.

---

## Elliptical orbits: the eccentric anomaly and Kepler's equation

For $0\le e<1$, place the ellipse in a frame centered on the ellipse itself
(not the focus), with semi-major axis $a$ and semi-minor axis $b=a\sqrt{1-e^2}$
along the coordinate axes. The standard parametrization of this ellipse by an
angle $E$, the **eccentric anomaly**, is

$$
X=a\cos E,\qquad y=b\sin E,
$$

which satisfies $X^2/a^2+y^2/b^2=1$ for any $E$ by construction. Since the
focus sits a distance $ae$ from the ellipse's center along the major axis, the
focus-centered coordinate is $x=X-ae=a(\cos E-e)$, and $x=r\cos\theta$.
Combined with $r=\sqrt{x^2+y^2}$, this yields (after expanding and using
$b^2=a^2(1-e^2)$)

$$
\boxed{
r=a(1-e\cos E).
}
$$

Equating this with $x=r\cos\theta$ gives $a\cos E-ae=a(1-e\cos E)\cos\theta$,
and solving for $\cos E$,

$$
\boxed{
\cos E=\frac{e+\cos\theta}{1+e\cos\theta}.
}
$$

**Kepler's equation via areas.** Rather than integrating $dt=r^2d\theta/\ell$
directly, it is cleaner to use Kepler's second law together with the geometry
of the auxiliary circle of radius $a$ that circumscribes the ellipse.

The ellipse is the auxiliary circle compressed by a factor $b/a$ in the
$y$-direction. Areas scale by the same factor under this affine map, so the
area swept by the focus-to-body radius vector on the ellipse, from periapsis
to eccentric anomaly $E$, is $b/a$ times the corresponding area swept (from
the focus, not the center) on the circle.

On the circle, the sector from the center out to angle $E$ has area
$\tfrac12a^2E$. Subtracting the triangle formed by the center, the focus (a
distance $ae$ from the center), and the point on the circle — area
$\tfrac12(ae)(a\sin E)$ — gives the area swept from the *focus*:

$$
A_{\text{circle}}=\frac12a^2E-\frac12a^2e\sin E=\frac12a^2(E-e\sin E).
$$

Therefore the area swept on the ellipse is

$$
A_{\text{ellipse}}=\frac{b}{a}A_{\text{circle}}=\frac12ab(E-e\sin E).
$$

By Kepler's second law, $dA/dt=\ell/2$ is constant, so the area swept since
periapsis passage is also $A=\tfrac{\ell}{2}(t-\tau)$. Equating the two
expressions for $A$,

$$
t-\tau=\frac{ab}{\ell}(E-e\sin E).
$$

Using $\ell=\sqrt{GMa(1-e^2)}$ and $b=a\sqrt{1-e^2}$, the prefactor simplifies:

$$
\frac{ab}{\ell}=\frac{a\cdot a\sqrt{1-e^2}}{\sqrt{GMa(1-e^2)}}=\sqrt{\frac{a^3}{GM}}.
$$

Hence

$$
\boxed{
t-\tau=\sqrt{\frac{a^3}{GM}}\left(E-e\sin E\right).
}
$$

Defining the mean motion $n=\sqrt{GM/a^3}$ and the mean anomaly
$M=n(t-\tau)$ gives the compact form

$$
\boxed{
M=E-e\sin E.
}
$$

This is the **elliptic Kepler equation**. It is exact, but it is
transcendental in $E$: there is no elementary closed-form inverse $E(M)$.
Given a time $t$ (hence $M$), one solves

$$
f(E)=E-e\sin E-M=0
$$

numerically. Newton's method,

$$
E_{n+1}=E_n-\frac{E_n-e\sin E_n-M}{1-e\cos E_n},
$$

converges quadratically from the starting guess $E_0=M$ for small-to-moderate
$e$; convergence degrades as $e\to1$ and near $M\approx0,\pi$, where a
bisection safeguard or a better starting guess is used in practice.

---

## Hyperbolic orbits: the hyperbolic anomaly

For $e>1$ the same construction applies with circular functions replaced by
hyperbolic ones and $a<0$ by convention. Introducing the **hyperbolic
anomaly** $H$ through the analogous parametrization gives

$$
\boxed{
r=(-a)(e\cosh H-1).
}
$$

The hyperbola's "sector area" swept from the focus is the hyperbolic analogue
of the circular-sector construction above, $\tfrac12(-a)^2(e\sinh H-H)$, and
carrying the same equal-areas argument through gives

$$
\boxed{
t-\tau=\sqrt{\frac{(-a)^3}{GM}}\left(e\sinh H-H\right).
}
$$

With the hyperbolic mean anomaly $M=\sqrt{GM/(-a)^3}\,(t-\tau)$, this is the
**hyperbolic Kepler equation**,

$$
\boxed{
M=e\sinh H-H,
}
$$

again solved for $H$ by Newton's method given $M$.

---

## Parabolic orbits: Barker's equation

The parabolic case, $e=1$, has infinite semi-major axis, so neither
anomaly above applies. Instead substitute $D=\tan(\theta/2)$ directly into
$dt=r^2\,d\theta/\ell$. For a parabola $r=p/(1+\cos\theta)$, and the half-angle
identity $1+\cos\theta=2/(1+D^2)$ gives

$$
r=\frac{p}{2}(1+D^2),\qquad d\theta=\frac{2}{1+D^2}\,dD.
$$

Therefore

$$
r^2\,d\theta=\frac{p^2}{4}(1+D^2)^2\cdot\frac{2}{1+D^2}\,dD=\frac{p^2}{2}(1+D^2)\,dD,
$$

so

$$
dt=\frac{p^2}{2\ell}(1+D^2)\,dD.
$$

Integrating from periapsis ($D=0$ at $t=\tau$),

$$
t-\tau=\frac{p^2}{2\ell}\left(D+\frac{D^3}{3}\right).
$$

Since $p=\ell^2/GM$ holds for any conic, $p^2/\ell=\sqrt{p^3/GM}$, giving
**Barker's equation**:

$$
\boxed{
t-\tau=\frac12\sqrt{\frac{p^3}{GM}}\left(D+\frac{D^3}{3}\right).
}
$$

Unlike the elliptic and hyperbolic Kepler equations, this is an explicit
cubic in $D$ and can in principle be inverted in closed form (Cardano's
formula); in practice a numerical root solve is just as convenient.

---

## Common structure

$$
\boxed{
\begin{array}{c|c|c}
\text{Orbit} & \text{Anomaly} & \text{Time equation}\\
\hline
e<1 & E & M=E-e\sin E\\[4pt]
e=1 & D & t-\tau=\tfrac12\sqrt{p^3/GM}\left(D+D^3/3\right)\\[6pt]
e>1 & H & M=e\sinh H-H
\end{array}
}
$$

In every case the sequence is the same:

$$
\boxed{
\text{orbit shape}\longrightarrow\text{time-of-flight relation}\longrightarrow\text{anomaly}\longrightarrow\mathbf r(t),\mathbf v(t).
}
$$

Recovering the position and velocity vectors in the orbital plane, once $r$
and $\theta$ are known, uses

$$
\mathbf r=r\,\mathbf e_r,
\qquad
\dot r=\frac{GM}{\ell}e\sin\theta,
\qquad
r\dot\theta=\frac{GM}{\ell}(1+e\cos\theta),
$$

so that

$$
\boxed{
\mathbf v=\frac{GM}{\ell}\left[e\sin\theta\,\mathbf e_r+(1+e\cos\theta)\,\mathbf e_\theta\right].
}
$$

Rotating $\mathbf r$ and $\mathbf v$ from the orbital plane into the reference
frame — by the argument of periapsis $\omega$, inclination $i$, and longitude
of ascending node $\Omega$ from {doc}`05a_orbit_parameters` — gives the full
three-dimensional Cartesian state. Going the other way, from an initial
Cartesian state $(\mathbf r_0,\mathbf v_0)$ one computes
$\mathbf h=\mathbf r_0\times\mathbf v_0$, $\varepsilon=v_0^2/2-GM/r_0$, and the
eccentricity vector $\mathbf e=(\mathbf v_0\times\mathbf h)/GM-\mathbf r_0/r_0$
to recover $(a,e)$, the orbital plane, and the initial anomaly, closing the
loop between the two representations.

The conclusion of the analytic route is notable: **the ideal Newtonian
two-body problem does not require numerical integration of the equations of
motion.** The trajectory is known in closed form; propagation reduces to
advancing a time-of-flight relation and solving a single scalar transcendental
(or, for $e=1$, cubic) equation.

---

## The numerical route: integrating the Cartesian equations of motion

The anomaly-based method above is exact but specific to the unperturbed
two-body problem — every step relies on the conic solution. As soon as
additional forces are present (atmospheric drag, third-body perturbations,
solar radiation pressure, non-spherical gravity, or simply multiple attracting
bodies), no closed-form orbit exists and there is no anomaly to solve for.
The general-purpose alternative is to integrate Newton's equations directly as
an initial value problem in Cartesian coordinates.

### The ODE system

In Cartesian coordinates the equation of motion $\ddot{\mathbf r}=-GM\mathbf
r/r^3$ is a second-order vector ODE. Writing it as a first-order system in the
state vector $\mathbf y=(x,y,v_x,v_y)$ (planar case),

$$
\boxed{
\frac{d}{dt}
\begin{bmatrix}x\\y\\v_x\\v_y\end{bmatrix}
=
\begin{bmatrix}
v_x\\
v_y\\
-GM\,x/r^3\\
-GM\,y/r^3
\end{bmatrix},
\qquad r=\sqrt{x^2+y^2}.
}
$$

This is a four-dimensional initial value problem in the plane, or a
six-dimensional one in three dimensions with $(x,y,z,v_x,v_y,v_z)$. Compared
to the polar/anomaly formulation, the Cartesian form has no coordinate
singularity at $\theta=0$ or $r=0$ beyond the physical collision singularity,
treats every conic type (ellipse, parabola, hyperbola) with the same equation,
and generalizes immediately to any additional force by simply adding a term
to $\dot{\mathbf v}$. This is why numerical propagators for real
(perturbed) orbits are built on this Cartesian IVP rather than on the
anomaly formalism, even though the anomaly formalism is exact for the
unperturbed problem.

### Suitable classes of integrators

- **Explicit Runge-Kutta methods** (RK4, or adaptive-step embedded pairs such
  as RK45/Dormand-Prince). General-purpose, easy to implement, and adaptive
  step control keeps the local truncation error below a chosen tolerance.
  Adequate for propagating a handful of orbits, but the accumulated phase and
  energy error grows with the number of steps, which matters for long
  integrations.

- **Symplectic integrators** (leapfrog/Störmer-Verlet, higher-order symplectic
  composition methods, or specialized methods like Wisdom-Holman for
  near-Keplerian problems). These do not conserve energy exactly at each step
  but conserve a nearby "shadow" Hamiltonian, so the energy error stays
  bounded rather than drifting secularly over many orbital periods. They are
  the natural choice whenever the integration spans many orbits, e.g. for
  studying long-term stability.

- **Implicit methods** are generally unnecessary for the pure Kepler problem,
  which is not stiff, but become relevant once very different timescales are
  present (e.g. a highly eccentric orbit combined with a fast perturbing
  force).

- **High-order specialized propagators** (e.g. Gauss-Jackson multistep
  methods) are used in operational astrodynamics when very high accuracy is
  required over long arcs, at the cost of a more complex implementation.

For most exploratory or teaching purposes, an adaptive explicit Runge-Kutta
method is the simplest adequate choice; a symplectic integrator is preferable
once the goal is long-term qualitative behavior rather than short-term
precision.

### Quantities to monitor for correctness

Because the two-body problem has an exact analytic solution, it offers an
unusually strong test bed for validating a numerical integrator: several
quantities are known to be exactly conserved, and the exact trajectory itself
is available for direct comparison.

- **Specific energy**, $\varepsilon=v^2/2-GM/r$, must remain constant. A
  systematic drift (rather than small oscillation) indicates the step size is
  too large or the method is not appropriate for the required integration
  span.
- **Specific angular momentum**, $\ell=xv_y-yv_x$ (its $z$-component in the
  planar case), must also remain constant; it is a particularly sensitive
  check because integration errors that break the central-force symmetry show
  up here first.
- **The eccentricity vector**, $\mathbf e=(\mathbf v\times\mathbf h)/GM-\mathbf
  r/r$, should keep both constant magnitude and constant direction. A slowly
  rotating eccentricity vector is the signature of spurious numerical apsidal
  precession — an error a plain energy check can miss.
- **Direct comparison against the analytic solution.** Since $\mathbf r(t)$
  from the Kepler-equation route above is available in closed form (up to a
  cheap scalar root solve) for exactly the same initial conditions, the
  numerically integrated trajectory can be compared point-by-point against it.
  This is a validation opportunity specific to the two-body problem: most
  ODE integrators cannot be checked against an exact solution this directly.
- **Periodicity.** For a bound orbit, propagating for one period
  $T=2\pi\sqrt{a^3/GM}$ should return the state to its initial value; the
  residual is a convenient single-number accuracy diagnostic.

In the pure Kepler problem, numerical integration is a validation and
teaching exercise rather than a necessity, since the analytic route above
already solves it exactly. Its real purpose is as the foundation for
perturbed and many-body problems, where no analytic shape or anomaly exists —
and the two-body analytic solution developed in this note remains the
standard benchmark against which any such numerical propagator is first
checked.
