from time import sleep

from fei.ppds import Thread

from first_letter_capitalized import capitalize_first_letter
from primes_in_fibonacci import fibonacci_sequence


class Shared:
    """Object to share variable among other threads."""

    def __init__(self):
        self.is_over = False


def scheduler(shared):
    """Co-program scheduling demonstration function

    :param shared:
    """
    fibonacci = fibonacci_sequence()
    first_letter_capitalized = capitalize_first_letter()
    while not shared.is_over:
        next(fibonacci)
        next(first_letter_capitalized)
    fibonacci.close()
    first_letter_capitalized.close()


def main():
    """Main function.

    """
    shared = Shared()
    working_thread = Thread(scheduler, shared)

    # working time...
    sleep(1)

    # end working time
    shared.is_over = True

    working_thread.join()


if __name__ == "__main__":
    main()
