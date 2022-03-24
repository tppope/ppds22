from fei.ppds import Thread, Mutex, Semaphore

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


def hackers_boating(shared):
    pass


def serfs_boating(shared):
    pass


def main():
    shared = Shared()

    hackers = [Thread(hackers_boating, shared) for _ in range(4)]
    serfs = [Thread(serfs_boating, shared) for _ in range(4)]

    for thread in hackers + serfs:
        thread.join()


if __name__ == "__main__":
    main()
