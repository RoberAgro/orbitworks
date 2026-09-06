"""Layout, callback, asset and local-launcher checks for the current app."""

import importlib
from pathlib import Path
from unittest.mock import Mock
import pytest
import orbitworks

orbit_app = importlib.import_module("orbitworks.app")
ASSETS = Path(orbit_app.__file__).parent / "assets"


def walk(node):
    """Read serialized layout children for text and configuration assertions."""
    if isinstance(node, list):
        for child in node:
            yield from walk(child)
    elif isinstance(node, dict):
        yield node["props"]
        yield from walk(node["props"].get("children"))


def test_help_branding_and_isolated_assets():
    client = orbit_app.server.test_client()
    page = client.get("/").data.decode()
    assert "orbit_scene.js" in page and "orbitworks.css" in page
    assert client.get("/assets/orbitworks.css").status_code == 200
    assert client.get("/health").json["app"] == "orbitworks"
    props = list(walk(client.get("/_dash-layout").json))
    config = next(p["data"] for p in props if p.get("id") == "scene-config")
    assert config["positionSliderLimit"] == 10
    assert config["positionLimit"] == 10000
    assert config["defaults"]["angle"] == 90
    wordmark = next(p for p in props if p.get("className") == "wordmark")
    assert wordmark["children"] == "OrbitWorks"
    help_props = next(p for p in props if p.get("id") == "controls-dialog")
    help_nodes = list(walk(help_props["children"]))
    text = [p["children"] for p in help_nodes if isinstance(p.get("children"), str)]
    headings = [
        t
        for t in text
        if t
        in ["Controls", "Left panel", "Top buttons", "Flights log", "Technical details"]
    ]
    assert headings == [
        "Controls",
        "Left panel",
        "Top buttons",
        "Flights log",
        "Technical details",
    ]
    all_text = " ".join(text).lower()
    for excluded in ["release follow", "scales", "decimal", "server"]:
        assert excluded not in all_text
    assert "space bar" in all_text
    assert "hold shift" in all_text
    assert "press h" in all_text


def test_shortcuts_and_removed_success_message():
    javascript = (ASSETS / "orbit_scene.js").read_text(encoding="utf-8")
    css = (ASSETS / "orbitworks.css").read_text(encoding="utf-8")
    assert "event.shiftKey" in javascript
    assert 'event.key.toLowerCase() === "h"' in javascript
    assert "input:not([type=range])" in javascript
    assert "Ready to fire again" not in javascript
    assert "outside-range" not in css
    assert "font-variant-caps: small-caps" in css


def test_google_sans_typography_is_shared_by_ui_and_canvas():
    page = orbit_app.server.test_client().get("/").data.decode()
    assert "https://fonts.googleapis.com/css2?family=Google+Sans" in page
    css = (ASSETS / "orbitworks.css").read_text(encoding="utf-8")
    javascript = (ASSETS / "orbit_scene.js").read_text(encoding="utf-8")
    assert 'font-family: "Google Sans", "Segoe UI", system-ui, sans-serif' in css
    assert ".wordmark { font-family: inherit;" in css
    assert "this.fontFamily = getComputedStyle(canvas).fontFamily" in javascript
    assert "ctx.font=`11px ${this.fontFamily}`" in javascript


def test_dash_launch_callback_and_namespace():
    client = orbit_app.server.test_client()
    for route in [
        "/",
        "/_dash-layout",
        "/_dash-dependencies",
        "/assets/orbit_scene.js",
        "/assets/orbitworks.css",
    ]:
        assert client.get(route).status_code == 200
    dependencies = client.get("/_dash-dependencies").json
    callback = next(c for c in dependencies if c.get("clientside_function"))
    assert callback["clientside_function"]["namespace"] == "orbitworks"
    response = client.post(
        "/_dash-update-component",
        json={
            "output": "flight-result.data",
            "outputs": {"id": "flight-result", "property": "data"},
            "inputs": [
                {
                    "id": "launch-request",
                    "property": "data",
                    "value": {
                        "id": "shot",
                        "epoch": 4,
                        "x": 1.2,
                        "y": 0,
                        "ratio": 0.7,
                        "angle": 90,
                    },
                }
            ],
            "state": [],
            "changedPropIds": ["launch-request.data"],
        },
    )
    assert response.status_code == 200
    result = response.json["response"]["flight-result"]["data"]
    assert result["epoch"] == 4 and result["request_id"] == "shot"
    assert result["flight"]["outcome"] == "impact"


def test_health_identity_matches_javascript():
    payload = orbit_app.server.test_client().get("/health")
    assert payload.headers["Cache-Control"] == "no-store"
    javascript = (ASSETS / "orbit_scene.js").read_text(encoding="utf-8")
    assert f'.app!=="{payload.json["app"]}"' in javascript
    assert "window.orbitworks" in javascript
    assert "class OrbitScene" in javascript


@pytest.mark.parametrize(
    "debug,child,open_browser,opens",
    [
        (False, False, True, True),
        (True, False, True, False),
        (True, True, True, True),
        (False, False, False, False),
    ],
)
def test_local_launcher(monkeypatch, debug, child, open_browser, opens):
    monkeypatch.setenv("WERKZEUG_RUN_MAIN", "true" if child else "false")
    timer = Mock()
    timer_factory = Mock(return_value=timer)
    browser = Mock()
    run = Mock()
    monkeypatch.setattr("threading.Timer", timer_factory)
    monkeypatch.setattr("webbrowser.open", browser)
    monkeypatch.setattr(orbit_app.app, "run", run)
    orbitworks.launch_app(debug=debug, open_browser=open_browser)
    run.assert_called_once_with(
        host=orbit_app.HOST, port=orbit_app.PORT, debug=debug, use_reloader=debug
    )
    assert timer_factory.called == opens
    if opens:
        timer.start.assert_called_once()
        timer.cancel.assert_called_once()
        assert timer.daemon is True
        timer_factory.call_args.args[1]()
        browser.assert_called_once_with(f"http://{orbit_app.HOST}:{orbit_app.PORT}/")


def test_local_launcher_cancels_timer_on_start_failure(monkeypatch):
    timer = Mock()
    monkeypatch.setattr("threading.Timer", Mock(return_value=timer))
    monkeypatch.setattr(
        orbit_app.app, "run", Mock(side_effect=RuntimeError("Port occupied"))
    )
    with pytest.raises(RuntimeError, match="Port occupied"):
        orbitworks.launch_app()
    timer.cancel.assert_called_once()
