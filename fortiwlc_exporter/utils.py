import time

from .config import CONFIG


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if CONFIG.get('debug'):
            print('{} {} ms'.format(method.__name__, (te - ts) * 1000))
        return result
    return timed
