# Kepler's laws and synthesis

Kepler's three empirical laws — the shape of planetary orbits, the constancy
of areal velocity, and the relation between period and size — are
consequences of Newton's law together with the results derived so far. This
chapter states the first two explicitly, derives the third, and closes the
guide with its complete logical chain and a formula reference.

## Kepler's first law

The orbital equation

$$
r(\theta)=\frac{p}{1+e\cos\theta}
$$

is a conic with the central mass at one focus (chapter 5). Bound planetary
motion has $\varepsilon<0$, which forces $0\le e<1$ (chapter 7). Together,

$$
\boxed{
\text{bound planets move in ellipses with the Sun at one focus}
}
$$

with the circular orbit as the special case $e=0$.

## Kepler's second law

Zero torque from a central force conserves angular momentum,
$\ell=r^2\dot\theta$ (chapter 4), giving

$$
\boxed{
\frac{dA}{dt}=\frac{\ell}{2}=\text{constant}.
}
$$

Equal areas are swept in equal times. Nothing new is needed here; it is
restated for completeness of the three-laws list.

## Kepler's third law

For an ellipse with semi-major axis $a$ and semi-minor axis $b$, the total
enclosed area is $A=\pi ab$. By the second law, $dA/dt=\ell/2$ is constant, so
over one complete period $T$ the whole ellipse is swept out:

$$
\pi ab=\frac{\ell}{2}T
\quad\Longrightarrow\quad
T=\frac{2\pi ab}{\ell}.
$$

With $b=a\sqrt{1-e^2}$ and $p=a(1-e^2)=\ell^2/GM$ (chapter 5),
$\ell^2=GMa(1-e^2)$ and $\ell=\sqrt{GMa(1-e^2)}$. Substituting,

$$
T=\frac{2\pi a^2\sqrt{1-e^2}}{\sqrt{GMa(1-e^2)}}
=\frac{2\pi a^2}{\sqrt{GMa}}
=2\pi\frac{a^{3/2}}{\sqrt{GM}}.
$$

Therefore

$$
\boxed{
T=2\pi\sqrt{\frac{a^3}{GM}}
},
\qquad
\boxed{
T^2=\frac{4\pi^2}{GM}a^3.
}
$$

The eccentricity cancels completely: orbital period depends only on the
semi-major axis, not on the shape of the ellipse.

## Why the mathematics is so compact

$$
\boxed{
\text{inverse-square gravity}
\;\rightarrow\;
\text{central force}
\;\rightarrow\;
\text{angular momentum conservation}
\;\rightarrow\;
\text{constant areal velocity (2nd law)}
}
$$

The inverse-square form is also what makes the reciprocal-radius substitution
$u=1/r$ turn the orbital equation linear,

$$
u''+u=\text{constant}
\quad\Longrightarrow\quad
r=\frac{p}{1+e\cos\theta},
$$

and what supplies the extra conserved eccentricity vector, which pins the
orbit's orientation in place. Negative energy makes that conic an ellipse
(1st law), and combining the ellipse's geometry with constant areal velocity
gives $T^2\propto a^3$ (3rd law). The three empirical laws are not
independent postulates: they are consequences of one force law together with
Newton's laws of motion.

## Summary of central results

Newtonian gravity and acceleration:

$$
\boxed{
\mathbf F=-\frac{GMm}{r^2}\mathbf e_r
},
\qquad
\boxed{
\mathbf a=-\frac{GM}{r^2}\mathbf e_r
}
$$

Circular and escape speed:

$$
\boxed{
v_c=\sqrt{\frac{GM}{r}}
},
\qquad
\boxed{
v_{\mathrm{esc}}=\sqrt{\frac{2GM}{r}}=\sqrt2\,v_c
}
$$

Specific angular momentum and areal velocity:

$$
\boxed{
\boldsymbol\ell=\mathbf r\times\mathbf v
},
\qquad
\boxed{
\frac{dA}{dt}=\frac{\ell}{2}
}
$$

Specific energy and effective potential:

$$
\boxed{
\varepsilon=\frac{v^2}{2}-\frac{GM}{r}
},
\qquad
\boxed{
V_{\mathrm{eff}}(r)=\frac{\ell^2}{2r^2}-\frac{GM}{r}
}
$$

Binet equation and conic orbit:

$$
\boxed{
u''+u=\frac{GM}{\ell^2}
},
\qquad
\boxed{
r(\theta)=\frac{p}{1+e\cos\theta}
}
$$

Eccentricity vector:

$$
\boxed{
\mathbf e=\frac{\mathbf v\times\boldsymbol\ell}{GM}-\mathbf e_r
}
$$

Semi-latus rectum, periapsis, apoapsis:

$$
\boxed{
p=\frac{\ell^2}{GM}=a(1-e^2)
},
\qquad
\boxed{
r_p=a(1-e)
},
\qquad
\boxed{
r_a=a(1+e)
}
$$

Vis-viva and the energy of an ellipse:

$$
\boxed{
v^2=GM\left(\frac{2}{r}-\frac{1}{a}\right)
},
\qquad
\boxed{
\varepsilon=-\frac{GM}{2a}
}
$$

Eccentricity from energy and angular momentum, and from tangential launch:

$$
\boxed{
e^2=1+\frac{2\varepsilon\ell^2}{(GM)^2}
},
\qquad
\boxed{
e=\frac{v^2}{v_c^2}-1
}
$$

Kepler's third law:

$$
\boxed{
T^2=\frac{4\pi^2}{GM}a^3
}
$$

Classification, equivalently by shape or by energy:

$$
\boxed{
\begin{array}{ccl}
e=0 &:& \text{circle}\\
0<e<1 &:& \text{ellipse}\\
e=1 &:& \text{parabola}\\
e>1 &:& \text{hyperbola}
\end{array}
}
\qquad
\boxed{
\begin{array}{ccl}
\varepsilon<0 &:& \text{bound ellipse}\\
\varepsilon=0 &:& \text{parabolic escape}\\
\varepsilon>0 &:& \text{hyperbolic escape}
\end{array}
}
$$

The complete conceptual chain:

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
}
$$

With the orbit's shape, its governing conserved quantities, and its complete
geometric parameterization now established, the final step is to locate the
body along the orbit as a function of time — the subject of the next chapter.
