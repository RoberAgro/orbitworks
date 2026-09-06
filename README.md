# OrbitWorks

OrbitWorks is an educational computational laboratory for classical orbital
mechanics. It is designed to keep the governing equations visible and to make
analytical solutions, numerical trajectories, conservation laws, and orbital
geometry easy to compare.

> **Project status:** the interactive Dash app is implemented. The broader
> reusable simulation API and some experiments below remain planned work.

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

Launch the local app and open it in your default browser:

```powershell
poetry run python scripts/launch_app.py
```

The script calls `orbitworks.launch_app(debug=False, open_browser=True)`.
Adjust `DEBUG` and `OPEN_BROWSER` at the top of the script as needed. The app
runs at **http://127.0.0.1:8054**; stop it with Ctrl+C. To start without opening
a browser, use `poetry run python -m orbitworks.app`.

For the current implementation and longer-term plans, see:

- [App development reference](docs/source/notes/app_development.md).
- [Repository roadmap](docs/source/notes/orbitworks_planned_work.md).
- [Orbital-mechanics theory](docs/source/theory/index.md).


## Example experiments

The highest-priority experiments will explore circular and escape velocities,
conic geometry, tangential launch speeds, analytical-versus-numerical orbits,
conservation errors, Kepler's second and third laws, and nondimensional orbit
families.

A particularly useful control is the ratio \(v/v_c\). Varying it at a fixed
starting radius reveals sub-circular and super-circular ellipses, the circular
case at \(v/v_c=1\), and the escape boundary at \(v/v_c=\sqrt{2}\).

## Interactive app

Run the complete test suite with `poetry run python scripts/run_tests.py`.
App releases use `app-vMAJOR.MINOR.PATCH` tags and deploy only after the GitHub
test matrix passes. See the [test and release guide](docs/source/notes/app_releases.md)
for version bumping and the required one-time Render/GitHub setup.

The Dash app in `src/orbitworks/app.py` lets you place and aim a launcher, preview
its path, and fire multiple independent projectiles around Earth. SciPy computes
their trajectories; the browser animates their travelled paths and displays flight
details and energy drift. The interface and styling live in
`src/orbitworks/assets/orbit_scene.js` and `orbitworks.css`.


Or if you installed from source with Poetry:
```bash
poetry run python -c "import orbitworks; orbitworks.launch_app()"
```

## License

OrbitWorks is available under the [MIT License](LICENSE.md).
