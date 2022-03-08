from random import randint
from time import sleep

from fei.ppds import Mutex, Semaphore, Thread


class Shared:
    def __init__(self, capacity):
        self.mutex = Mutex()
        self.free = Semaphore(capacity)
        self.items = Semaphore(0)


def produce(shared):
    while True:
        sleep(randint(1, 10) / 10)
        shared.free.wait()
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.items.signal()


def consume(shared):
    while True:
        shared.items.wait()
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.free.signal()
        sleep(randint(1, 10) / 10)


if __name__ == "__main__":
    synch = Shared(10)

    consumers = [Thread(consume, synch) for _ in range(2)]
    producers = [Thread(produce, synch) for _ in range(5)]

    [thread.join() for thread in producers + consumers]
