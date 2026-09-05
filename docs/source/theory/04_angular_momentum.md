# Equations of motion and angular momentum

The general two-body problem becomes especially transparent in polar
coordinates. Its tangential equation exposes angular-momentum conservation and
leads directly to Kepler's equal-area law.

## Equations of motion in polar coordinates

The full orbital problem is most naturally written in plane polar coordinates $(r,\theta)$.

The acceleration vector is

$$
\boxed{
\mathbf a
=
\left(
\ddot r-r\dot\theta^2
\right)\mathbf e_r
+
\left(
r\ddot\theta+2\dot r\dot\theta
\right)\mathbf e_\theta
}
$$

Gravity is purely radial:

$$
\mathbf a
=
-\frac{\mu}{r^2}\mathbf e_r.
$$

Therefore the radial and tangential equations are

$$
\boxed{
\ddot r-r\dot\theta^2
=
-\frac{\mu}{r^2}
}
$$

and

$$
\boxed{
r\ddot\theta+2\dot r\dot\theta=0
}
$$

These two equations contain the complete two-dimensional Newtonian orbital dynamics.

---

## Angular momentum conservation

Start from the tangential equation:

$$
r\ddot\theta+2\dot r\dot\theta=0.
$$

Multiply by $r$:

$$
r^2\ddot\theta
+
2r\dot r\dot\theta
=
0.
$$

Recognize that

$$
\frac{d}{dt}
\left(
r^2\dot\theta
\right)
=
2r\dot r\dot\theta
+
r^2\ddot\theta.
$$

Therefore,

$$
\frac{d}{dt}
\left(
r^2\dot\theta
\right)
=
0.
$$

Hence,

$$
\boxed{
r^2\dot\theta=h
}
$$

where $h$ is a constant.

This is the specific angular momentum.

The ordinary angular momentum magnitude is

$$
L=mh.
$$

For planar motion,

$$
\boxed{
h=r^2\dot\theta
}
$$

is one of the central invariants of the orbital problem.

---

## Kepler's second law from angular momentum conservation

The area swept by the radius vector in a small time $dt$ is approximately the area of a thin triangle:

$$
dA
=
\frac{1}{2}r^2\,d\theta.
$$

Divide by $dt$:

$$
\frac{dA}{dt}
=
\frac{1}{2}r^2\dot\theta.
$$

Using

$$
r^2\dot\theta=h,
$$

we obtain

$$
\boxed{
\frac{dA}{dt}
=
\frac{h}{2}
=
\mathrm{constant}
}
$$

Therefore equal areas are swept in equal times.

This is exactly Kepler's second law.

The result follows directly from the fact that gravity is a central force.

A central force produces zero torque:

$$
\boldsymbol\tau
=
\mathbf r\times\mathbf F
=
0.
$$

Zero torque implies angular momentum conservation, and angular momentum conservation implies constant areal velocity.

Thus,

$$
\boxed{
\text{central force}
\Rightarrow
\text{zero torque}
\Rightarrow
\text{constant angular momentum}
\Rightarrow
\text{equal areas in equal times}
}
$$

