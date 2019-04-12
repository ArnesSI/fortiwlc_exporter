import logging
import signal
import time

from fortiwlc_exporter import settings


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if hasattr(args[0], 'name'):
            logging.debug(
                '{}[{}].{}: {:0.6f} s'.format(
                    type(args[0]).__name__, args[0].name, method.__name__, (te - ts)
                )
            )
        else:
            logging.debug(
                '{}.{}: {:0.6f} s'.format(method.__module__, method.__name__, (te - ts))
            )
        return result

    return timed


def timeout():
    def decorate(f):
        def handler(signum, frame):
            raise TimeoutError()

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(settings.TIMEOUT)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
            return result

        new_f.__name__ = f.__name__
        return new_f

    return decorate
