# Highlight exception messages
# https://stackoverflow.com/questions/25109105/how-to-colorize-the-output-of-python-errors-in-the-gnome-terminal/52797444#52797444
try:
    import IPython.core.ultratb
except ImportError:
    # No IPython. Use default exception printing.
    pass
else:
    import sys

    sys.excepthook = IPython.core.ultratb.FormattedTB(call_pdb=False)


from .graphics import *
from .centrifugal_compressor import CentrifugalCompressor

from . import centrifugal_compressor as cc


# Package info
__version__ = "0.1.1"
PACKAGE_NAME = "turbomaps"
URL_GITHUB = "https://github.com/turbo-sim/turbomaps"
# URL_DOCS = "https://turbo-sim.github.io/turbomaps/"
URL_PYPI = "https://pypi.org/project/turbomaps/"
URL_DTU = "https://thermalpower.dtu.dk/"
BREAKLINE = 80 * "-"


def launch_app():
    import os
    import webbrowser
    from threading import Timer
    from turbomaps.app import app

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, lambda: webbrowser.open("http://127.0.0.1:8050/")).start()

    app.run(debug=True)
