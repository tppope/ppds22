from random import randint
from time import sleep

from fei.ppds import Thread

from adt import SequenceADT


def make_fibonacci(fibonacci, adt, index):
    sleep(randint(1, 10) / 10)
    adt.wait(index)
    fibonacci[index + 2] = fibonacci[index] + fibonacci[index + 1]
    adt.signal()


if __name__ == "__main__":
    threads_count = 15

    fibonacci = [0] * (threads_count + 2)
    fibonacci[1] = 1

    adt = SequenceADT(threads_count)

    threads = [Thread(make_fibonacci, fibonacci, adt, i) for i in range(threads_count)]

    for thread in threads:
        thread.join()

    print(fibonacci)
