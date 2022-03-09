"""
    Author: Tomas Popik
    License: MIT

    This file contains implementation and then experimentation on the synchronization task "producers and consumers",
    who represent parallel threads accessing a shared space.
"""

from random import randint
from time import sleep

from fei.ppds import Mutex, Semaphore, Thread, print


class Shared:
    def __init__(self, capacity):
        self.end = False
        self.mutex = Mutex()
        self.storage = Semaphore(capacity)
        self.items = Semaphore(0)


def produce(shared):
    while True:
        sleep(randint(1, 10) / 10)
        shared.storage.wait()
        if shared.end:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        print("P")
        shared.items.signal()


def consume(shared):
    while True:
        shared.items.wait()
        if shared.end:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.storage.signal()
        print("F")
        sleep(randint(1, 10) / 10)


if __name__ == "__main__":
    synch = Shared(10)

    consumers = [Thread(consume, synch) for _ in range(2)]
    producers = [Thread(produce, synch) for _ in range(5)]

    sleep(5)
    synch.end = True
    print('Main thread: waiting for completion')
    synch.storage.signal(100)
    synch.items.signal(100)
    [thread.join() for thread in producers + consumers]

    print('Main thread: complete')
