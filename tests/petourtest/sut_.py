

def foobar(*args, **kwargs):
    return len(args) + len(kwargs)


class FooBar(object):

    def __init__(self):
        self.num = -10

    def count(self, *args, **kwargs):
        return self.num + len(args) + len(kwargs)
