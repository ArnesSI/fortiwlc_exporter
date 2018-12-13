import time

from .config import CONFIG


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if CONFIG.get('debug'):
            print('{}: {:0.6f} s'.format(method.__name__, (te - ts)))
        return result
    return timed
