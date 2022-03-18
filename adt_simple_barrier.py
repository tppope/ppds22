"""
    Author: Tomas Popik
    License: MIT

    This file contains example usage demonstration of the simple barrier with using five threads that perform the
    barrier_example function.
"""

from random import randint
from time import sleep

from fei.ppds import Thread, print

from adt import SemaphoreSimpleBarrier
from adt import EventSimpleBarrier


def barrier_example(barrier, thread_id):
    """Execution demonstration using sleep and then demonstrate barrier usage to keep all threads waiting for last one.

    :param barrier: synchronization pattern using some abstract data type for synchronization
    :param thread_id: identification number of thread that executes this function
    """
    sleep(randint(1, 10) / 10)
    print("Vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("Vlakno %d po bariere" % thread_id)


def main():
    threads_count = 5

    simple_barrier = EventSimpleBarrier(threads_count)

    threads = [Thread(barrier_example, simple_barrier, i) for i in range(threads_count)]
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
