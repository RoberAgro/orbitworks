"""Run the complete test suite with the current Python environment.

Run from the repository root, or use
this file's absolute path from any directory. The process exits with pytest's
exit code, so failed tests also fail a CI job. No browser or app server starts.
"""

from pathlib import Path
import subprocess
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTEST_OPTIONS = ["-q", "-p", "no:dash"]


def run_suite():
    """Discover all tests under tests/, using the same environment as this script.

    The optional Dash browser-testing plugin is disabled because these tests
    do not use its Selenium fixtures. This does not skip any repository tests.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", *PYTEST_OPTIONS],
        cwd=REPOSITORY_ROOT,
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(run_suite())
