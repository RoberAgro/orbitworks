# OrbitWorks app: functionality and development decisions

## Overview and organization

OrbitWorks is an interactive orbital-mechanics app for experimenting with a
projectile launched around Earth. Place the launcher, choose a direction and
speed, inspect the predicted path, and launch independent projectiles. The app
shows how circles, ellipses, parabolas, hyperbolas and radial trajectories arise
from different initial conditions, including paths that collide with Earth.

The interface has three areas: launch controls on the left, an interactive
scene in the centre, and a scrollable **Flights log** on the right. The guiding
idea is direct experimentation: **“Place it, aim it, and let gravity take over!”**

This document records the implemented application, rather than a task list.
The current implementation in `src/orbitworks/` takes precedence over historical
READMEs and review checklists.

| Location, relative to the repository root | Responsibility |
| --- | --- |
| `src/orbitworks/app.py` | Physical model, initial conditions, SciPy integration, Dash layout, launch callback and health endpoint |
| `src/orbitworks/assets/orbit_scene.js` | Launch-state synchronization, geometric preview, animation, camera, interactions and flight cards |
| `src/orbitworks/assets/orbitworks.css` | Layout, typography, controls, Help dialog and status styling |
| `src/orbitworks/constants.py` | Shared physical constants, including Earth's radius and gravitational parameter |
| `render.yaml` | Render deployment configuration using Gunicorn and `orbitworks.app:server` |
| `src/orbitworks/__init__.py` | Lazy-imported `launch_app()` helper for local development |
| `scripts/launch_app.py` | Simple local entry point with browser and debug settings at the top |
| `tests/test_orbitworks_app.py` | Physical regression checks against the current packaged app |
| `tests/test_orbitworks_interactions.py` | Layout, callback, asset, health, shortcut-source and launcher checks |

Run the current app from the repository root:

```bash
poetry install
poetry run python scripts/launch_app.py
```

The script opens `http://127.0.0.1:8054` in the default browser. Stop the local
server with Ctrl+C. Its `DEBUG` and `OPEN_BROWSER` settings are at the top of
the script. The equivalent Python interface is:

```python
from orbitworks import launch_app

launch_app(debug=False, open_browser=True)
```

Imports are deferred until the helper is called, so importing `orbitworks`
does not start the server or load Dash. Browser opening uses a one-second
daemon timer, cancelled if the server exits or fails to start. In debug mode,
only the reloader's serving process opens a tab, not its supervisor. A reload
starts a new serving process and can open another tab; use `open_browser=False`
to avoid that. The timer is a convenience delay, not a server-readiness check.

`poetry run python -m orbitworks.app` remains available without automatically
opening a browser. The local entry point binds to `127.0.0.1` with debugging
disabled by default; the deployment configuration
uses Gunicorn instead of the development server. A deployment configuration is
present, but this document does not assert that a hosted instance is available.

## 1. Physical model and initial conditions

For the shared test runner, synchronized package/docs version and tag-gated
Render deployment workflow, see [Testing and releasing the app](app_releases.md).
The release configuration replaces the original commit-triggered deployment;
the Render dashboard setup in that guide must also be applied.

- Earth is stationary and spherical. The motion is two-dimensional, with the
  centre of Earth at the origin.
- Each projectile is an independent point particle. There is no atmosphere,
  Earth rotation, force from the Sun or Moon, interaction between projectiles,
  or collision between projectiles. Projectile mass cancels from acceleration.
- Earth has a finite collision radius even though the exterior gravitational
  field is represented by a central point mass. A conic can intersect Earth;
  classifying it as elliptical or hyperbolic does not rule out impact.
- Horizontal and vertical launch positions are measured in Earth radii.
- Launch speed is entered as a ratio to the local circular speed,
  $v_c=\sqrt{GM/r_0}$. Moving the launcher preserves this ratio, not the speed in
  km/s. The actual speed is displayed next to the speed control.
- Ratio 1 produces a circle only with tangential aim. Ratio $\sqrt{2}$ is the
  local escape speed; a direction towards Earth can still produce an impact.
- Launch angle is measured **counterclockwise from the fixed positive x-axis**:
  0 degrees points right, 90 degrees up and -90 degrees down. Moving the
  launcher preserves this screen-based direction. The backend, arrow and
  preview all use the same convention.

The initial velocity is therefore

$$
\mathbf v_0 = q\sqrt{\frac{GM}{r_0}}
\begin{pmatrix}\cos\alpha\\\sin\alpha\end{pmatrix},
$$

where $q$ is the entered speed ratio and $\alpha$ is the launch angle.

## 2. What runs where: Python vs JavaScript

Two independent code paths compute orbital geometry from the same physics;
neither is a stand-in for the other. This section is the map; §3 and §5 give
the full detail behind the Python and JavaScript rows below.

| Computation | Where | Notes |
| --- | --- | --- |
| Time integration of the equations of motion | Python, `solve_ivp` (§3) | The only place a trajectory is advanced through time; SciPy's adaptive DOP853 solver. |
| Stopping-condition detection (impact, distance boundary, periapsis turn) and grazing-impact root refinement | Python, `impact_event`, `outer_event`, `periapsis_event`, `brentq` (§3) | Runs alongside and after the integration above. |
| Orbital elements from the initial state — energy, angular momentum, eccentricity vector, orbit type, periapsis/apoapsis, period | Computed **independently in both** Python (`compute_positioned_flight`) and JavaScript (`preview`) | The same closed-form formulas are evaluated twice: once server-side for the launched flight's metadata, once client-side for the live preview. Neither call reuses the other's result. |
| Numerical energy-drift diagnostic | Python | Recomputed at every returned sample; see §4. |
| Live geometric preview path, before firing | JavaScript, `preview()` | Samples the conic $r=p/(1+e\cos\theta)$ directly and locates the surface/boundary crossing analytically (via `acos`); it does not integrate anything. See §5. |
| Smooth on-screen motion between returned samples | JavaScript, `sample()` | Cubic Hermite interpolation of the positions/velocities Python already computed; no new physics. See §7. |
| Camera, drawing, controls, clock, connection heartbeat | JavaScript | UI state and rendering only; consumes numbers computed elsewhere. |

The dividing line is time integration: Python is the only code that ever
advances the ODE. JavaScript recomputes the same orbital-element algebra from
scratch for its live preview — so dragging the launcher updates instantly,
without a server round trip — and otherwise only interpolates and renders the
samples the server already produced.

## 3. Numerical integration and stopping conditions

The server integrates the Cartesian initial-value problem

$$
\frac{d\mathbf r}{dt}=\mathbf v,
\qquad
\frac{d\mathbf v}{dt}=-\frac{GM}{r^3}\mathbf r.
$$

- **Scaling:** length is scaled by Earth's radius $R$, time by
  $\sqrt{R^3/(GM)}$, and speed by $\sqrt{GM/R}$. This makes the gravitational
  parameter equal to 1 in the integration equations.
- **Solver:** SciPy `solve_ivp` with adaptive DOP853, relative tolerance
  `1e-10`, absolute tolerance `1e-12`, and dense output. The app does not use a
  fixed-timestep Verlet method.
- **Impact:** a terminal event detects an inward crossing of radius $R$.
- **Distance boundary:** a terminal event detects an outward crossing of
  100,000 Earth radii. “Out of range” is a calculation boundary, not proof of
  gravitational escape; a large bound orbit can also reach it.
- **Time limit:** integration is capped at 1,000 simulated years. For a bound
  orbit, the requested interval is the smaller of one period and this cap.
- **Grazing-impact protection:** if the inferred periapsis lies inside Earth,
  a radial-turn event can catch a shallow contact missed within a large solver
  step. A bracketed root search on the dense solution locates the first surface
  crossing. An unresolved contact produces a useful error rather than a
  silently accepted underground trajectory.
- **Sampling:** the returned times combine adaptive solver nodes with 3,000
  evenly spaced samples over the completed interval. The final sample count is
  therefore not necessarily 3,000.
- **Units sent to the browser:** time is in seconds, positions in Earth radii,
  and interpolation velocities in Earth radii per second. Displayed launch
  speed is separately converted to km/s.

The default launch is 500 km above Earth's surface on its right-hand side,
with speed ratio 1, angle 90 degrees, and playback multiplier 2,000.

## 4. Orbital geometry and numerical diagnostics

The initial state determines specific energy, specific angular momentum and
the eccentricity vector. These provide orbit type, eccentricity, periapsis,
apoapsis and, for bound motion, the period. In physical units,

$$
\varepsilon=\frac{v^2}{2}-\frac{GM}{r},
\qquad
a=-\frac{GM}{2\varepsilon},
\qquad
T=2\pi\sqrt{\frac{a^3}{GM}}.
$$

The period formula applies to bound motion. Radial shots, including zero-speed
drops, are handled as well as the ordinary conic cases.

The reported numerical-quality measure is the maximum sampled energy deviation,
expressed as a percentage of the magnitude of the initial energy. For shots
classified as parabolic, the normalization is $GM/r_0$ instead, avoiding division
by zero. The flight card states which normalization was used. This measures the
computed samples, not a rigorous error bound between them. The app does not
currently display a separate angular-momentum drift diagnostic.

## 5. Live geometric preview

- A thin dashed line previews the **current launch settings**, before firing.
  It is recomputed in JavaScript as the launcher, arrow or controls change.
- The preview derives energy, angular momentum and eccentricity from the
  initial state and samples the conic equation $r=p/(1+e\cos\theta)$ in the
  direction of motion. It does not run a numerical time integration.
- Future radius crossings are located analytically before sampling, so the
  preview ends at predicted impact or the distance boundary rather than
  drawing an irrelevant continuation through Earth.
- Radial trajectories use a straight-line preview, including an outward turn
  followed by return for a bound radial launch.
- The preview is geometric and does **not** apply the numerical time cap.
- Launched projectiles display only their travelled numerical paths. Updating
  the launcher changes the next-shot preview, never a previous shot's orbit.

## 6. Browser/server responsibilities and multiple flights

- The browser owns the launch settings, camera, flight list, playback state
  and simulation clock. Sliders, number boxes, arrow and preview use one shared
  launch state rather than independent callback-driven copies.
- Launch snapshots the current settings into a request. The server computes
  that flight, then returns its sampled trajectory and metadata.
- Existing flights continue moving while a new flight is calculated. A new
  flight starts at the browser's current simulation time when its result arrives.
- Only one new launch request is pending per browser tab; Launch is temporarily
  disabled while it is calculated. Firing while paused preserves the pause.
- Request identifiers prevent duplicate results from being added. An epoch
  counter invalidates results from before **Clear all**, so an old computation
  cannot repopulate the cleared scene. This discards its result; it does not
  cancel the server-side integration.
- Clear all removes flights, resets elapsed time and restarts visible flight
  numbering at 1. Individual removal does not renumber the remaining flights.
- There is no server round trip for every animation frame. Launch requests
  perform the numerical work; a separate lightweight heartbeat checks connectivity.
- State belongs to the browser page. Refreshing clears the flights; persistent
  saving, shared sessions and flight-history storage are not implemented.

## 7. Animation and time

- A `requestAnimationFrame` loop draws the scene on an HTML canvas.
- Cubic Hermite interpolation uses both positions and velocities for smooth
  movement between returned trajectory samples.
- All flights share one clock. The time multiplier is simulated seconds per
  real second; changing it affects every flight together.
- The multiplier ranges from 1 to $10^{10}$ through a logarithmic slider. This
  supports both near-Earth orbits and much longer distant flights. Very high
  values can make short-period motion appear to jump between frames.
- If one complete bound period is integrated without an earlier stopping
  condition, those samples replay indefinitely. Replay is visual reuse, not
  additional integration; the energy diagnostic describes the original period.
- Impact, boundary-limited and time-limited flights do not replay.
- Pause and hidden-tab handling freeze playback. Returning to a hidden tab
  does not add the time spent away. The clock also stops when no moving flights
  remain.
- **Time elapsed:** appears at the top right inside the scene, using spelled-out
  seconds, minutes, hours, days and years, with singular forms where appropriate.
  Flight-card duration values retain compact units. Grid spacing appears at
  the top left of the scene.

## 8. Launch controls and direct manipulation

| Control | Implemented behaviour |
| --- | --- |
| Horizontal/vertical position sliders | Fixed range -10 to +10 Earth radii |
| Position number boxes and scene placement | Accept coordinates up to +/-10,000 Earth radii per axis |
| Launch speed | Ratio 0 to 3 of local circular speed; actual km/s shown inline |
| Launch angle | -180 to +180 degrees, counterclockwise from the right |
| Time multiplier | Immediately after angle; logarithmic range 1 to $10^{10}$ |

- Each descriptive label sits above a row with roughly two-thirds slider and
  one-third number box. Sliders have numeric ticks, without special
  circular-speed or escape-speed buttons.
- Out-of-slider-range coordinates remain in the number box, preview and
  simulation. Only the slider thumb is clamped visually; it stays blue. Moving
  that slider deliberately chooses a new value inside its displayed range.
- Number boxes show four decimal places after editing, including round values.
  Display formatting does not round the underlying simulation state. Partial
  or invalid input is allowed while editing but blocks launching.
- Invalid interior or out-of-domain launch positions are shown rather than
  silently snapped to another physical location. The minimum height is 1 metre.
- Moving the arrowhead changes direction and speed simultaneously. Arrow length
  represents normalized speed in screen pixels, independently of zoom. A short
  handle remains at zero speed so the arrow can still be grabbed.
- A separate knob and joystick were not added: direct scene editing and the
  synchronized sliders provide those functions without extra control state.

## 9. Mouse, keyboard and camera controls

| Action | Input |
| --- | --- |
| Place launcher | Left-click empty space |
| Move launcher | Drag its round base |
| Change direction and speed | Drag its arrowhead |
| Change angle only | Shift + mouse wheel over the scene; up turns counterclockwise, down clockwise |
| Zoom | Ordinary mouse wheel, or the boxed -/+ buttons |
| Pan | Right-button drag |
| Launch | Launch button, F, or double-click the launcher base |
| Pause/resume | Space bar or Pause/Resume button |
| Centre Earth | Home or Centre Earth button |
| Open Help | H or Help button; Escape closes the dialog |

Shift-wheel uses two-degree increments per vertical wheel event and wraps the
angle through the -180/+180 boundary without changing speed or zoom.

Double-clicking empty space only places the launcher; it does not fire an
accidental shot. The implementation distinguishes the double-click count from
pointer-drag events and checks that the presses began on the launcher base.

Keyboard shortcuts are suppressed during text/number editing, but remain active
when a slider has focus. F therefore works immediately after releasing a slider,
without clicking elsewhere. Arrow keys retain their normal slider behaviour.

**Centre Earth** restores a near-Earth view. **Show all trajectories** fits Earth,
the launcher and already-travelled visible paths, not their future continuation.
Selecting a flight highlights it without moving the camera. **Follow selected**
tracks it; manual panning releases follow mode. Free-camera wheel zoom is centred
on the pointer, while following keeps the selected projectile centred.

## 10. Flights log and feedback

- The right-hand log is independently scrollable and uses compact colour-coded
  cards. Each flight's colour matches its path and marker.
- Cards show flight identity, orbit type, eccentricity and current status,
  including lap count for a replaying orbit.
- Selecting a heading highlights that flight. **Details** expands a structured
  information grid inside the card, rather than a plain-text panel underneath
  the scene. Opening another card's details closes the previous expansion.
- Details include distance from Earth, flight age, launch speed and angle,
  initial coordinates, period, periapsis/apoapsis, computed duration and energy
  drift. Geometric periapsis can lie inside Earth even though integration stops
  at the surface.
- **Hide/Show** controls visibility without deleting the flight or changing
  the clock. The remove button deletes that flight from the browser's list.
- The repetitive successful-shot message was removed to keep the Launch area
  quiet. Validation, calculation and connectivity messages remain.

## 11. Presentation, Help and connection status

- The title is **OrbitWorks**, with small caps, larger O and W, weight 700 and
  no added letter spacing. The subtitle ends with an exclamation mark.
- Google Sans is loaded through Google Fonts across the interface and canvas
  text, with local sans-serif fallbacks when unavailable.
- Secondary text on light panels uses the shared `--text-muted` colour
  `#596b80`. Text against the dark scene remains light. This separates visual
  hierarchy from excessively low contrast.
- Launch stays at the bottom of the left pane. Navigation buttons have visible
  boxes; Help is aligned to the right of their row. Responsive CSS rearranges
  the panels for narrower displays.
- Hover/focus explanations describe the controls without adding permanent
  explanatory blocks. Help is opened on demand, not forced at startup.
- Help has five sections: **Controls**, **Left panel**, **Top buttons**,
  **Flights log**, and **Technical details**. It is written for users unfamiliar
  with programming or orbital mechanics. Units are explained alongside their
  controls instead of in a separate Scales section.
- The status indicator distinguishes green **Running**, amber **Paused**, grey
  **Stopped**, and red **Stopped · disconnected**.
- A health request runs on a two-second timer with a 1.5-second timeout. The
  response identifies the app as `orbitworks`; the client must expect that same
  identifier. A stale `orbitworks-v5` expectation previously caused a false
  disconnection despite successful HTTP responses.
- A failed health check freezes playback and disables Launch. Reconnection
  preserves existing browser flights and leaves playback paused until Resume.
  Detection is periodic rather than instantaneous and may be delayed in
  background tabs.

## 12. Development history and scope

The first version used an altitude-only launcher and a local-tangent angle.
Later versions introduced arbitrary x/y placement, direct scene manipulation,
the geometric preview, a three-panel layout, larger simulation limits and
flight cards. The current app uses a fixed-axis angle, narrow practical sliders
independent of the wider input domain, and a simpler Help guide.

Some choices in the archived checklists are deliberately superseded: the
position sliders are no longer +/-10,000 or +/-5; out-of-range thumbs no longer
turn amber; Help uses H rather than ?; and Shift-wheel angle adjustment was
restored after being removed in an intermediate version. Later typography,
elapsed-time, numbering and keyboard-focus changes live in the packaged app,
and are maintained there. The obsolete root `app/` directory was subsequently
removed; the tests no longer load versioned app copies from it.

The old planning notes also proposed JAX-accelerated geometry, Diffrax
integration, standalone performance benchmarks, separate knob/joystick controls,
and password-protected access. These are **not implemented features** of the
current app. Numerical integration remains in the Python app module, and the
live conic preview remains in JavaScript, as detailed in §2. The archived
material preserves those ideas without presenting them as completed work.

Current regression coverage includes orbital closure, circular and open
orbits, impact and grazing-contact handling, distant launches, invalid inputs,
angle conventions, layout, assets, health responses and local-launcher behaviour.
The two app test modules import `orbitworks.app` directly and consolidate the
previous version-specific tests. Targeted interaction
checks during development also exercised dragging, double-click launch, input
precision, slider shortcuts, Help, and disconnection/reconnection. Those manual
or one-off checks are not a permanent browser test suite.

The source documents for this consolidation are `README.md`, `README_v2.md`,
`todo.md`, `TODO_v3.md`, `TODO_v4.md`, and `TODO_v5.md`. Those historical files
were consolidated before the obsolete application directory was removed.
The separate repository roadmap,
[OrbitWorks planned work](orbitworks_planned_work.md), remains independent of
this implemented-feature record.
