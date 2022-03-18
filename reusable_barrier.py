"""
    Author: Tomas Popik
    License: MIT

    This file contains example usage demonstration of the simple reusable event barrier with using five threads that
    perform the barrier_example function.
"""

from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print

from adt import ReusableEventSimpleBarrier


def rendezvous(thread_name):
    """A simple function to demonstrate the execution of a program using the sleep function.

    :param thread_name: thread identification
    """
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    """A simple function to demonstrate the execution of a program using the sleep function.

    :param thread_name: thread identification
    """
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name, barrier):
    """Example function to demonstrate the use of a reusable barrier in an infinite cycle. To end the program,
    it is necessary to forcibly interrupt the process.

    :param thread_name: thread identification
    :param barrier: synchronization pattern using some abstract data type for synchronization
    """
    while True:
        barrier.wait()
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)


def main():
    threads_count = 10

    simple_barrier = ReusableEventSimpleBarrier(threads_count)

    # infinite cycle is used, force quit is required to end of the program
    threads = [Thread(barrier_example, 'Thread %d' % i, simple_barrier) for i in range(threads_count)]
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
