from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print

from adt import ReusableEventSimpleBarrier


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name, barrier):
    while True:
        barrier.wait()
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)


if __name__ == "__main__":
    threads_count = 10

    simple_barrier = ReusableEventSimpleBarrier(threads_count)

    threads = [Thread(barrier_example, 'Thread %d' % i, simple_barrier) for i in
               range(threads_count)]
    for thread in threads:
        thread.join()
