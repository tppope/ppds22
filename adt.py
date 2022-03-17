"""
    Author: Tomas Popik
    License: MIT

    This file contains implementation of synchronization patterns and shared objects that using abstract data types for
    synchronization problems in savages and chefs exercise.
"""

from random import randint
from time import sleep

from fei.ppds import Mutex, Event, Semaphore


def put_servings_in_pot(chef_id):
    """Demonstration of placing portions in a pot.

    :param chef_id: identification number of the chef who puts the portions into the pot
    """
    print("chef %02d put servings in pot" % chef_id)
    sleep(randint(1, 10) / 1000)


class ChefsReusableEventSimpleBarrier:
    """Synchronization pattern to achieve synchronization where all threads wait for each other before executing
    critical area. It is using abstract data types Mutex and Event for synchronization. Its instance is reusable,
    thanks to which it can be used in a cycle. This barrier has a modified wait() function code for the savage and
    cook role.
    """

    def __init__(self, n):
        """Initialize number of threads to wait, counter and abstract data type Mutex and Event for synchronization.

        :param n: number of threads to wait on barrier
        """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self, chef_id, shared):
        """A function that forces threads to wait until the last thread arrives. It uses a mutex to atomically
        increment the counter and verify the condition. Uses the Event functions to implement the barrier. By
        implementing the clear function, reusable barrier was made. This function is changed in case of
        synchronization of chefs after cooking portions.

        :param chef_id: identification number of chefs thread
        :param shared: object with shared abstract data types
        """
        self.mutex.lock()
        self.counter += 1
        # local variable for each thread, thanks to which we can avoid blocking the last thread, which will make clear()
        temp_counter = self.counter
        if self.counter == self.n:
            self.counter = 0
            # the last chef puts the cooked portions in the pot
            put_servings_in_pot(chef_id)
            shared.portions = shared.max_portions
            # signal that the chefs have to wait for empty_pot.wait() until the pot is empty
            shared.empty_pot.clear()
            # signal for savages to be able to start taking portions of the pot
            shared.full_pot.signal()
            self.event.set()
            self.event.clear()
        self.mutex.unlock()
        # do not block the thread that made clear
        if temp_counter != self.n:
            self.event.wait()


class Shared:
    """Wrapper of the shared abstract types among savages and chefs threads."""

    def __init__(self, threads_count, max_portions):
        """Initialization of Mutex lock for atomic operations, portions for actual number of portions in the pot,
        max_portions for maximum possible number of portions in the pot, full_pot Semaphore to signal for savages to
        be able to start taking portions of the pot, empty_pot Event to signal that the chefs have to wait for
        empty_pot.wait() until the pot is empty, barrier for synchronizing chefs after cooking and for putting
        portions in the pot by only one chef.

        :param threads_count: the number of threads to wait for each other on the barrier
        :param max_portions: maximum number of portions in the pot
        """
        self.mutex = Mutex()
        self.portions = max_portions
        self.max_portions = max_portions
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier = ChefsReusableEventSimpleBarrier(threads_count)
