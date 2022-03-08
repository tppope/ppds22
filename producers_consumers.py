from fei.ppds import Mutex, Semaphore


class Shared:
    def __init__(self, capacity):
        self.mutex = Mutex()
        self.free = Semaphore(capacity)
        self.items = Semaphore(0)


def produce(shared):
    pass


def consume(shared):
    pass


if __name__ == "__main__":
    pass
