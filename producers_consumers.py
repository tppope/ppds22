"""
    Author: Tomas Popik
    License: MIT

    This file contains implementation and then experimentation on the synchronization task "producers and consumers",
    who represent parallel threads accessing a shared space.
"""

from random import randint
from time import sleep

import numpy
from fei.ppds import Mutex, Semaphore, Thread, print
from matplotlib import pyplot as plt, cm


class Shared:
    """Wrapper of the shared abstract types among producers and consumers threads"""

    def __init__(self, capacity):
        """Initialize mutex lock for atomic read and write operation, storage Semaphore for stop producing when
        storage is full, items Semaphore for stop consuming when nothing is produced and end variable to warn
        producers and consumers to stop doing computation. Also, initialization of processed items to zero and mutex
        lock for atomic increment of processed items.

        :param capacity: capacity of storage
        """
        self.end = False
        self.mutex = Mutex()
        self.storage = Semaphore(capacity)
        self.items = Semaphore(0)
        self.processed_items = 0
        self.processed_items_mutex = Mutex()


def produce(shared):
    """Producers threads using this function to demonstrate production of items to storage.

    :param shared: object with shared abstract data types
    """
    while True:

        # time demonstration of item production
        sleep(randint(1, 10) / 100)

        shared.storage.wait()
        if shared.end:
            break
        shared.mutex.lock()

        # time demonstration of item storage
        sleep(randint(1, 10) / 1000)

        shared.mutex.unlock()
        shared.items.signal()


def consume(shared):
    """Consumers threads using this function to demonstrate consumption of items to storage.

    :param shared: object with shared abstract data types
    """
    while True:
        shared.items.wait()
        if shared.end:
            break
        shared.mutex.lock()

        # time demonstration of item consumption
        sleep(randint(1, 10) / 1000)

        shared.mutex.unlock()
        shared.storage.signal()

        # time demonstration of item processing
        sleep(randint(1, 10) / 100)

        shared.processed_items_mutex.lock()
        shared.processed_items += 1
        shared.processed_items_mutex.unlock()


def make_graph(x, y, z):
    """Implementation of 3D-surface graph.

    :param x: data on x-axis
    :param y: data on y-axis
    :param z: data on z-axis
    """
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    x, y = numpy.meshgrid(x, y)

    # Plot the surface
    ax.plot_surface(x, y, numpy.array(z), cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # label names
    ax.set_zlabel("processed items")
    ax.set_xlabel("consumers count")
    ax.set_ylabel("producers count")

    plt.show()


if __name__ == "__main__":
    synch = Shared(10)

    consumers = [Thread(consume, synch) for _ in range(2)]
    producers = [Thread(produce, synch) for _ in range(5)]

                # work time of producers and consumers
                sleep(1)
                synch.end = True

    print('Main thread: waiting for completion')

    # release of producers and consumers who were waiting for their computation when notified of stop doing computation
    synch.storage.signal(100)
    synch.items.signal(100)

    [thread.join() for thread in producers + consumers]

    print('Main thread: complete')
