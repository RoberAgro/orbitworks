"""Physical regression checks for the current packaged OrbitWorks app."""

import importlib
import numpy as np
import pytest

orbit_app = importlib.import_module("orbitworks.app")


@pytest.mark.parametrize(
    "x,y,angle", [(2, 0, 90), (0, 2, 180), (-2, 0, -90), (0, -2, 0)]
)
def test_tangential_circles_at_different_positions(x, y, angle):
    flight = orbit_app.compute_positioned_flight(x, y, 1, angle)
    assert flight["repeat"]
    assert flight["eccentricity"] < 1e-8
    assert np.hypot(flight["x"][-1] - x, flight["y"][-1] - y) < 1e-6


@pytest.mark.parametrize("x,y", [(2, 0), (0, 2), (-2, 0)])
@pytest.mark.parametrize("angle", [0, 90, -90, 180, 37])
def test_angle_is_counterclockwise_from_positive_x_at_every_position(x, y, angle):
    flight = orbit_app.compute_positioned_flight(x, y, 1, angle)
    direction = np.array([flight["vx"][0], flight["vy"][0]])
    direction /= np.linalg.norm(direction)
    alpha = np.deg2rad(angle)
    np.testing.assert_allclose(direction, [np.cos(alpha), np.sin(alpha)], atol=1e-12)


def test_wider_number_box_domain_is_unchanged():
    flight = orbit_app.compute_positioned_flight(123.456789, 0, 1, 90)
    assert flight["launch_x"] == 123.456789
    assert flight["repeat"]


@pytest.mark.parametrize(
    "ratio,kind",
    [
        (1, "Circular"),
        (1.15, "Elliptical"),
        (np.sqrt(2), "Parabolic"),
        (1.6, "Hyperbolic"),
    ],
)
def test_four_conics_and_endpoints(ratio, kind):
    flight = orbit_app.compute_positioned_flight(1.2, 0, ratio, 90)
    radius = np.hypot(flight["x"], flight["y"])
    assert flight["orbit_type"] == kind
    assert np.all(np.diff(flight["time"]) > 0)
    assert radius.min() >= 1 - 1e-8
    assert flight["energy_error"] < 1e-4
    if kind in ("Circular", "Elliptical"):
        assert flight["repeat"]
        assert flight["duration"] == pytest.approx(flight["period"])
        assert np.hypot(flight["x"][-1] - 1.2, flight["y"][-1]) < 1e-6
    else:
        assert not flight["repeat"]
        assert flight["outcome"] == "out of range"
        assert radius[-1] == pytest.approx(orbit_app.OUTER_RADIUS)


@pytest.mark.parametrize(
    "radius,ratio,angle",
    [
        (1.2, 0.7, 90),
        (1.2, 0, 90),
        (1.2, 0.5, 0),
        (1.2, 0.5, 180),
        (1 + 1 / orbit_app.R_EARTH, 0.5, 90),
        (1 + 1 / orbit_app.R_EARTH, 0.5, 0),
        (1 + 1 / orbit_app.R_EARTH, 0.5, 180),
        (1.2, 2.5, 180),
        (10000, 0, 0),
    ],
)
def test_impacts_including_radial_surface_and_inward_hyperbolic_shots(
    radius, ratio, angle
):
    flight = orbit_app.compute_positioned_flight(radius, 0, ratio, angle)
    radii = np.hypot(flight["x"], flight["y"])
    assert flight["outcome"] == "impact"
    assert not flight["repeat"]
    assert flight["duration"] > 0
    assert radii[-1] == pytest.approx(1, abs=1e-8)
    assert radii.min() >= 1 - 1e-8


@pytest.mark.parametrize("apoapsis", [1.2, 10000])
def test_grazing_contact_is_not_skipped(apoapsis):
    periapsis = 1 - 10 / orbit_app.R_EARTH
    axis = (apoapsis + periapsis) / 2
    ratio = np.sqrt(2 - apoapsis / axis)
    flight = orbit_app.compute_positioned_flight(apoapsis, 0, ratio, 90)
    assert flight["outcome"] == "impact"


def test_large_ellipse_is_out_of_range_not_replayed(monkeypatch):
    monkeypatch.setattr(orbit_app, "OUTER_RADIUS", 25)
    flight = orbit_app.compute_positioned_flight(1.2, 0, 1.41, 90)
    assert flight["orbit_type"] == "Elliptical"
    assert flight["outcome"] == "out of range"
    assert not flight["repeat"]


def test_time_cap(monkeypatch):
    monkeypatch.setattr(orbit_app, "MAXIMUM_FLIGHT_TIME", 60)
    flight = orbit_app.compute_positioned_flight(1.2, 0, 1, 90)
    assert flight["duration"] == pytest.approx(60)
    assert flight["outcome"] == "time limit"
    assert not flight["repeat"]


@pytest.mark.parametrize(
    "values",
    [
        (None, 0, 1, 90),
        (0, 0, 1, 90),
        (10001, 0, 1, 90),
        (2, 0, -1, 90),
        (2, 0, 1, 181),
        (2, 0, float("nan"), 90),
    ],
)
def test_invalid_request_preserves_identifiers(values):
    result = orbit_app.fire_projectile(
        dict(zip(["x", "y", "ratio", "angle"], values), id="shot", epoch=3)
    )
    assert "error" in result
    assert result["epoch"] == 3
    assert result["request_id"] == "shot"
