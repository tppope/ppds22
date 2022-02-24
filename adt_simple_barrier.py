from random import randint
from time import sleep

from fei.ppds import Thread, print

from adt import SemaphoreSimpleBarrier


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("Vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("Vlakno %d po bariere" % thread_id)


if __name__ == "__main__":
    threads_count = 5

    simple_barrier = SemaphoreSimpleBarrier(threads_count)

    threads = [Thread(barrier_example, simple_barrier, i) for i in range(threads_count)]
    for thread in threads:
        thread.join()
