"""Exercise workflow validation and HTTP request construction without deploying."""

from pathlib import Path
import re
import textwrap
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest
import orbitworks

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github/workflows/test_and_deploy_app.yaml").read_text(
    encoding="utf-8"
)
PYTHON_BLOCKS = [
    textwrap.dedent(block)
    for block in re.findall(
        r"python - <<'PY'\n(.*?)\n\s+PY(?:\n|$)", WORKFLOW, re.DOTALL
    )
]


def test_deploy_has_test_tag_and_main_gates():
    assert "needs: test" in WORKFLOW
    assert (
        "github.event_name == 'push' && startsWith(github.ref, 'refs/tags/app-v')"
        in WORKFLOW
    )
    assert "git merge-base --is-ancestor HEAD origin/main" in WORKFLOW
    assert "git rev-parse HEAD" in WORKFLOW
    assert "os: [ubuntu-latest, windows-latest]" in WORKFLOW
    assert "poetry run python scripts/run_tests.py" in WORKFLOW
    assert len(PYTHON_BLOCKS) == 2


@pytest.mark.parametrize("valid", [True, False])
def test_release_tag_validation(monkeypatch, valid):
    monkeypatch.chdir(ROOT)
    tag = f"app-v{orbitworks.__version__}" if valid else "app-v0.0.0-wrong"
    monkeypatch.setenv("RELEASE_TAG", tag)
    if valid:
        exec(compile(PYTHON_BLOCKS[0], "release-validation", "exec"), {})
    else:
        with pytest.raises(SystemExit, match="does not match"):
            exec(compile(PYTHON_BLOCKS[0], "release-validation", "exec"), {})


def test_hook_pins_tested_sha_without_exposing_secret(monkeypatch, capsys):
    monkeypatch.setenv(
        "RENDER_DEPLOY_HOOK_URL",
        "https://api.render.com/deploy/srv-example?key=private&ref=old",
    )
    monkeypatch.setenv("RELEASE_COMMIT", "a" * 40)
    response = MagicMock()
    response.__enter__.return_value.status = 200
    request_mock = MagicMock(return_value=response)
    monkeypatch.setattr("urllib.request.urlopen", request_mock)
    exec(compile(PYTHON_BLOCKS[1], "deploy-request", "exec"), {})
    request = request_mock.call_args.args[0]
    assert request.method == "POST"
    assert parse_qs(urlsplit(request.full_url).query) == {
        "key": ["private"],
        "ref": ["a" * 40],
    }
    output = capsys.readouterr().out
    assert "private" not in output
    assert "a" * 40 in output


@pytest.mark.parametrize(
    "failure", ["missing-secret", "invalid-sha", "wrong-host", "network"]
)
def test_hook_failures_are_safe(monkeypatch, failure):
    monkeypatch.setenv(
        "RENDER_DEPLOY_HOOK_URL",
        "https://api.render.com/deploy/srv-example?key=private",
    )
    monkeypatch.setenv("RELEASE_COMMIT", "a" * 40)
    request_mock = MagicMock(side_effect=RuntimeError("secret URL: private"))
    monkeypatch.setattr("urllib.request.urlopen", request_mock)
    if failure == "missing-secret":
        monkeypatch.delenv("RENDER_DEPLOY_HOOK_URL")
    elif failure == "invalid-sha":
        monkeypatch.setenv("RELEASE_COMMIT", "not-a-sha")
    elif failure == "wrong-host":
        monkeypatch.setenv("RENDER_DEPLOY_HOOK_URL", "https://example.com/?key=private")
    with pytest.raises(SystemExit) as error:
        exec(compile(PYTHON_BLOCKS[1], "deploy-request", "exec"), {})
    assert "private" not in str(error.value)
    assert request_mock.called == (failure == "network")
