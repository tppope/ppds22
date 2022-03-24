from random import randint
from time import sleep

from fei.ppds import Thread, Mutex, Semaphore, print

from adt import ReusableEventSimpleBarrier


class Shared:
    """Wrapper of the shared abstract types among hackers and serfs threads"""

    def __init__(self):
        """Initialize hackers_count serfs_count before boating on 0, mutex for the atomic execution of a critical
        area and also so that hackers and slaves do not overtake. Semaphore hackers_queue and serfs_queue to
        synchronize hackers and slaves so that only 4 hackers or 4 slaves or 2 hackers and 2 slaves can board.
        Barrier for the ship to wait until there are four of them.

        """
        self.hackers_count = 0
        self.serfs_count = 0
        self.mutex = Mutex()
        self.hackers_queue = Semaphore(0)
        self.serfs_queue = Semaphore(0)
        self.barrier = ReusableEventSimpleBarrier(4)


def boarding(member):
    print(member + " is boarding...")
    sleep(randint(1, 10) / 100)


def sail_out(captain):
    print(captain + " as captain gave signal to sail out...\n")
    sleep(randint(1, 10) / 100)


def hackers_boating(shared, hacker):
    # delay for hacker threads order randomization
    sleep(randint(1, 10) / 100)
    while True:
        is_captain = False
        shared.mutex.lock()
        shared.hackers_count += 1
        if shared.hackers_count == 4:
            is_captain = True
            shared.hackers_count = 0
            shared.hackers_queue.signal(4)
        elif shared.hackers_count == 2 and shared.serfs_count >= 2:
            is_captain = True
            shared.hackers_count = 0
            shared.hackers_queue.signal(2)
            shared.serfs_count -= 2
            shared.serfs_queue.signal(2)
        else:
            shared.mutex.unlock()

        shared.hackers_queue.wait()

        boarding(hacker)
        # wait for four members...
        shared.barrier.wait()

        if is_captain:
            sail_out(hacker)
            shared.mutex.unlock()


def serfs_boating(shared, serf):
    # delay for serf threads order randomization
    sleep(randint(1, 10) / 100)
    while True:
        is_captain = False
        shared.mutex.lock()
        shared.serfs_count += 1
        if shared.serfs_count == 4:
            is_captain = True
            shared.serfs_count = 0
            shared.serfs_queue.signal(4)
        elif shared.serfs_count == 2 and shared.hackers_count >= 2:
            is_captain = True
            shared.serfs_count = 0
            shared.serfs_queue.signal(2)
            shared.hackers_count -= 2
            shared.hackers_queue.signal(2)
        else:
            shared.mutex.unlock()

        shared.serfs_queue.wait()

        boarding(serf)
        # wait for four members...
        shared.barrier.wait()

        if is_captain:
            sail_out(serf)
            shared.mutex.unlock()


def main():
    shared = Shared()

    hackers = [Thread(hackers_boating, shared, "Hacker " + str(hacker)) for hacker in range(8)]
    serfs = [Thread(serfs_boating, shared, "Serf " + str(serf)) for serf in range(8)]

    for thread in hackers + serfs:
        thread.join()


if __name__ == "__main__":
    main()
