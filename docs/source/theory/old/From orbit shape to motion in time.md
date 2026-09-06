## From orbit shape to motion in time

Solving the Newtonian two-body problem in polar coordinates gives the shape of the orbit,

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
p=\frac{\ell^2}{\mu}
}
$$

with

$$
\mu=GM
$$

for a negligible orbiting mass, and

$$
\ell=r^2\dot\theta
$$

the conserved specific angular momentum.

The eccentricity $e$ determines the type of conic:

$$
\boxed{
\begin{aligned}
0\le e<1
&\qquad \text{ellipse},\\
e=1
&\qquad \text{parabola},\\
e>1
&\qquad \text{hyperbola}.
\end{aligned}
}
$$

Thus,

$$
r(\theta)=\frac{p}{1+e\cos\theta}
$$

is not restricted to elliptical orbits. It describes all three Keplerian conics.

However, this equation determines only the **geometry of the orbit**. It tells us the radial distance corresponding to each angular position, but it does not yet tell us when the body reaches that position.

There is therefore an important distinction between

$$
\boxed{
r=r(\theta)
}
$$

and

$$
\boxed{
\mathbf r=\mathbf r(t).
}
$$

The first describes the **shape of the trajectory**. The second describes the **motion along that trajectory in time**.

---

## From orbital position to time

Conservation of specific angular momentum gives

$$
r^2\dot\theta=\ell.
$$

Therefore,

$$
\dot\theta
=
\frac{d\theta}{dt}
=
\frac{\ell}{r^2}.
$$

Inverting,

$$
\boxed{
dt
=
\frac{r^2}{\ell}\,d\theta.
}
$$

This equation provides the bridge between the geometric orbit and its time evolution.

Substituting

$$
r(\theta)
=
\frac{p}{1+e\cos\theta}
$$

gives

$$
dt
=
\frac{p^2}{\ell}
\frac{d\theta}
{(1+e\cos\theta)^2}.
$$

Hence,

$$
\boxed{
t-t_0
=
\frac{p^2}{\ell}
\int_{\theta_0}^{\theta}
\frac{d\vartheta}
{(1+e\cos\vartheta)^2}.
}
$$

This relation applies to elliptical, parabolic, and hyperbolic Keplerian trajectories.

The integral can be evaluated analytically in all three cases. However, the most convenient form of the result depends on the type of conic.

This leads naturally to the introduction of different anomaly variables.

---

## Elliptical orbits: eccentric anomaly

For

$$
0\le e<1,
$$

introduce the **eccentric anomaly** $E$ through

$$
\boxed{
\tan\frac{E}{2}
=
\sqrt{\frac{1-e}{1+e}}
\tan\frac{\theta}{2}.
}
$$

The radial distance becomes

$$
\boxed{
r=a(1-e\cos E),
}
$$

where $a>0$ is the semi-major axis.

The time integral reduces to

$$
\boxed{
t-\tau
=
\sqrt{\frac{a^3}{\mu}}
\left(
E-e\sin E
\right),
}
$$

where $\tau$ is the time of periapsis passage.

Define the mean motion

$$
\boxed{
n=\sqrt{\frac{\mu}{a^3}}
}
$$

and the mean anomaly

$$
M=n(t-\tau).
$$

Then

$$
\boxed{
M=E-e\sin E.
}
$$

This is the **elliptic Kepler equation**.

The relation is exact, but it cannot generally be inverted in elementary functions to obtain $E(t)$. Given a time $t$, one therefore computes $M$ and solves the scalar nonlinear equation

$$
E-e\sin E-M=0
$$

for $E$.

---

## Hyperbolic orbits: hyperbolic anomaly

For

$$
e>1,
$$

the trajectory is hyperbolic.

It is convenient to introduce the **hyperbolic anomaly** $H$. With the usual convention that the hyperbolic semi-major axis satisfies $a<0$, the radial distance can be written as

$$
\boxed{
r=(-a)(e\cosh H-1).
}
$$

The corresponding time relation is

$$
\boxed{
t-\tau
=
\sqrt{\frac{(-a)^3}{\mu}}
\left(
e\sinh H-H
\right).
}
$$

Defining the hyperbolic mean anomaly

$$
M
=
\sqrt{\frac{\mu}{(-a)^3}}
(t-\tau),
$$

gives the **hyperbolic Kepler equation**

$$
\boxed{
M=e\sinh H-H.
}
$$

As in the elliptical case, this relation is exact but generally must be inverted numerically to obtain $H$ for a specified time.

Thus, the same basic structure remains:

$$
t
\longrightarrow
M
\longrightarrow
H
\longrightarrow
\mathbf r,\mathbf v.
$$

---

## Parabolic orbits: Barker's equation

The parabolic case,

$$
e=1,
$$

is special because the orbital energy is exactly zero and the semi-major axis becomes infinite. Consequently, the elliptical and hyperbolic anomaly formulations cannot be used directly.

Instead, define

$$
\boxed{
D=\tan\frac{\theta}{2}.
}
$$

For a parabola,

$$
r
=
\frac{p}{1+\cos\theta}.
$$

Using the half-angle identity

$$
1+\cos\theta
=
\frac{2}{1+D^2},
$$

gives

$$
\boxed{
r
=
\frac{p}{2}(1+D^2).
}
$$

The time integral can then be evaluated explicitly, giving **Barker's equation**:

$$
\boxed{
t-\tau
=
\frac{1}{2}
\sqrt{\frac{p^3}{\mu}}
\left(
D+\frac{D^3}{3}
\right).
}
$$

Thus the parabolic case also has an analytic time relation.

Unlike the elliptic and hyperbolic Kepler equations, Barker's equation is a cubic equation in $D$ and can, in principle, be inverted explicitly. In practice it can also simply be solved numerically.

---

## A common structure for all Keplerian orbits

Although the anomaly variable changes, all three conic types follow the same conceptual sequence:

$$
\boxed{
\text{orbit shape}
\longrightarrow
\text{time relation}
\longrightarrow
\text{anomaly}
\longrightarrow
\mathbf r(t),\mathbf v(t).
}
$$

More specifically,

$$
\begin{array}{c|c|c}
\text{Orbit} & \text{Anomaly} & \text{Time equation}\\
\hline
e<1 & E & M=E-e\sin E\\[4pt]
e=1 & D & 
t-\tau=
\dfrac{1}{2}\sqrt{\dfrac{p^3}{\mu}}
\left(D+\dfrac{D^3}{3}\right)\\[8pt]
e>1 & H & M=e\sinh H-H
\end{array}
$$

Thus, obtaining the geometric orbit and obtaining the time-dependent motion are separate steps for every type of Keplerian trajectory.

---

## From an initial state to the orbit

In practical orbital mechanics, the starting point is often not $a$, $e$, or $\theta$, but an initial Cartesian state

$$
\boxed{
\mathbf r_0,\qquad \mathbf v_0
}
$$

specified at some time $t_0$.

The goal is to determine

$$
\boxed{
\mathbf r(t),\qquad \mathbf v(t)
}
$$

at a later or earlier time.

The first step is to determine which Keplerian orbit is defined by the initial state.

### 1. Compute the specific angular momentum

The specific angular momentum vector is

$$
\boxed{
\mathbf h
=
\mathbf r_0\times\mathbf v_0.
}
$$

Its magnitude is

$$
h=|\mathbf h|.
$$

This is the same conserved quantity denoted by $\ell$ in the planar derivation:

$$
\ell=h.
$$

The orbital plane is perpendicular to $\mathbf h$.

The semi-latus rectum follows immediately:

$$
\boxed{
p=\frac{h^2}{\mu}.
}
$$

### 2. Compute the specific orbital energy

The specific mechanical energy is

$$
\boxed{
\varepsilon
=
\frac{v_0^2}{2}
-
\frac{\mu}{r_0}.
}
$$

Its sign immediately classifies the orbit:

$$
\boxed{
\begin{aligned}
\varepsilon<0
&\quad\Rightarrow\quad
\text{ellipse},\\
\varepsilon=0
&\quad\Rightarrow\quad
\text{parabola},\\
\varepsilon>0
&\quad\Rightarrow\quad
\text{hyperbola}.
\end{aligned}
}
$$

For non-parabolic orbits,

$$
\boxed{
a=-\frac{\mu}{2\varepsilon}.
}
$$

Thus,

- an ellipse has $a>0$;
- a hyperbola has $a<0$;
- a parabola has no finite semi-major axis.

### 3. Compute the eccentricity vector

Define the eccentricity vector

$$
\boxed{
\mathbf e
=
\frac{\mathbf v_0\times\mathbf h}{\mu}
-
\frac{\mathbf r_0}{r_0}.
}
$$

Its magnitude gives the orbital eccentricity,

$$
\boxed{
e=|\mathbf e|.
}
$$

The vector $\mathbf e$ points toward periapsis.

This determines both the shape and the orientation of the conic within the orbital plane.

At this point, the initial state has determined the complete geometric orbit.

---

## Determine the initial position on the orbit

The next step is to determine where the body lies on that conic at $t_0$.

The true anomaly $\theta_0$ is the angle from the eccentricity vector to the initial position vector.

Its cosine is

$$
\cos\theta_0
=
\frac{\mathbf e\cdot\mathbf r_0}
{e\,r_0}.
$$

The sign of the radial velocity,

$$
\dot r_0
=
\frac{\mathbf r_0\cdot\mathbf v_0}{r_0},
$$

distinguishes the outgoing and incoming branches.

For robust numerical implementations, the quadrant of $\theta_0$ should be determined using an $\operatorname{atan2}$ formulation rather than $\arccos$ alone.

Once $\theta_0$ is known, it is converted into the appropriate anomaly for the orbit type.

---

## Propagating an elliptical orbit

For

$$
e<1,
$$

convert the initial true anomaly $\theta_0$ into the initial eccentric anomaly $E_0$.

A convenient relation is

$$
\tan\frac{E_0}{2}
=
\sqrt{\frac{1-e}{1+e}}
\tan\frac{\theta_0}{2}.
$$

Then calculate the initial mean anomaly,

$$
\boxed{
M_0
=
E_0-e\sin E_0.
}
$$

The mean anomaly evolves linearly with time:

$$
\boxed{
M(t)
=
M_0+n(t-t_0),
}
$$

where

$$
n=\sqrt{\frac{\mu}{a^3}}.
$$

At the desired time $t$, solve

$$
\boxed{
E-e\sin E=M(t)
}
$$

for $E$.

Once $E$ is known, the radial distance is

$$
r=a(1-e\cos E),
$$

and the true anomaly follows from

$$
\tan\frac{\theta}{2}
=
\sqrt{\frac{1+e}{1-e}}
\tan\frac{E}{2}.
$$

The position and velocity can then be reconstructed.

---

## Propagating a hyperbolic orbit

For

$$
e>1,
$$

determine the initial hyperbolic anomaly $H_0$ from the initial orbital position.

Then calculate

$$
\boxed{
M_0
=
e\sinh H_0-H_0.
}
$$

The hyperbolic mean anomaly evolves as

$$
\boxed{
M(t)
=
M_0
+
\sqrt{\frac{\mu}{(-a)^3}}
(t-t_0).
}
$$

At the desired time, solve

$$
\boxed{
e\sinh H-H=M(t)
}
$$

for $H$.

The resulting $H$ determines the radius and true anomaly, from which position and velocity follow.

---

## Propagating a parabolic orbit

For

$$
e=1,
$$

define

$$
D=\tan\frac{\theta}{2}.
$$

At the initial time,

$$
D_0=\tan\frac{\theta_0}{2}.
$$

Barker's equation gives

$$
t-\tau
=
\frac{1}{2}
\sqrt{\frac{p^3}{\mu}}
\left(
D+\frac{D^3}{3}
\right).
$$

Rather than explicitly determining $\tau$, one can subtract the initial relation from the final relation:

$$
\boxed{
t-t_0
=
\frac{1}{2}
\sqrt{\frac{p^3}{\mu}}
\left[
D+\frac{D^3}{3}
-
D_0-\frac{D_0^3}{3}
\right].
}
$$

Given $t-t_0$, this equation determines $D$, and hence

$$
\theta=2\tan^{-1}D.
$$

The radius then follows from

$$
r
=
\frac{p}{1+\cos\theta}.
$$

---

## Recovering position and velocity

Once $r$ and $\theta$ are known, the position in the orbital plane is

$$
\boxed{
\mathbf r
=
r\,\mathbf e_r.
}
$$

The velocity is

$$
\mathbf v
=
\dot r\,\mathbf e_r
+
r\dot\theta\,\mathbf e_\theta.
$$

For any Keplerian conic,

$$
\boxed{
\dot r
=
\frac{\mu}{h}e\sin\theta
}
$$

and

$$
\boxed{
r\dot\theta
=
\frac{\mu}{h}
(1+e\cos\theta).
}
$$

Therefore,

$$
\boxed{
\mathbf v
=
\frac{\mu}{h}
\left[
e\sin\theta\,\mathbf e_r
+
(1+e\cos\theta)\mathbf e_\theta
\right].
}
$$

These expressions apply to elliptical, parabolic, and hyperbolic trajectories.

To return to the original three-dimensional Cartesian coordinate system, the orbital-plane vectors are rotated according to the orientation of the orbital plane determined from the initial state.

---

## Complete state-propagation algorithm

The complete two-body propagation procedure can therefore be summarized as

$$
\boxed{
(\mathbf r_0,\mathbf v_0,t_0)
\longrightarrow
(\mathbf r(t),\mathbf v(t)).
}
$$

Starting from the initial state:

1. Compute the specific angular momentum,

   $$
   \mathbf h=\mathbf r_0\times\mathbf v_0.
   $$

2. Compute the specific orbital energy,

   $$
   \varepsilon
   =
   \frac{v_0^2}{2}
   -
   \frac{\mu}{r_0}.
   $$

3. Compute the eccentricity vector,

   $$
   \mathbf e
   =
   \frac{\mathbf v_0\times\mathbf h}{\mu}
   -
   \frac{\mathbf r_0}{r_0}.
   $$

4. Determine

   $$
   e=|\mathbf e|,
   \qquad
   p=\frac{h^2}{\mu},
   $$

   and, when $\varepsilon\ne0$,

   $$
   a=-\frac{\mu}{2\varepsilon}.
   $$

5. Classify the orbit:

   $$
   e<1,\qquad e=1,\qquad e>1.
   $$

6. Determine the initial true anomaly $\theta_0$ from $\mathbf r_0$ and $\mathbf e$.

7. Convert $\theta_0$ to the anomaly appropriate for the conic:

   $$
   \begin{aligned}
   e<1 &: \quad E_0,\\
   e=1 &: \quad D_0,\\
   e>1 &: \quad H_0.
   \end{aligned}
   $$

8. Advance the corresponding time equation from $t_0$ to the desired time $t$.

9. Solve the resulting scalar equation for the new anomaly.

10. Recover $r$, $\theta$, and finally

    $$
    \boxed{
    \mathbf r(t),\mathbf v(t).
    }
    $$

Thus, the ideal Newtonian two-body problem does **not** fundamentally require numerical integration of the differential equations of motion.

The dynamics have already been solved analytically. Propagation reduces to advancing an anomaly through an exact time relation and, for elliptical and hyperbolic motion, numerically solving a single scalar transcendental equation.

---

## The central distinction

It is useful to keep three different ideas separate.

First, solving

$$
\boxed{
r(\theta)
=
\frac{p}{1+e\cos\theta}
}
$$

determines the **geometric orbit**. It tells us the curve followed by the body, but not the rate at which the body moves along it.

Second, angular-momentum conservation,

$$
\boxed{
r^2\dot\theta=h,
}
$$

introduces time and determines how quickly the orbit is traversed.

Third, integrating this relation produces an exact time-of-flight equation. Its most convenient form depends on the conic:

$$
\boxed{
\begin{array}{c|c}
\text{Orbit} & \text{Time relation}\\
\hline
\text{ellipse} &
M=E-e\sin E\\[4pt]
\text{parabola} &
t-\tau=
\dfrac{1}{2}
\sqrt{\dfrac{p^3}{\mu}}
\left(D+\dfrac{D^3}{3}\right)\\[10pt]
\text{hyperbola} &
M=e\sinh H-H
\end{array}
}
$$

Consequently, the progression from Newton's equation to a propagated state is

$$
\boxed{
\text{equations of motion}
\longrightarrow
\text{conic shape}
\longrightarrow
\text{time-of-flight relation}
\longrightarrow
\text{anomaly at }t
\longrightarrow
\mathbf r(t),\mathbf v(t).
}
$$

The orbit shape is therefore analytic, and the time evolution is also governed by exact analytic relations. What is generally unavailable for elliptical and hyperbolic motion is an **elementary explicit inverse** giving the anomaly directly as a function of time.

That distinction explains why Keplerian orbit propagation normally requires a small numerical root solve, but not numerical integration of the original equations of motion.