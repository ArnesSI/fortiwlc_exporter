import time

from fortiwlc_exporter import settings


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if settings.DEBUG:
            print('{}: {:0.6f} s'.format(method.__name__, (te - ts)))
        return result

    return timed
