"""Start OrbitWorks locally and open its page in the default browser."""

from orbitworks import launch_app

DEBUG = False
OPEN_BROWSER = True


if __name__ == "__main__":
    launch_app(debug=DEBUG, open_browser=OPEN_BROWSER)
