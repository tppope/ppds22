from fei.ppds import Thread


class Shared:
    def __init__(self, size):
        pass


def do_increment(shared):
    pass


shared = Shared(1_000_000)

t1 = Thread(do_increment, shared)
