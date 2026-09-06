# OrbitWorks — repository specification and implementation roadmap

This document defines the intended architecture and educational goals of
the repository. Read it before implementing new features or restructuring
the package.

## 1. Purpose of the repository

This repository should be a small, well-structured computational laboratory for learning classical orbital mechanics from first principles.

The primary objective is not to build the most sophisticated or visually impressive orbital simulator possible. The objective is to create a codebase where the analytical equations, numerical methods, conservation laws, and geometric interpretation of Newtonian two-body motion can be explored interactively and verified against one another.

The project should make it easy to move through the following conceptual progression:

$$
\text{Newtonian gravity}
\rightarrow
\text{circular motion}
\rightarrow
\text{energy and angular momentum}
\rightarrow
\text{conic sections}
\rightarrow
\text{Kepler's laws}
\rightarrow
\text{numerical integration}
\rightarrow
\text{N-body extensions}
$$

The repository should therefore emphasize:

- clean physics,
- transparent equations,
- readable code,
- direct correspondence between mathematical derivations and code,
- dimensional consistency,
- numerical validation,
- visualization,
- small experiments that isolate one physical idea at a time.

A secondary objective is to provide a good foundation for future extensions such as perturbation analysis, orbital transfers, restricted three-body dynamics, and full N-body integration.

---

## 2. Guiding design principles

The implementation should follow a few principles throughout the repository.

### Keep the physics explicit

Avoid burying important equations inside abstractions.

For example, the gravitational acceleration should remain visibly connected to

$$
\mathbf a
=
-\frac{\mu}{r^3}\mathbf r
$$

rather than being hidden behind layers of framework code.

The code should make it easy to compare a function directly with the equation it implements.

### Separate analytical and numerical mechanics

Analytical orbital-element calculations and numerical ODE propagation should be implemented independently.

This allows important consistency checks such as:

$$
\text{analytical trajectory}
\approx
\text{numerically integrated trajectory}.
$$

The numerical solver should not depend internally on the analytical conic solution.

### Prefer small reusable functions

Examples include:

```python
circular_velocity(mu, r)
escape_velocity(mu, r)
specific_energy(mu, r_vec, v_vec)
specific_angular_momentum(r_vec, v_vec)
eccentricity_vector(mu, r_vec, v_vec)
orbital_elements(mu, r_vec, v_vec)
two_body_rhs(t, state, mu)
```

Each function should correspond to a clear physical concept.

### Use consistent units

The core package should not silently mix units.

A recommended convention is SI:

- distance in m,
- velocity in m/s,
- time in s,
- mass in kg,
- $\mu$ in m$^3$/s$^2$.

Examples and visualizations may convert to km, days, AU, or years for readability.

### Support nondimensional formulations

Nondimensionalization should be included explicitly because it reveals the universal structure of the two-body problem.

### Make validation part of the project

Energy conservation, angular momentum conservation, conic consistency, and Kepler-law verification should not be optional afterthoughts.

They should be first-class features.

---

## 3. Recommended repository structure

A suggested structure is:

```text
orbitworks/
├── README.md
├── pyproject.toml
├── LICENSE
├── .gitignore
├── docs/
│   ├── theory.md
│   ├── equations.md
│   ├── numerical_methods.md
│   └── experiments.md
├── src/
│   └── orbitworks/
│       ├── __init__.py
│       ├── constants.py
│       ├── analytical.py
│       ├── dynamics.py
│       ├── elements.py
│       ├── energy.py
│       ├── geometry.py
│       ├── nondimensional.py
│       ├── propagation.py
│       ├── diagnostics.py
│       ├── graphics_mpl.py
│       ├── graphics_plotly.py
│       ├── plotting.py
│       └── nbody.py
├── examples/
│   ├── 01_circular_orbits.py
│   ├── 02_escape_velocity.py
│   ├── 03_conic_sections.py
│   ├── 04_initial_conditions_to_elements.py
│   ├── 05_integrate_two_body_orbit.py
│   ├── 06_compare_analytical_numerical.py
│   ├── 07_conservation_diagnostics.py
│   ├── 08_kepler_second_law.py
│   ├── 09_kepler_third_law.py
│   ├── 10_nondimensional_orbits.py
│   ├── 11_integrator_comparison.py
│   └── 12_solar_system_demo.py
├── app/
│   └── streamlit_app.py
├── tests/
│   ├── test_analytical.py
│   ├── test_elements.py
│   ├── test_energy.py
│   ├── test_dynamics.py
│   ├── test_propagation.py
│   ├── test_nondimensional.py
│   └── test_nbody.py
```

The exact number of modules can be reduced initially. The important part is that analytical relations, numerical dynamics, orbital elements, diagnostics, and plotting remain conceptually separated.

---

## 4. Core physical constants

Create:

```text
src/orbitworks/constants.py
```

Recommended constants include:

```python
G
M_EARTH
R_EARTH
MU_EARTH
M_SUN
MU_SUN
AU
DAY
YEAR
```

Prefer authoritative numerical values and document their units.

The package should use the standard gravitational parameter

$$
\boxed{
\mu=GM
}
$$

throughout the orbital equations because $\mu$ appears directly in the dynamics and is often more convenient than carrying $G$ and $M$ separately.

---

## 5. Basic circular-orbit calculations

Implement the first analytical functions in:

```text
src/orbitworks/analytical.py
```

The minimum set should include:

```python
gravitational_acceleration(mu, r)
circular_velocity(mu, r)
escape_velocity(mu, r)
circular_period(mu, r)
```

These correspond to:

$$
g(r)=\frac{\mu}{r^2}
$$

$$
\boxed{
v_c=\sqrt{\frac{\mu}{r}}
}
$$

$$
\boxed{
v_{\mathrm{esc}}=\sqrt{\frac{2\mu}{r}}
}
$$

and

$$
\boxed{
T=2\pi\sqrt{\frac{r^3}{\mu}}
}
$$

The first scripts should visualize these functions.

Recommended plots:

- $g(r)$,
- $v_c(r)$,
- $v_{\mathrm{esc}}(r)$,
- $v_{\mathrm{esc}}/v_c$,
- $T(r)$,
- $T^2$ versus $r^3$.

The last plot should give a straight line and numerically illustrate Kepler's third law.

---

## 6. Newton's cannonball experiment

Create an educational script demonstrating Newton's cannonball argument.

The script should compare the local projectile drop

$$
y_{\mathrm{fall}}
=
\frac{gx^2}{2v^2}
$$

with the local curvature of a spherical surface

$$
y_{\mathrm{surface}}
\approx
\frac{x^2}{2R}.
$$

At

$$
v=\sqrt{gR},
$$

the local curvatures match.

The script should show several launch velocities:

$$
v<v_c,
$$

$$
v=v_c,
$$

and

$$
v>v_c.
$$

This experiment should be clearly identified as a local approximation when constant $g$ and flat tangent coordinates are used.

The exact orbital simulations should use inverse-square gravity.

---

## 7. Analytical conic-section module

Implement the conic equation:

$$
\boxed{
r(\theta)
=
\frac{p}{1+e\cos\theta}
}
$$

where

$$
\boxed{
p=\frac{h^2}{\mu}
}
$$

and, for ellipses,

$$
\boxed{
p=a(1-e^2)
}
$$

Functions might include:

```python
conic_radius(theta, p, e)
ellipse_radius(theta, a, e)
polar_to_cartesian(r, theta)
periapsis_radius(a, e)
apoapsis_radius(a, e)
semi_minor_axis(a, e)
```

Relevant relations are:

$$
b=a\sqrt{1-e^2}
$$

$$
r_p=a(1-e)
$$

$$
r_a=a(1+e)
$$

The plotting script should show several eccentricities:

$$
e=0,
\quad
e=0.2,
\quad
e=0.5,
\quad
e=0.8,
\quad
e=1,
\quad
e>1.
$$

The figure should clearly place the central body at a focus rather than at the ellipse center.

This distinction is important and should be visually obvious.

---

## 8. Conic classification

Provide a function such as:

```python
classify_orbit_from_eccentricity(e, tolerance=...)
```

with classifications:

$$
e=0
\rightarrow
\text{circle}
$$

$$
0<e<1
\rightarrow
\text{ellipse}
$$

$$
e=1
\rightarrow
\text{parabola}
$$

$$
e>1
\rightarrow
\text{hyperbola}
$$

Because floating-point values rarely equal exactly $1$, the implementation should use an explicit numerical tolerance.

A second classification should use specific mechanical energy:

$$
\varepsilon<0
\rightarrow
\text{bound}
$$

$$
\varepsilon=0
\rightarrow
\text{parabolic escape}
$$

$$
\varepsilon>0
\rightarrow
\text{hyperbolic escape}.
$$

---

## 9. Energy calculations

Create:

```text
src/orbitworks/energy.py
```

Implement:

```python
specific_kinetic_energy(v_vec)
specific_gravitational_potential(mu, r)
specific_energy(mu, r_vec, v_vec)
vis_viva_speed(mu, r, a)
```

The primary equations are:

$$
\boxed{
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}
}
$$

for the general two-body state,

$$
\boxed{
\varepsilon
=
-\frac{\mu}{2a}
}
$$

for an ellipse, and

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

for the vis-viva equation.

The implementation should make it easy to verify that the same value of $\varepsilon$ is obtained everywhere along an analytically defined ellipse.

---

## 10. Angular momentum

Implement specific angular momentum:

$$
\boxed{
\mathbf h
=
\mathbf r\times\mathbf v
}
$$

and its magnitude

$$
h=|\mathbf h|.
$$

For planar motion,

$$
\boxed{
h=xv_y-yv_x
}
$$

The package should also expose the relation

$$
\boxed{
p=\frac{h^2}{\mu}
}
$$

and, for an ellipse,

$$
\boxed{
h^2
=
\mu a(1-e^2)
}
$$

These relations are useful both analytically and for validating numerical solutions.

---

## 11. Eccentricity vector

Implement the eccentricity vector:

$$
\boxed{
\mathbf e
=
\frac{\mathbf v\times\mathbf h}{\mu}
-
\frac{\mathbf r}{r}
}
$$

Its magnitude is the orbital eccentricity:

$$
\boxed{
e=|\mathbf e|
}
$$

The eccentricity vector points toward periapsis.

This should be preferred over extracting eccentricity from geometry when converting arbitrary initial conditions into orbital elements.

Useful functions:

```python
eccentricity_vector(mu, r_vec, v_vec)
eccentricity(mu, r_vec, v_vec)
```

The implementation should be checked against:

$$
\boxed{
e^2
=
1+
\frac{2\varepsilon h^2}{\mu^2}
}
$$

---

## 12. Initial state to orbital parameters

Create:

```text
src/orbitworks/elements.py
```

At minimum, the module should convert

$$
\mathbf r_0,\mathbf v_0
$$

into:

- radius $r$,
- speed $v$,
- specific energy $\varepsilon$,
- specific angular momentum $\mathbf h$,
- eccentricity vector $\mathbf e$,
- eccentricity $e$,
- semi-major axis $a$ where applicable,
- semi-latus rectum $p$,
- periapsis radius,
- apoapsis radius for bound orbits,
- orbit classification.

For bound and unbound conics, the semi-major axis can be obtained from:

$$
\boxed{
a=-\frac{\mu}{2\varepsilon}
}
$$

provided

$$
\varepsilon\neq0.
$$

For a parabolic orbit, $a$ is formally infinite.

The code should handle this explicitly rather than returning misleading finite values.

---

## 13. Tangential launch experiment

This should be one of the main educational scripts.

Choose a starting radius $r_0$ and tangential launch velocity $v$.

Compute:

$$
v_c
=
\sqrt{\frac{\mu}{r_0}}
$$

and

$$
v_{\mathrm{esc}}
=
\sqrt{\frac{2\mu}{r_0}}.
$$

For tangential launch above circular velocity and below escape velocity,

$$
v_c<v<v_{\mathrm{esc}},
$$

the starting point is periapsis.

For this special case,

$$
\boxed{
e
=
\frac{v^2}{v_c^2}
-
1
}
$$

The repository should verify this numerically.

Suggested dimensionless launch speeds are:

$$
\frac{v}{v_c}
=
0.7,\,
0.8,\,
1.0,\,
1.1,\,
1.2,\,
1.3,\,
\sqrt{2},\,
1.6.
$$

For each case, calculate:

- orbital energy,
- eccentricity,
- periapsis,
- apoapsis when applicable,
- orbital classification,
- analytical trajectory.

This single experiment connects speed, energy, curvature, and conic geometry.

---

## 14. Cartesian equations of motion

Create:

```text
src/orbitworks/dynamics.py
```

The basic two-body equation is

$$
\boxed{
\ddot{\mathbf r}
=
-\frac{\mu}{r^3}\mathbf r
}
$$

In two dimensions,

$$
\dot x=v_x,
$$

$$
\dot y=v_y,
$$

$$
\dot v_x
=
-\frac{\mu x}
{(x^2+y^2)^{3/2}},
$$

$$
\dot v_y
=
-\frac{\mu y}
{(x^2+y^2)^{3/2}}.
$$

The state vector may be defined as

$$
\mathbf y
=
[x,y,v_x,v_y]^T.
$$

Implement:

```python
two_body_rhs_2d(t, state, mu)
```

A 3-D version should also be considered:

$$
\mathbf y
=
[x,y,z,v_x,v_y,v_z]^T.
$$

with

$$
\dot{\mathbf r}=\mathbf v,
$$

$$
\dot{\mathbf v}
=
-\frac{\mu}{|\mathbf r|^3}\mathbf r.
$$

---

## 15. Numerical propagation

Create:

```text
src/orbitworks/propagation.py
```

Use JAX arrays and Diffrax's solver interface:

```python
diffrax.diffeqsolve
```

Implement a wrapper such as:

```python
propagate_two_body(
    r0,
    v0,
    mu,
    t0,
    t1,
    saveat,
    solver=None,
    dt0=None,
    rtol=...,
    atol=...
)
```

The wrapper should return a clean result object or dictionary with:

- time,
- position,
- velocity,
- radius,
- speed,
- solver metadata.

It should be possible to use different Diffrax solvers for comparison.

Recommended methods to explore:

- `Tsit5`,
- `Dopri8`,
- an appropriate implicit solver such as `Kvaerno5`,
- directly implemented fixed-step RK4 and symplectic methods.

The default should favor accuracy for smooth orbital problems.

---

## 16. Analytical versus numerical orbit comparison

This should be one of the core demonstrations.

Procedure:

1. Define an initial state $(\mathbf r_0,\mathbf v_0)$.
2. Compute analytical orbital elements.
3. Construct the analytical conic.
4. Integrate the Cartesian ODE numerically.
5. Overlay both trajectories.

The numerical and analytical trajectories should agree closely for the ideal two-body problem.

This experiment validates both implementations simultaneously.

The comparison should be performed for:

- circular orbit,
- moderately eccentric ellipse,
- highly eccentric ellipse,
- near-parabolic trajectory,
- hyperbolic trajectory.

---

## 17. Conservation-law diagnostics

Create:

```text
src/orbitworks/diagnostics.py
```

For every propagated state, calculate:

$$
\varepsilon(t)
=
\frac{v(t)^2}{2}
-
\frac{\mu}{r(t)}
$$

and

$$
\mathbf h(t)
=
\mathbf r(t)\times\mathbf v(t).
$$

Define relative conservation errors such as:

$$
\boxed{
\delta_\varepsilon(t)
=
\frac{
\varepsilon(t)-\varepsilon(0)
}{
|\varepsilon(0)|
}
}
$$

and

$$
\boxed{
\delta_h(t)
=
\frac{
h(t)-h(0)
}{
h(0)
}
}
$$

for cases where these normalizations are well defined.

The repository should provide plots of:

- position trajectory,
- energy versus time,
- relative energy error,
- angular momentum versus time,
- relative angular-momentum error.

These diagnostics are essential for understanding numerical integration.

---

## 18. Kepler's second law as a numerical experiment

The theoretical relation is

$$
\boxed{
\frac{dA}{dt}
=
\frac{h}{2}
}
$$

For discrete trajectory points, the swept area between two neighboring position vectors can be approximated by

$$
\Delta A
\approx
\frac{1}{2}
|\mathbf r_i\times\mathbf r_{i+1}|.
$$

For equal time intervals,

$$
\Delta t=\mathrm{constant},
$$

the values of

$$
\frac{\Delta A}{\Delta t}
$$

should remain approximately constant.

Create a script that:

- propagates an eccentric ellipse,
- divides the trajectory into equal time intervals,
- visualizes several swept sectors,
- calculates swept area for each interval,
- compares them numerically,
- compares the result with $h/2$.

This experiment should make Kepler's second law visually and quantitatively clear.

---

## 19. Kepler's third law as a numerical experiment

For a family of elliptical or circular orbits, calculate periods and semi-major axes.

Verify:

$$
\boxed{
T^2
=
\frac{4\pi^2}{\mu}a^3
}
$$

Possible numerical experiment:

1. Generate several values of $a$.
2. Propagate one complete orbit for each.
3. Estimate the orbital period numerically.
4. Plot $T^2$ against $a^3$.
5. Fit a straight line.
6. Compare its slope with

$$
\boxed{
\frac{4\pi^2}{\mu}
}
$$

The code should report the relative error in the fitted slope.

---

## 20. Nondimensionalization

Create:

```text
src/orbitworks/nondimensional.py
```

Choose a reference length $r_0$.

Define the characteristic velocity

$$
\boxed{
v_0
=
\sqrt{\frac{\mu}{r_0}}
}
$$

and characteristic time

$$
\boxed{
t_0
=
\sqrt{\frac{r_0^3}{\mu}}
}
$$

Define nondimensional variables:

$$
\tilde{\mathbf r}
=
\frac{\mathbf r}{r_0},
$$

$$
\tilde{\mathbf v}
=
\frac{\mathbf v}{v_0},
$$

$$
\tilde t
=
\frac{t}{t_0}.
$$

The dimensional equation

$$
\frac{d^2\mathbf r}{dt^2}
=
-\frac{\mu}{r^3}\mathbf r
$$

then becomes

$$
\boxed{
\frac{d^2\tilde{\mathbf r}}
{d\tilde t^2}
=
-
\frac{
\tilde{\mathbf r}
}{
|\tilde{\mathbf r}|^3
}
}
$$

The important point is that the parameter $\mu$ disappears completely.

The repository should provide utility functions for conversion between dimensional and nondimensional quantities.

---

## 21. Canonical nondimensional orbit experiment

Use:

$$
\mu=1,
\qquad
r_0=1.
$$

Then:

$$
v_c=1
$$

and

$$
v_{\mathrm{esc}}=\sqrt{2}.
$$

Start at

$$
\mathbf r_0=(1,0)
$$

with tangential velocity

$$
\mathbf v_0=(0,v).
$$

Run the following cases:

$$
v=0.8,
$$

$$
v=1.0,
$$

$$
v=1.1,
$$

$$
v=1.3,
$$

$$
v=\sqrt{2},
$$

$$
v=1.6.
$$

For every case:

- compute $\varepsilon$,
- compute $\mathbf h$,
- compute $e$,
- classify the orbit,
- generate the analytical conic,
- numerically integrate the trajectory,
- overlay the two,
- report conservation errors.

For the cases

$$
1<v<\sqrt{2},
$$

verify

$$
\boxed{
e=v^2-1
}
$$

because

$$
v_c=1.
$$

This should be treated as a flagship experiment in the repository.

---

## 22. Integrator comparison

A later educational extension should compare numerical integrators.

Compare at least:

- Diffrax `Tsit5`,
- Diffrax `Dopri8`,
- a simple fixed-step RK4 implementation,
- a symplectic method such as velocity Verlet or leapfrog.

The purpose is not merely performance benchmarking.

The important question is how different integrators behave with respect to conserved quantities.

For each method, compare:

- trajectory accuracy,
- energy drift,
- angular momentum drift,
- computational cost,
- behavior over many orbital periods.

A symplectic method should be included because orbital mechanics provides an excellent demonstration of why preserving Hamiltonian structure matters for long-time integration.

---

## 23. Implement a simple symplectic integrator

Implement either velocity Verlet or leapfrog.

For velocity Verlet, one possible form is:

$$
\mathbf v_{n+1/2}
=
\mathbf v_n
+
\frac{\Delta t}{2}
\mathbf a(\mathbf r_n),
$$

$$
\mathbf r_{n+1}
=
\mathbf r_n
+
\Delta t\,\mathbf v_{n+1/2},
$$

$$
\mathbf v_{n+1}
=
\mathbf v_{n+1/2}
+
\frac{\Delta t}{2}
\mathbf a(\mathbf r_{n+1}).
$$

Compare long-term energy behavior with standard RK methods.

This is a worthwhile extension because it links orbital mechanics with numerical Hamiltonian dynamics.

---

## 24. Interactive orbit explorer

Create:

```text
app/streamlit_app.py
```

The app should remain lightweight.

Recommended controls:

- central body,
- central mass or $\mu$,
- starting radius,
- radial velocity,
- tangential velocity,
- velocity expressed optionally as $v/v_c$,
- integration duration,
- solver tolerance,
- plotting time range.

Recommended outputs:

- orbit trajectory,
- starting point,
- central body position,
- analytical conic overlay where possible,
- current orbital classification,
- eccentricity,
- semi-major axis,
- semi-latus rectum,
- periapsis,
- apoapsis,
- specific energy,
- specific angular momentum,
- orbital period for bound ellipses,
- escape status,
- conservation-error plots.

A particularly useful slider is:

$$
\boxed{
\frac{v}{v_c}
}
$$

because moving this value continuously shows the transition between different orbital regimes.

Suggested slider range:

$$
0.5
\le
\frac{v}{v_c}
\le
2.
$$

Important reference values should be visible:

$$
\frac{v}{v_c}=1
$$

for circular orbit and

$$
\frac{v}{v_c}=\sqrt{2}
$$

for escape from a tangential launch.

---

## 25. Visualizations to include

The plotting module should eventually support:

- orbit in Cartesian coordinates,
- polar orbit,
- central body and focus,
- periapsis and apoapsis markers,
- velocity vectors,
- acceleration vectors,
- eccentricity vector,
- angular momentum direction for 3-D cases,
- swept-area sectors,
- energy versus time,
- angular momentum versus time,
- radius versus time,
- speed versus time,
- true anomaly versus time,
- analytical versus numerical trajectory,
- integrator error comparisons.

Plots should preserve equal axis scaling for orbital geometry.

A circle should visually appear as a circle.

Use:

```python
ax.set_aspect("equal")
```

or an equivalent approach where appropriate.

---

## 26. Plotting conventions

Create:

```text
src/orbitworks/plotting.py
```

Plotting helpers should avoid mixing physics calculations with visualization logic.

Shared library defaults belong in:

```text
src/orbitworks/graphics_mpl.py
src/orbitworks/graphics_plotly.py
```

Use Matplotlib for static and publication-oriented figures and Plotly for
interactive figures. Both backends should share compatible colors, typography,
grid treatment, and line weights.

Suggested functions:

```python
plot_orbit(...)
plot_conic(...)
plot_state_vectors(...)
plot_conservation_errors(...)
plot_swept_areas(...)
plot_analytical_vs_numerical(...)
```

Every orbital plot should clearly indicate:

- coordinate units,
- central body,
- initial condition,
- equal aspect ratio,
- meaningful labels.

Avoid unnecessary decorative complexity.

The plots should primarily help interpret the equations.

---

## 27. Documentation structure

The `docs/` folder should contain explanatory Markdown files.

Recommended:

```text
docs/theory.md
```

A condensed derivation of:

- Newtonian gravitation,
- circular orbital velocity,
- escape velocity,
- conservation of angular momentum,
- Kepler's second law,
- Binet equation,
- conic solution,
- energy classification,
- Kepler's third law.

```text
docs/equations.md
```

A compact equation reference.

```text
docs/numerical_methods.md
```

Discussion of:

- state-vector formulation,
- ODE integration,
- error tolerances,
- conservation-law diagnostics,
- RK versus symplectic methods.

```text
docs/experiments.md
```

Descriptions of all computational experiments and what each is intended to demonstrate physically.

The previously prepared detailed orbital-mechanics derivation can be adapted into `docs/theory.md`.

---

## 28. README requirements

The main README should explain immediately what the project is.

Recommended sections:

```text
# OrbitWorks

## Purpose
## Physics covered
## Installation
## Quick start
## Repository structure
## Example experiments
## Interactive app
## Validation philosophy
## Future extensions
```

The README should include at least one representative orbit figure once the plotting scripts exist.

It should emphasize that this is an educational computational mechanics project rather than a high-fidelity astrodynamics package.

---

## 29. Testing philosophy

The repository should use `pytest`.

Tests should verify physical identities, not only software behavior.

Examples:

### Circular velocity

Given $r$,

$$
\frac{v_c^2}{r}
=
\frac{\mu}{r^2}.
$$

### Escape velocity

Verify:

$$
v_{\mathrm{esc}}
=
\sqrt{2}\,v_c.
$$

### Circular eccentricity

For a circular initial condition,

$$
e\approx0.
$$

### Elliptical energy

For an ellipse,

$$
\varepsilon
=
-\frac{\mu}{2a}.
$$

### Semi-latus rectum

Verify:

$$
p
=
\frac{h^2}{\mu}
=
a(1-e^2).
$$

### Vis-viva

Verify:

$$
v^2
=
\mu
\left(
\frac{2}{r}
-
\frac{1}{a}
\right).
$$

### Tangential-launch eccentricity

For

$$
v_c<v<v_{\mathrm{esc}},
$$

verify:

$$
e
=
\frac{v^2}{v_c^2}-1.
$$

### Numerical conservation

For a well-resolved two-body simulation:

$$
\varepsilon(t)
\approx
\varepsilon(0)
$$

and

$$
h(t)
\approx
h(0).
$$

The tolerances should be chosen in accordance with the numerical method and solver settings.

---

## 30. Error handling and numerical robustness

The implementation should explicitly consider:

- zero-radius singularity,
- near-parabolic trajectories,
- nearly circular trajectories,
- floating-point comparison around $e=1$,
- division by very small energy when calculating $a$,
- extreme eccentricity,
- integration too close to the singularity,
- invalid state-vector dimensions,
- nonfinite input values.

Avoid silently returning physically meaningless quantities.

For example, if

$$
|\varepsilon|
$$

is numerically indistinguishable from zero, classify the state as approximately parabolic rather than calculating an enormous finite semi-major axis and treating it as reliable.

---

## 31. Coordinate and state conventions

Document all conventions clearly.

Recommended 2-D state:

$$
[x,y,v_x,v_y].
$$

Recommended 3-D state:

$$
[x,y,z,v_x,v_y,v_z].
$$

Recommended central body location:

$$
\mathbf r=(0,0)
$$

or

$$
\mathbf r=(0,0,0).
$$

Recommended default orbital plane:

$$
z=0.
$$

For the standard tangential-launch experiments, use:

$$
\mathbf r_0=(r_0,0)
$$

and

$$
\mathbf v_0=(0,v_0).
$$

This makes periapsis orientation and conic plots easy to interpret.

---

## 32. Solar-system visualization — first version

The first solar-system visualization should remain a collection of independent two-body Sun–planet orbits.

For each planet:

- use the Sun as the fixed central mass,
- assign its orbital semi-major axis,
- assign an approximate eccentricity,
- propagate analytically or numerically,
- display all planetary trajectories.

This version should be described clearly as a set of uncoupled two-body approximations.

The purpose is visualization and scale comparison, not precision ephemeris prediction.

Because orbital radii differ greatly, consider multiple visualization modes:

- true spatial scale,
- normalized/semi-log display,
- inner planets only,
- outer planets only.

---

## 33. N-body model

After the two-body framework is solid, add:

```text
src/orbitworks/nbody.py
```

For body $i$,

$$
\boxed{
\ddot{\mathbf r}_i
=
G
\sum_{j\neq i}
m_j
\frac{
\mathbf r_j-\mathbf r_i
}{
|\mathbf r_j-\mathbf r_i|^3
}
}
$$

Implement:

```python
nbody_rhs(t, state, masses, G)
```

The state may contain all body positions and velocities flattened into a single vector.

The implementation should first be tested with:

- two-body case,
- symmetric binary system,
- simple three-body configuration.

Only later should it be used for a solar-system mock-up.

---

## 34. Two-body center-of-mass extension

The initial treatment assumes

$$
M\gg m
$$

and places the central body at rest.

A useful later extension is the exact two-body formulation.

Define relative position:

$$
\mathbf r
=
\mathbf r_2-\mathbf r_1.
$$

The relative motion obeys

$$
\boxed{
\ddot{\mathbf r}
=
-\frac{G(M+m)}{r^3}\mathbf r
}
$$

so the effective gravitational parameter is

$$
\boxed{
\mu=G(M+m)
}
$$

The two bodies orbit their common center of mass.

This extension helps explain binary stars and systems where the secondary mass cannot be neglected.

---

## 35. Possible future orbital-transfer module

A useful future extension would be orbital maneuvers.

Potential topics:

- impulsive $\Delta v$,
- Hohmann transfer,
- plane change,
- escape injection,
- capture,
- transfer time.

For a Hohmann transfer between circular radii $r_1$ and $r_2$, the transfer ellipse has

$$
a_t
=
\frac{r_1+r_2}{2}.
$$

Vis-viva can then be used to derive the required burn velocities.

This should not be part of the first implementation phase but fits naturally after the core mechanics are complete.

---

## 36. Possible future perturbation topics

Potential later additions include:

- atmospheric drag,
- oblateness and $J_2$,
- third-body perturbations,
- solar radiation pressure,
- relativistic perihelion precession,
- thrust-driven trajectories.

These should remain outside the initial project scope.

The value of the initial repository lies in keeping the ideal Newtonian problem transparent.

---

## 37. Possible future restricted three-body work

Another future branch could introduce the circular restricted three-body problem.

Relevant topics include:

- rotating reference frame,
- effective potential,
- Jacobi constant,
- Lagrange points,
- zero-velocity curves,
- halo and periodic orbits.

This is a logical extension once the user is comfortable with energy, angular momentum, and effective potentials in the two-body problem.

---

## 38. Dependencies

Recommended initial dependencies:

```text
jax
diffrax
equinox
matplotlib
plotly
streamlit
pytest
```

Avoid unnecessary dependencies during the early stages.

A minimal `pyproject.toml` should define:

- package metadata,
- Python version,
- dependencies,
- optional development dependencies,
- pytest configuration if useful.

Potential development tools:

```text
ruff
black
mypy
```

These are optional but useful if the repository is intended to remain clean.

---

## 39. Recommended implementation order

The project should be developed in phases.

### Phase 1 — algebraic mechanics

Implement:

- constants,
- gravitational acceleration,
- circular velocity,
- escape velocity,
- circular period,
- basic tests,
- simple plots.

Goal:

Understand the basic scaling laws and validate the package setup.

### Phase 2 — analytical conics

Implement:

- conic equation,
- ellipse geometry,
- periapsis,
- apoapsis,
- conic plotting,
- eccentricity classification.

Goal:

Understand how eccentricity controls orbital geometry.

### Phase 3 — conservation laws and orbital elements

Implement:

- energy,
- angular momentum,
- eccentricity vector,
- initial-state-to-elements conversion,
- vis-viva,
- tests.

Goal:

Understand how initial conditions determine the orbit.

### Phase 4 — numerical propagation

Implement:

- Cartesian RHS,
- JAX and Diffrax propagation,
- trajectory plotting,
- conservation diagnostics.

Goal:

Solve the same mechanics without assuming the conic form.

### Phase 5 — analytical/numerical comparison

Implement:

- analytical orbit from initial state,
- numerical integration,
- trajectory overlay,
- error metrics.

Goal:

Demonstrate that Newton's ODE solution and the conic equation describe the same motion.

### Phase 6 — Kepler-law experiments

Implement:

- swept-area numerical verification,
- period versus semi-major-axis verification,
- corresponding visualizations.

Goal:

Recover Kepler's empirical laws directly from Newtonian mechanics.

### Phase 7 — nondimensional mechanics

Implement:

- scaling utilities,
- canonical $\mu=1$, $r_0=1$ experiments,
- velocity-ratio sweep.

Goal:

Reveal the universal structure of the two-body equations.

### Phase 8 — numerical-method experiments

Implement:

- RK4,
- leapfrog or velocity Verlet,
- integrator comparison,
- long-term conservation analysis.

Goal:

Connect orbital mechanics with numerical analysis.

### Phase 9 — interactive app

Implement:

- Streamlit controls,
- live orbit classification,
- plots and diagnostics.

Goal:

Make the equations easy to explore experimentally.

### Phase 10 — multi-body extensions

Implement:

- exact two-body center-of-mass motion,
- N-body RHS,
- solar-system demonstration.

Goal:

Show where the exact Keplerian solution ceases to apply.

---

## 40. Suggested milestone checklist

Use the following as the main implementation checklist.

- [ ] Initialize repository and `pyproject.toml`
- [ ] Create `src/orbitworks/`
- [ ] Add constants and unit documentation
- [ ] Implement gravitational acceleration
- [ ] Implement circular velocity
- [ ] Implement escape velocity
- [ ] Implement circular orbital period
- [ ] Add algebraic unit tests
- [ ] Create circular-orbit plotting script
- [ ] Create Newton cannonball demonstration
- [ ] Implement conic radius equation
- [ ] Implement ellipse geometry relations
- [ ] Plot multiple eccentricities
- [ ] Show central body at one focus
- [ ] Implement specific mechanical energy
- [ ] Implement angular momentum
- [ ] Implement eccentricity vector
- [ ] Implement orbit classification
- [ ] Implement initial-state-to-elements conversion
- [ ] Implement semi-major axis from energy
- [ ] Implement semi-latus rectum
- [ ] Implement periapsis and apoapsis
- [ ] Implement vis-viva equation
- [ ] Verify all analytical identities with tests
- [ ] Implement two-body Cartesian RHS
- [ ] Add 2-D numerical propagation
- [ ] Add 3-D numerical propagation
- [ ] Add solver wrapper around `diffrax.diffeqsolve`
- [ ] Plot numerically integrated circular orbit
- [ ] Plot numerically integrated elliptical orbit
- [ ] Plot parabolic escape case
- [ ] Plot hyperbolic case
- [ ] Overlay analytical and numerical trajectories
- [ ] Implement energy conservation diagnostics
- [ ] Implement angular momentum conservation diagnostics
- [ ] Add conservation-error plots
- [ ] Verify Kepler's second law numerically
- [ ] Visualize equal swept areas
- [ ] Verify Kepler's third law numerically
- [ ] Plot $T^2$ versus $a^3$
- [ ] Implement nondimensional scaling
- [ ] Implement canonical $\mu=1$ experiments
- [ ] Sweep $v/v_c$ across orbital regimes
- [ ] Verify $e=v^2-1$ for nondimensional tangential launch with $v>1$
- [ ] Add simple RK4 integrator
- [ ] Add leapfrog or velocity Verlet integrator
- [ ] Compare integrator accuracy
- [ ] Compare long-term energy behavior
- [ ] Create plotting helper module
- [ ] Create documentation pages
- [ ] Adapt the orbital derivation into `docs/theory.md`
- [ ] Add compact equation reference
- [ ] Add experiment descriptions
- [ ] Create Streamlit orbit explorer
- [ ] Add $v/v_c$ interactive slider
- [ ] Display live orbital elements
- [ ] Display analytical/numerical overlay in app
- [ ] Add conservation plots to app
- [ ] Add approximate uncoupled solar-system visualization
- [ ] Implement exact two-body center-of-mass formulation
- [ ] Implement N-body RHS
- [ ] Test N-body model against two-body limit
- [ ] Add simple three-body example
- [ ] Add N-body solar-system demonstration
- [ ] Review numerical tolerances and edge cases
- [ ] Improve README and screenshots
- [ ] Add continuous integration for tests
- [ ] Tag a first stable educational release

---

## 41. High-value experiments to prioritize

If development time is limited, prioritize these experiments above all others.

### Experiment 1 — circular velocity and escape velocity

Plot:

$$
v_c(r)
=
\sqrt{\frac{\mu}{r}}
$$

and

$$
v_{\mathrm{esc}}(r)
=
\sqrt{\frac{2\mu}{r}}.
$$

Show explicitly that:

$$
\frac{v_{\mathrm{esc}}}{v_c}
=
\sqrt{2}.
$$

### Experiment 2 — eccentricity sweep

Plot:

$$
r
=
\frac{p}{1+e\cos\theta}
$$

for several values of $e$.

This gives the cleanest geometric view of conic classification.

### Experiment 3 — tangential launch velocity sweep

At fixed radius, vary

$$
v/v_c.
$$

Show the transition:

$$
\text{sub-circular ellipse}
\rightarrow
\text{circle}
\rightarrow
\text{super-circular ellipse}
\rightarrow
\text{parabola}
\rightarrow
\text{hyperbola}.
$$

### Experiment 4 — analytical versus ODE solution

Overlay the conic solution with the numerical integration of

$$
\ddot{\mathbf r}
=
-\frac{\mu}{r^3}\mathbf r.
$$

This is arguably the most important computational demonstration in the repository.

### Experiment 5 — conservation diagnostics

Plot numerical error in:

$$
\varepsilon
$$

and

$$
h.
$$

This turns the repository from a visualization exercise into a numerical-mechanics laboratory.

### Experiment 6 — equal areas in equal times

Numerically demonstrate Kepler's second law for a visibly eccentric orbit.

### Experiment 7 — Kepler's third law

Generate multiple orbits and verify:

$$
T^2\propto a^3.
$$

### Experiment 8 — nondimensional universal orbit

Set:

$$
\mu=1,
\qquad
r_0=1,
\qquad
v_c=1.
$$

Sweep initial velocity and classify the resulting conic.

This is perhaps the cleanest single demonstration of the complete orbital structure.

---

## 42. Definition of a good first release

The project does not need N-body dynamics or a sophisticated UI before being useful.

A strong version `0.1.0` would contain:

- analytical circular orbit relations,
- conic-section plotting,
- energy and angular momentum,
- eccentricity vector,
- initial conditions to orbital elements,
- numerical two-body integration,
- analytical versus numerical comparison,
- conservation diagnostics,
- Kepler's second-law demonstration,
- Kepler's third-law demonstration,
- nondimensional velocity sweep,
- good tests,
- clear theory documentation.

That alone would already provide a complete computational treatment of the Newtonian two-body problem.

---

## 43. Context for future coding assistants

Any coding assistant working on this repository should preserve the educational purpose of the project.

The intended style is:

- mathematically explicit,
- physically correct,
- compact rather than overengineered,
- well tested,
- easy to inspect,
- easy to modify,
- suitable for experimentation.

Do not replace transparent mechanics with opaque high-level astrodynamics libraries unless an extension specifically requires them.

The point of the project is to implement the equations directly.

When adding a new feature, the preferred workflow is:

1. state the physical equation,
2. implement it in a small function,
3. test it against an analytical identity,
4. create a minimal experiment,
5. visualize the result if visualization improves understanding,
6. document the physical interpretation.

Where analytical and numerical approaches both exist, implement both and compare them.

Where conservation laws exist, monitor them.

Where nondimensionalization clarifies the physics, expose it.

Where a result can be derived from earlier equations, prefer deriving and verifying it rather than treating it as an isolated formula.

The central conceptual chain that the repository should preserve is:

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
\rightarrow
\text{numerical verification}
}
$$

This should remain the organizing principle of the entire project.
