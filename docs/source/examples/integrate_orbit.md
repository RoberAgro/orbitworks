# Integrating a general Kepler orbit numerically

Run it from the repository root:

```bash
poetry run python examples/integrate_orbit.py
```

## What it shows

The script builds a Cartesian initial state at $4R_\oplus$ (the tangential
speed ratio is configurable at the top of the file: circle, ellipse,
parabola, and hyperbola cases are all noted there), integrates it numerically
with SciPy's adaptive DOP853, and compares the result against the exact
analytic conic through the same initial state — the numerical route and the
shape-only analytic route from {doc}`../theory/09_time_dependent_motion`,
side by side.

The printed report and the right-hand plot cover exactly the quantities that
chapter's "quantities to monitor for correctness" section recommends:
specific energy, specific angular momentum, and eccentricity-vector drift
(all as percentage deviations from their initial values), plus a fourth,
independent check — the propagated positions' deviation from the exact
conic shape. Because the unperturbed two-body problem has a closed-form
solution, this script can compare the numerical trajectory directly against
it, which is a validation opportunity most ODE integrators never get.

Bound orbits integrate for a fixed number of periods; open orbits integrate
until a configurable escape radius or a time cap, whichever comes first —
see {doc}`../theory/07_energy_and_vis_viva` for why only bound orbits have a
period to begin with.

