# Conic sections from initial tangential speed

Run it from the repository root:

```bash
poetry run python examples/conic_sections.py
```

## What it shows

A body starts at a fixed radius $r_0=4R_\oplus$ with zero radial velocity, so
whenever its tangential speed is at least the local circular speed, that
starting point is periapsis. Four tangential speeds, expressed as ratios to
the local circular speed $v_c=\sqrt{GM/r_0}$,

$$
1,\qquad\sqrt{1.5},\qquad\sqrt2,\qquad\sqrt{2.5},
$$

produce a circle, an ellipse, a parabola, and a hyperbola respectively — the
same four cases used to build the classification table in
{doc}`../theory/05_conic_orbits`. The script prints a table of each case's
speed, specific energy, eccentricity, and semi-latus rectum, then plots the
four resulting shapes side by side.

## How it uses the shared package

Each initial state is classified with
{py:func}`orbitworks.analytical.classify_orbit` — the same function that
implements the eccentricity-vector derivation of {doc}`../theory/06_orbital_elements_from_state`
and the energy relations of {doc}`../theory/07_energy_and_vis_viva` — rather
than recomputing $e$, $p$, and the energy locally. The resulting
{py:class}`orbitworks.analytical.OrbitElements` is then sampled into points
with {py:func}`orbitworks.geometry.sample_conic`
({doc}`../theory/08_conic_geometry_atlas`), which trims the open parabolic and
hyperbolic branches to a finite plotting radius with
{py:func}`orbitworks.geometry.angle_limit_for_radius`. Both functions also
back {py:mod}`orbitworks.app`, so this script, the interactive app, and
{doc}`integrate_orbit` all classify and sample conics through the same tested
code.
