# Launching the interactive app

Run it from the repository root:

```bash
poetry run python examples/launch_app.py
```

This opens `http://127.0.0.1:8054` in the default browser: place a launcher
around Earth, aim and set its speed, and fire independent projectiles to see
circles, ellipses, parabolas, hyperbolas, and radial trajectories emerge from
different initial conditions in real time. The script itself is a thin wrapper 
around {py:func}`orbitworks.launch_app`