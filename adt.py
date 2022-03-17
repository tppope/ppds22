from random import randint
from time import sleep

from fei.ppds import Mutex, Event, Semaphore


def put_servings_in_pot(chef_id):
    print("chef %2d put servings in pot" % chef_id)
    sleep(randint(1, 10) / 1000)


class ChefsReusableEventSimpleBarrier:
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

    def wait(self, shared, chef_id):
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
            put_servings_in_pot(chef_id)
            shared.portions = shared.max_portions
            shared.empty_pot.clear()
            shared.full_pot.signal()
            self.event.set()
            self.event.clear()
        self.mutex.unlock()
        # do not block the thread that made clear
        if temp_counter != self.n:
            self.event.wait()


class Shared:
    def __init__(self, threads_count, max_portions):
        self.mutex = Mutex()
        self.portions = max_portions
        self.max_portions = max_portions
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier = ChefsReusableEventSimpleBarrier(threads_count)
