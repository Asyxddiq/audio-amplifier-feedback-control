"""
RepeatTimer, as provided in the EE2073 course notebook.

Calls `function` roughly every `interval` seconds on a background thread.
Note the timing caveat we found in Lab 9: the next call is only scheduled
after the current one finishes, so each cycle actually takes
interval + execution time + OS scheduling delay, not exactly `interval`.
"""
import threading


class RepeatTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            pass
        self.start()        # re-arm only after function() has returned

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        try:
            self._timer.cancel()
            self.is_running = False
        except Exception:
            pass
