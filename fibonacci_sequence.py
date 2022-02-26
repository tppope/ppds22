"""
    Author: Tomas Popik

    This file contains example fibonacci sequence computations with (threads_count + 2) elements using threads_count
    threads. This example shows the use of synchronization abstract data types to sort thread execution.
"""

from random import randint
from time import sleep

from fei.ppds import Thread

from adt import SequenceSemaphoreADT, SequenceEventADT


def make_fibonacci(fibonacci, adt, index):
    """Fibonacci sequence computation using own adt to align the threads so that they perform the calculation only
    when the thread in charge of the smaller index does the calculation.

    :param fibonacci: shared list between threads for fibonacci sequence computation with value 0 on index 0 and 1 on
    index 1
    :param adt: own abstract data type for align the threads to the right sequence
    :param index: points to the value in the fibonacci field that is calculated by the thread with that index
    """
    sleep(randint(1, 10) / 10)
    adt.wait(index)
    fibonacci[index + 2] = fibonacci[index] + fibonacci[index + 1]
    adt.signal()


if __name__ == "__main__":
    threads_count = 15

    fibonacci = [0] * (threads_count + 2)
    fibonacci[1] = 1

    adt = SequenceEventADT(threads_count)

    threads = [Thread(make_fibonacci, fibonacci, adt, i) for i in range(threads_count)]

    for thread in threads:
        thread.join()

    print(fibonacci)
