"""
    Author: Tomas Popik

    This file contains implementation of synchronization patterns that using abstract data types for synchronization.
"""

from fei.ppds import Mutex, Semaphore, Event, print


class SemaphoreSimpleBarrier:
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Semaphore for synchronization.
    """

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
    critical area. It is using abstract data types Mutex and Event for synchronization.
    """

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
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Event for synchronization. Its instance is reusable,
    thanks to which it can be used in a cycle.
    """

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


class SequenceSemaphoreADT:
    """Synchronization tool for sequencing threads."""

    def __init__(self, n):
        """Initialize number of threads, index counter for the organization of threads, counter1 and counter2 for
        distinguishing semaphores in the signal function, mutex for atomic operation and adt Semaphores to wait for all
        the threads, so they could be lined up.

        :param n: number of threads to line up
        """
        self.n = n
        self.index_counter = 0
        self.counter1 = 0
        self.counter2 = 0
        self.mutex = Mutex()
        self.semaphore1 = Semaphore(0)
        self.semaphore2 = Semaphore(0)

    def wait(self, index):
        """A method that stops the threads and releases them in the correct order after the signal.

        :param index: thread index
        """
        while True:
            self.mutex.lock()
            self.counter1 += 1
            if self.counter1 == self.n - self.index_counter:
                self.counter1 = 0
                self.semaphore1.signal(self.n - self.index_counter)
            self.mutex.unlock()
            self.semaphore1.wait()

            if index == self.index_counter:
                break

            self.mutex.lock()
            self.counter2 += 1
            if self.counter2 == self.n - self.index_counter:
                self.counter2 = 0
                self.semaphore2.signal(self.n - self.index_counter)
            self.mutex.unlock()
            self.semaphore2.wait()

            if index == self.index_counter:
                break

    def signal(self):
        """A signal to the next thread in order, that it can begin to perform a critical area. The conditions release
        the waiting threads if the last thread to be stopped for the barrier was the thread to be released.

        """
        self.mutex.lock()
        self.index_counter += 1
        if self.counter1 == self.n - self.index_counter:
            self.counter1 = 0
            self.semaphore1.signal(self.n - self.index_counter)
        elif self.counter2 == self.n - self.index_counter:
            self.counter2 = 0
            self.semaphore2.signal(self.n - self.index_counter)
        self.mutex.unlock()


class SequenceEventADT:
    """Synchronization tool for sequencing threads."""

    def __init__(self, n):
        """Initialize number of threads, index counter for the organization of threads, counter of threads,
        mutex for atomic operation and abstract data type Event to wait for all the threads, so they could be lined up.

        :param n: number of threads to line up
        """
        self.n = n
        self.index_counter = 0
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self, index):
        """A method that stops the threads and releases them in the correct order after the signal.

        :param index: thread index
        """
        while True:
            self.mutex.lock()
            self.counter += 1
            # local variable for threads, thanks to which we can avoid blocking the last thread, which will make clear()
            temp_counter = self.counter
            if self.counter == self.n - self.index_counter:
                self.counter = 0
                self.event.set()
                self.event.clear()
            self.mutex.unlock()
            # do not block the thread that made clear
            if temp_counter != self.n - self.index_counter:
                self.event.wait()

            # release thread that has an index that is in line for execution
            if index == self.index_counter:
                break

    def signal(self):
        """A signal to the next thread in order, that it can begin to perform a critical area. The condition release
        the waiting threads if the last thread to be stopped for the barrier was the thread to be released.

        """
        self.mutex.lock()
        self.index_counter += 1
        if self.counter == self.n - self.index_counter:
            self.counter = 0
            self.event.set()
            self.event.clear()
        self.mutex.unlock()
