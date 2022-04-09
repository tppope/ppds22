from time import sleep

from fei.ppds import Thread

from primes_in_fibonacci import fibonacci_sequence


class Shared:
    def __init__(self):
        self.is_over = False


def scheduler(shared):
    fibonacci = fibonacci_sequence()
    while not shared.is_over:
        next(fibonacci)
    fibonacci.close()


def main():
    shared = Shared()
    working_thread = Thread(scheduler, shared)

    # working time...
    sleep(10)

    # end working time
    shared.is_over = True

    working_thread.join()


if __name__ == "__main__":
    main()
