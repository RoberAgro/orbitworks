# OrbitWorks

OrbitWorks explores classical orbital mechanics, letting you place, launch,
and track objects in orbit around a planet.


## Documentation and live app

- **Documentation:** <https://roberagro.github.io/orbitworks/>
- **Live app:** <https://orbitworks-xxh2.onrender.com/>

## Installation

OrbitWorks uses [Poetry](https://python-poetry.org/) for dependency and package management.

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

Launch the app locally and open it in your default browser:

```bash
poetry run python examples/launch_app.py
```

The app runs at **http://127.0.0.1:8054**; stop it with Ctrl+C. Place the
launcher, aim and set its speed, and launch! Existing projectiles keep moving
while a new one is computed, so you can visualize several trajectories.

## License

OrbitWorks is available under the [MIT License](LICENSE.md).
