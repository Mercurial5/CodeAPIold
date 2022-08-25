import time


class Time:
    """
    Time - utility class use for snapping the time of subprocess

    from:
    https://stackoverflow.com/questions/45492786/find-execution-time-for-subprocess-popen-python
    """

    def __init__(self):
        self.time = None

    def snap(self) -> float:
        """
        This function return delta time between snaps
        """
        delta = 0.0
        if self.time is not None:
            delta = self.time - time.time()

        self.time = time.time()
        return delta
