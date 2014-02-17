from time import time
from collections import defaultdict


class TimeCacheKey:
    """Helper class for plone.memoize.ram.cache.

    Memoizes a callable for a time period."""

    def __init__(self, period, last_time=0):
        self.period = period
        self.last_time = defaultdict(int)

    def __call__(self, method, *args, **kargs):
        nargs = list(args)
        nkargs = self._kargs_to_list(kargs)
        nargs.extend(nkargs)
        nargs = str(nargs)
        now = time()
        last_time = self.last_time[nargs]
        if now - last_time > self.period:
            self.last_time[nargs] = now
            last_time = now

        print nargs, self.last_time
        return nargs, last_time

    def _kargs_to_list(self, kargs):
        lst = []
        for k, v in sorted(kargs.items()):
            if type(v) == list:
                vv = ','.join(sorted(v))
            else:
                vv = v
            lst.append((k, vv))
        return lst
