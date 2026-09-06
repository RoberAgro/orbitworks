"""Public package interface for the OrbitWorks orbital-mechanics laboratory."""


def launch_app(debug=False, open_browser=True):
    """Run the local app, optionally opening its page in the default browser.

    Imports are deferred so importing orbitworks alone does not create the Dash
    app or load its numerical dependencies. Debug mode enables the development
    reloader; only the serving process opens a browser tab, not its supervisor.
    The browser timer is cancelled when the server stops or fails to start.
    This helper is for local use, not the Gunicorn deployment entry point.
    """
    import os
    import webbrowser
    from threading import Timer

    from .app import HOST, PORT, app

    browser_timer = None
    serving_process = not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    if open_browser and serving_process:
        browser_timer = Timer(1, lambda: webbrowser.open(f"http://{HOST}:{PORT}/"))
        browser_timer.daemon = True
        browser_timer.start()
    try:
        app.run(host=HOST, port=PORT, debug=debug, use_reloader=debug)
    finally:
        if browser_timer is not None:
            browser_timer.cancel()
