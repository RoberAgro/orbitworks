"""Check the small test-and-deploy workflow without making network requests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github/workflows/test_and_deploy_app.yaml").read_text(
    encoding="utf-8"
)


def test_both_platforms_use_the_current_runner():
    assert "os: [ubuntu-latest, windows-latest]" in WORKFLOW
    assert "poetry run python tests/run_suite.py" in WORKFLOW
    assert (ROOT / "tests/run_suite.py").is_file()


def test_deployment_requires_tests_and_a_pushed_release_tag():
    deploy_job = WORKFLOW.split("\n  deploy:\n", 1)[1]
    assert "needs: test" in deploy_job
    assert (
        "github.event_name == 'push' && startsWith(github.ref, 'refs/tags/app-v')"
        in deploy_job
    )
    assert "always()" not in deploy_job
    assert "continue-on-error" not in WORKFLOW


def test_deployment_pins_the_checked_out_commit_and_fails_on_http_errors():
    assert 'ref=$(git rev-parse HEAD)' in WORKFLOW
    assert "curl --fail --silent --show-error" in WORKFLOW
    assert "${{ secrets.RENDER_DEPLOY_HOOK_URL }}" in WORKFLOW
