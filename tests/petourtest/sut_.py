
import json
import os
import time

beef = 0xDEAD


def foobar(*args, **kwargs):
    return len(args) + len(kwargs)


def multi_foobar(interval, num_loops):
    for _ in xrange(num_loops):
        time.sleep(interval)
        foobar()


def upvalues(*args, **kwargs):
    p = '/tmp/test.ss'
    with open(p, 'w') as fp:
        json.dump({1: 2, 3: 4, 5: [7, 8, 9]}, fp)
    return os.path.exists(p)


def compute(a, b, c=1.0, d=2.0, **kwargs):
    return (a + b) * c / d + len(kwargs)


def sleep_in_loop(interval, num_loops):
    for _ in xrange(num_loops):
        time.sleep(interval)


class FooBar(object):

    IDDQD = 'IDKFA'

    def __init__(self):
        self.num = -10

    def count(self, *args, **kwargs):
        return self.num + len(args) + len(kwargs)

    def compute(self, a, b, c=1.0, d=2.0, **kwargs):
        return (a + b) * c / d + len(kwargs) + self.num

    def upvalues(self, *args, **kwargs):
        p = '/tmp/test.ss'
        with open(p, 'w') as fp:
            json.dump({1: 2, 3: 4, 5: [7, 8, 9]}, fp)
        return os.path.exists(p)

    @classmethod
    def kls_count(cls, *args, **kwargs):
        return 10 + len(args) + len(kwargs)

    @staticmethod
    def sta_count(*args, **kwargs):
        return 100 + len(args) + len(kwargs)
