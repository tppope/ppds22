"""
    Author: Tomas Popik
    License: MIT

    This file contains implementation of synchronization patterns that using abstract data types for synchronization
    problems in crossing the river exercise.
"""

from fei.ppds import Mutex, Event


class ReusableEventSimpleBarrier:
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Event for synchronization. Its instance is reusable,
    thanks to which it can be used in a cycle.
    """

    def __init__(self, n):
        """Initialize number of threads to wait, counter and abstract data type Mutex and Event for synchronization.
        :param n: number of threads to wait on barrier
        """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """A function that forces threads to wait until the last thread arrives. It uses a mutex to atomically
        increment the counter and verify the condition. Uses the Event functions to implement the barrier. By
        implementing the clear function, reusable barrier was made.

        """
        self.mutex.lock()
        self.counter += 1
        # local variable for each thread, thanks to which we can avoid blocking the last thread, which will make clear()
        temp_counter = self.counter
        if self.counter == self.n:
            self.counter = 0
            self.event.set()
            self.event.clear()
        self.mutex.unlock()
        # do not block the thread that made clear
        if temp_counter != self.n:
            self.event.wait()
