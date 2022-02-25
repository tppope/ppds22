"""
    Author: Tomas Popik

    This file contains implementation of synchronization patterns that using abstract data types for synchronization.
"""

from fei.ppds import Mutex, Semaphore, Event, print


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
        """A function that forces threads to wait until the last thread arrives. It uses a mutex to atomically
        increment the counter and verify the condition. Uses the Semaphore functions to implement the barrier.

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
        """A function that forces threads to wait until the last thread arrives. It uses a mutex to atomically
        increment the counter and verify the condition. Uses the Event functions to implement the barrier.

        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.event.set()
            self.counter = 0
        self.mutex.unlock()
        self.event.wait()


class ReusableEventSimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        temp_counter = self.counter
        if self.counter == self.n:
            self.counter = 0
            self.event.set()
            self.event.clear()
        self.mutex.unlock()
        if temp_counter != self.n:
            self.event.wait()
