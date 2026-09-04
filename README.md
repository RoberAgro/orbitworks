# OrbitWorks

OrbitWorks is an educational computational laboratory for classical orbital
mechanics. It is designed to keep the governing equations visible and to make
analytical solutions, numerical trajectories, conservation laws, and orbital
geometry easy to compare.

> **Project status:** the repository structure is currently being established.
> The modules and experiments described below are placeholders and do not yet
> provide a working simulation API.

## Purpose

The project follows a progression from Newtonian gravity through circular
motion, energy and angular momentum, conic sections, Kepler's laws, numerical
integration, and eventually multi-body dynamics. 

OrbitWorks is a learning and experimentation project, not a high-fidelity
orbital mechanics package.

## Physics covered

The planned first release covers:

- gravitational, circular-orbit, and escape-velocity relations;
- analytical conic sections and orbit classification;
- specific energy, angular momentum, and eccentricity vectors;
- conversion from Cartesian states to orbital elements;
- two- and three-dimensional two-body propagation;
- analytical-versus-numerical trajectory comparisons;
- numerical verification of Kepler's laws;
- nondimensional orbital mechanics; and
- conservation and integrator-error diagnostics.

Later work may add exact two-body center-of-mass motion, N-body systems,
orbital transfers, perturbations, and restricted three-body dynamics.


## Installation

OrbitWorks requires Python 3.11 through 3.14 and uses
[Poetry](https://python-poetry.org/) for dependency and package management.

**From source (Poetry):**

Clone the repository and let Poetry create the environment and install the
project dependencies:

```bash
git clone https://github.com/RoberAgro/orbitworks.git
cd orbitworks
poetry install
```

Verify that the package can be imported from the Poetry environment:

```bash
poetry run python -c "import orbitworks"
```


## Quick start

There is not yet an executable public API. Development will begin with the
small algebraic functions in `src/orbitworks/analytical.py`, followed by the
tests and focused scripts listed in the implementation roadmap.

The two documents that currently define the project are:

- [`newtonian_gravity_orbits_kepler.md`](newtonian_gravity_orbits_kepler.md),
  the detailed mathematical derivation; and
- [`orbitworks_repository_spec.md`](orbitworks_repository_spec.md),
  the architecture and implementation roadmap.


## Example experiments

The highest-priority experiments will explore circular and escape velocities,
conic geometry, tangential launch speeds, analytical-versus-numerical orbits,
conservation errors, Kepler's second and third laws, and nondimensional orbit
families.

A particularly useful control is the ratio \(v/v_c\). Varying it at a fixed
starting radius reveals sub-circular and super-circular ellipses, the circular
case at \(v/v_c=1\), and the escape boundary at \(v/v_c=\sqrt{2}\).

## Interactive app

The planned Streamlit app will expose initial conditions and solver settings,
then display the resulting orbit, classification, orbital elements,
analytical overlay, and conservation diagnostics. The app will remain a thin
interactive layer over the reusable package.


## License

OrbitWorks is available under the [MIT License](LICENSE.md).
