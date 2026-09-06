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

