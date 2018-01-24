

beef = 0xDEAD


def foobar(*args, **kwargs):
    return len(args) + len(kwargs)


class FooBar(object):

    IDDQD = 'IDKFA'

    def __init__(self):
        self.num = -10

    def count(self, *args, **kwargs):
        return self.num + len(args) + len(kwargs)

    @classmethod
    def kls_count(cls, *args, **kwargs):
        return 10 + len(args) + len(kwargs)

    @staticmethod
    def sta_count(*args, **kwargs):
        return 100 + len(args) + len(kwargs)
