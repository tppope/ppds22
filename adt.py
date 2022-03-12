from fei.ppds import Mutex, Semaphore, Event


class Lightswitch:
    """Synchronization pattern to achieve that there will be only one category in the room represented by
    the Semaphore. The first thread enter the room uses a lightswitch of the given category to block the room
    and the last thread that leave will unblock it.
    """

    def __init__(self):
        """Initialize counter of threads on 0, so no thread is in the room. Mutex lock for atomic incrementing
        and decrementing of the counter and checking the first and last fiber in the room.

        """
        self.counter = 0
        self.mutex = Mutex()

    def switch_on(self, room):
        """The thread that first tries to enter the room represented by the Semaphore locks it using this
        function. Counter increment and checking if the thread is first is done atomically and then the function returns
        the number of threads that are in the room.

        :param room: abstract data type Semaphore representing the room
        :return: the number of threads that are in the room
        """
        self.mutex.lock()
        self.counter += 1
        # local variable counter which is different for every thread
        counter = self.counter
        if self.counter == 1:
            room.wait()
        self.mutex.unlock()
        return counter

    def switch_off(self, room):
        """The thread that is the last to leave the room represented by the Semaphore will open it using this function.
        Counter decrement and check if the thread is last is done atomically.

        :param room: abstract data type Semaphore representing the room
        """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            room.signal()
        self.mutex.unlock()


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


class Control:
    def __init__(self):
        self.data_access = Semaphore(1)
        self.tourniquet = Semaphore(1)
        self.data_ready = Event()
        self.barrier = ReusableEventSimpleBarrier(3)
