# Equations of motion and angular momentum

The general two-body problem becomes especially transparent in polar
coordinates. Its tangential equation exposes angular-momentum conservation and
leads directly to Kepler's equal-area law.

(polar-coordinate-acceleration)=
## Derivation of acceleration in polar coordinates

In Cartesian coordinates, the coordinate directions are fixed. In polar
coordinates, however, the radial and tangential unit vectors rotate as the
object moves. Their changing directions must therefore be included when the
position vector is differentiated.

The polar unit vectors can be written in terms of fixed Cartesian unit vectors
as

$$
\mathbf e_r
=
\cos\theta\,\mathbf e_x
+
\sin\theta\,\mathbf e_y
$$

and

$$
\mathbf e_\theta
=
-\sin\theta\,\mathbf e_x
+
\cos\theta\,\mathbf e_y.
$$

Differentiating them with respect to time gives

$$
\dot{\mathbf e}_r
=
\dot\theta\,\mathbf e_\theta
$$

and

$$
\dot{\mathbf e}_\theta
=
-\dot\theta\,\mathbf e_r.
$$

The position vector is

$$
\mathbf r=r\,\mathbf e_r.
$$

Using the product rule, the velocity is therefore

$$
\mathbf v
=
\frac{d}{dt}\left(r\,\mathbf e_r\right)
=
\dot r\,\mathbf e_r
+
r\dot\theta\,\mathbf e_\theta.
$$

Differentiate once more:

$$
\begin{aligned}
\mathbf a
&=
\frac{d}{dt}
\left(
\dot r\,\mathbf e_r
+
r\dot\theta\,\mathbf e_\theta
\right) \\
&=
\ddot r\,\mathbf e_r
+
\dot r\,\dot{\mathbf e}_r
+
\left(\dot r\dot\theta+r\ddot\theta\right)\mathbf e_\theta
+
r\dot\theta\,\dot{\mathbf e}_\theta.
\end{aligned}
$$

Substituting the derivatives of the unit vectors,

$$
\begin{aligned}
\mathbf a
&=
\ddot r\,\mathbf e_r
+
\dot r\dot\theta\,\mathbf e_\theta
+
\left(\dot r\dot\theta+r\ddot\theta\right)\mathbf e_\theta
-
r\dot\theta^2\,\mathbf e_r \\
&=
\left(\ddot r-r\dot\theta^2\right)\mathbf e_r
+
\left(r\ddot\theta+2\dot r\dot\theta\right)\mathbf e_\theta.
\end{aligned}
$$
Thus,

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

or, separating the individual contributions:

$$
\boxed{
\mathbf a
=
\underbrace{\ddot r\,\mathbf e_r}_{\text{radial acceleration}}
-
\underbrace{r\dot\theta^2\,\mathbf e_r}_{\text{centripetal acceleration}}
+
\underbrace{r\ddot\theta\,\mathbf e_\theta}_{\text{angular acceleration}}
+
\underbrace{2\dot r\dot\theta\,\mathbf e_\theta}_{\text{Coriolis-like acceleration}}
}
$$

Each term has a distinct kinematic origin.

* **Radial acceleration, $\ddot r\mathbf e_r$.**
  This term represents the acceleration associated with a change in the radial velocity $\dot r$. It is present when the object accelerates toward or away from the origin.

* **Centripetal acceleration, $-r\dot\theta^2\mathbf e_r$.**
  Even if $r$ and $\dot\theta$ are constant, the direction of the tangential velocity continuously changes as the object moves around the origin. This produces an inward radial acceleration. Since the tangential speed is $v_\theta=r\dot\theta$, the term can also be written as

  $$
  -r\dot\theta^2\,\mathbf e_r
  =
  -\frac{v_\theta^2}{r}\,\mathbf e_r.
  $$

  For uniform circular motion, this is the entire acceleration.

* **Angular acceleration, $r\ddot\theta\mathbf e_\theta$.**
  This term represents the tangential acceleration caused by a change in angular velocity. At fixed radius, increasing or decreasing $\dot\theta$ changes the tangential speed $r\dot\theta$, producing an acceleration in the $\mathbf e_\theta$ direction.

* **Coriolis-like acceleration, $2\dot r\dot\theta,\mathbf e_\theta$.**
  This term appears when radial and angular motion occur simultaneously. If the object moves radially while also rotating about the origin, its tangential velocity $r\dot\theta$ changes simply because $r$ changes. In addition, the radial velocity vector itself changes direction because the polar basis rotates. These two effects each contribute $\dot r\dot\theta\mathbf e_\theta$, giving the factor of two:

  $$
  \dot r\dot\theta\,\mathbf e_\theta
  +
  \dot r\dot\theta\,\mathbf e_\theta
  =
  2\dot r\dot\theta\,\mathbf e_\theta.
  $$

The last term has the same mathematical structure as the Coriolis acceleration encountered in rotating reference frames. Here, however, it arises directly from differentiating the position vector in a rotating polar basis, so it is more precise to regard it as a **Coriolis-like kinematic term** rather than a fictitious force.

An important point is that the radial and tangential components of acceleration are therefore not simply $\ddot r$ and $r\ddot\theta$. Because the basis vectors $\mathbf e_r$ and $\mathbf e_\theta$ themselves rotate as $\theta$ changes, additional acceleration terms appear even when the corresponding coordinate rates are constant.

---

## Equations of motion in polar coordinates

The full orbital problem is most naturally written in plane polar coordinates $(r,\theta)$.

Using the result derived in {ref}`polar-coordinate-acceleration`, the
acceleration vector is

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
-\frac{GM}{r^2}\mathbf e_r.
$$

Therefore the radial and tangential equations are

$$
\boxed{
\ddot r-r\dot\theta^2
=
-\frac{GM}{r^2}
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

Thus, $r^2\dot\theta$ is constant. To identify this conserved quantity,
start from the vector definition of angular momentum,

$$
\boxed{
\mathbf L
=
m\,\mathbf r\times\mathbf v
}.
$$

In polar coordinates,

$$
\mathbf r=r\,\mathbf e_r
$$

and

$$
\mathbf v
=
\dot r\,\mathbf e_r
+
r\dot\theta\,\mathbf e_\theta.
$$

Substituting these expressions into the cross product gives

$$
\begin{aligned}
\mathbf L
&=
m\left(r\,\mathbf e_r\right)
\times
\left(
\dot r\,\mathbf e_r
+
r\dot\theta\,\mathbf e_\theta
\right) \\
&=
m r\dot r
\left(\mathbf e_r\times\mathbf e_r\right)
+
m r^2\dot\theta
\left(\mathbf e_r\times\mathbf e_\theta\right).
\end{aligned}
$$

Since a vector crossed with itself is zero and
$\mathbf e_r\times\mathbf e_\theta=\mathbf e_z$,

$$
\boxed{
\mathbf L
=
m r^2\dot\theta\,\mathbf e_z
}.
$$

The angular momentum is perpendicular to the orbital plane. Dividing by the
mass defines the **specific angular momentum vector**,

$$
\boldsymbol{\ell}
=
\frac{\mathbf L}{m}
=
\mathbf r\times\mathbf v
=
r^2\dot\theta\,\mathbf e_z.
$$

For planar motion, we denote its constant $z$-component by $\ell$:

$$
\boxed{
\ell=r^2\dot\theta
}.
$$

The corresponding angular-momentum magnitude is

$$
L=m\ell.
$$

Thus, $\ell$ is one of the central invariants of the orbital problem.

---

## Kepler's second law from angular momentum conservation

At time $t$, the orbiting body has position vector $\mathbf r(t)$. After a
short interval $\Delta t$, its position vector is $\mathbf r(t+\Delta t)$.
Together with the central body at the origin, these two vectors form a
triangle whose **vector area** is

$$
\boxed{
\Delta\mathbf A_{\triangle}
=
\frac{1}{2}
\mathbf r(t)\times\mathbf r(t+\Delta t)
}.
$$

This formula follows from the geometry of the cross product. For any two
vectors $\mathbf a$ and $\mathbf b$,

$$
\left|\mathbf a\times\mathbf b\right|
=
|\mathbf a|\,|\mathbf b|\sin\phi,
$$

where $\phi$ is the angle between them. This is the area of the parallelogram
spanned by the two vectors, so half of the cross product gives the area of the
corresponding triangle. Its direction is perpendicular to the orbital plane,
with its sign determined by the right-hand rule.

The body's actual path during $\Delta t$ is curved, so the swept area is not
exactly triangular for a finite interval. The difference vanishes relative to
the leading term as $\Delta t\rightarrow0$. To take this limit, write

$$
\mathbf r(t+\Delta t)
=
\mathbf r(t)+\Delta\mathbf r.
$$

Then

$$
\begin{aligned}
\Delta\mathbf A_{\triangle}
&=
\frac{1}{2}\mathbf r(t)
\times
\left[\mathbf r(t)+\Delta\mathbf r\right] \\
&=
\frac{1}{2}\mathbf r(t)\times\Delta\mathbf r,
\end{aligned}
$$

because $\mathbf r\times\mathbf r=0$. Dividing by $\Delta t$ and taking the
limit gives

$$
\begin{aligned}
\frac{d\mathbf A}{dt}
&=
\lim_{\Delta t\to0}
\frac{\Delta\mathbf A_{\triangle}}{\Delta t} \\
&=
\frac{1}{2}\mathbf r\times
\lim_{\Delta t\to0}\frac{\Delta\mathbf r}{\Delta t} \\
&=
\frac{1}{2}\mathbf r\times\mathbf v.
\end{aligned}
$$

Since the specific angular momentum vector is
$\boldsymbol{\ell}=\mathbf r\times\mathbf v$,

$$
\boxed{
\frac{d\mathbf A}{dt}
=
\frac{\boldsymbol{\ell}}{2}
}.
$$

The same result can be expressed in polar coordinates. For a small angular
displacement $d\theta$, the two position vectors have approximately equal
length $r$, and $\sin(d\theta)\approx d\theta$. The scalar swept area is
therefore

$$
dA
=
\frac{1}{2}r^2\,d\theta.
$$

Dividing by $dt$ gives

$$
\frac{dA}{dt}
=
\frac{1}{2}r^2\dot\theta.
$$

Using $r^2\dot\theta=\ell$, we obtain

$$
\boxed{
\frac{dA}{dt}
=
\frac{\ell}{2}
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
\begin{gathered}
\text{central force} \\
\Downarrow \\
\text{zero torque} \\
\Downarrow \\
\text{constant angular momentum} \\
\Downarrow \\
\text{equal areas in equal times}
\end{gathered}
}
$$

