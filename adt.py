"""
    Author: Tomas Popik

    This file contains implementation of synchronization patterns that using abstract data types for synchronization.
"""

from fei.ppds import Mutex, Semaphore, Event


class SemaphoreSimpleBarrier:
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Semaphore for synchronization."""

    def __init__(self, n):
        """Initialize number of threads to wait, counter and abstract data type Mutex and Semaphore for synchronization

        :param n: number of threads to wait on barrier
        """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self):
        """Simple barrier implementation with atomic counter incrementation and condition checking

        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()


class EventSimpleBarrier:
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Event for synchronization."""

    def __init__(self, n):
        """Initialize number of threads to wait, counter and abstract data type Mutex and Event for synchronization

        :param n: number of threads to wait on barrier
        """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        pass
