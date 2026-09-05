# Energy, orbital speed, and escape

Changing the tangential launch speed changes the orbit's shape and, at the
escape threshold, whether the motion remains bound. Energy gives a compact way
to distinguish these cases.

## What happens when the tangential speed differs from circular speed

At a given radius $r$,

$$
v_c=\sqrt{\frac{\mu}{r}}.
$$

If the object has exactly this tangential speed, the orbit is circular.

If the tangential speed is larger, gravity is not strong enough to bend the path with curvature $1/r$ at that instant.

The actual curvature is

$$
\kappa
=
\frac{g}{v^2}
=
\frac{\mu/r^2}{v^2}.
$$

For circular motion,

$$
\kappa_c=\frac{1}{r}.
$$

If

$$
v>v_c,
$$

then

$$
\frac{\mu}{r^2v^2}
<
\frac{1}{r},
$$

so

$$
\boxed{
\kappa<\frac{1}{r}
}
$$

The trajectory bends less sharply than the local circular path and therefore initially moves outward.

Whether it remains bound depends on its total mechanical energy.

---

## Escape velocity

The specific mechanical energy is

$$
\boxed{
\varepsilon
=
\frac{v^2}{2}
-
\frac{\mu}{r}
}
$$

where $\varepsilon$ is energy per unit mass.

At the threshold of escape, the body reaches infinity with zero remaining speed.

At infinity,

$$
\frac{\mu}{r}\rightarrow 0
$$

and

$$
v\rightarrow 0.
$$

Therefore the threshold energy is

$$
\varepsilon=0.
$$

Set

$$
\frac{v_{\mathrm{esc}}^2}{2}
-
\frac{\mu}{r}
=
0.
$$

Then

$$
\frac{v_{\mathrm{esc}}^2}{2}
=
\frac{\mu}{r}.
$$

Hence,

$$
\boxed{
v_{\mathrm{esc}}
=
\sqrt{\frac{2\mu}{r}}
}
$$

Since

$$
v_c=\sqrt{\frac{\mu}{r}},
$$

we obtain

$$
\boxed{
v_{\mathrm{esc}}
=
\sqrt{2}\,v_c
}
$$

For Earth near the surface,

$$
v_c\approx 7.9\ \mathrm{km/s},
$$

whereas

$$
v_{\mathrm{esc}}\approx 11.2\ \mathrm{km/s}.
$$

---

## Basic classification by speed and energy

For a purely tangential launch at radius $r$:

$$
v=v_c
$$

gives a circular orbit.

If

$$
v_c<v<v_{\mathrm{esc}},
$$

the object initially moves outward but remains gravitationally bound. Its orbit is an ellipse.

If

$$
v=v_{\mathrm{esc}},
$$

the orbit is parabolic.

If

$$
v>v_{\mathrm{esc}},
$$

the trajectory is hyperbolic.

For tangential launch below circular speed,

$$
v<v_c,
$$

the object initially curves inward more sharply than the local circle. In an ideal point-mass problem this is also an elliptical orbit, but if the launch occurs from a planetary surface, the ellipse may intersect the body.

The exact classification becomes especially clear once the general conic solution is derived.

