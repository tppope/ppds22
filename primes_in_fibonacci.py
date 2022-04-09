"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the "primes in fibonacci" co-program to demonstrate asynchronous
    programming using generators in python.
"""

from math import sqrt


class Fibonacci:
    """An object (iterator) that demonstrates iterating through a Fibonacci sequence"""

    def __init__(self):
        self.a = 0
        self.b = 1
        self.counter = -1

    def __next__(self):
        # for first two iteration return 0 and 1
        if self.counter < 1:
            self.counter += 1
            return self.counter

        # new number in fibonacci sequence
        self.a, self.b = self.b, self.a + self.b

        return self.b

    def __iter__(self):
        return self


def my_iterator(number):
    """Function that demonstrates the use of the generator as an iterator. The function throws a StopIteration
    Exception after its operation is done. We use it to generate numbers that need to be divided by a number to
    determine if it is a prime number.

    :param number: number to determine if it is a prime number
    """
    for i in range(2, int(sqrt(number)) + 1):
        yield i


def check_prime():
    """The function is complicated, due to demonstrations of how it is possible to send a value to the advanced
    generator and then return the result. The function checks if number which is sent to the generator is prime number.
    GeneratorExit Exception is ignored when close() is called on this generator.

    """
    is_prime = True
    while True:
        # yield gets the value sent to the generator and the next time it hits the yield,
        # the value is sent out of the generator.
        number = (yield is_prime)
        is_prime = True
        for i in my_iterator(number):
            if number % i == 0:
                is_prime = False


def primes_counter(is_prime):
    """Function that represents a generator that obtains a number from a Fibonacci sequence and determines if it is a
    prime number. If close() is called over this generator, GeneratorExit Exception is thrown and close() is called
    over the check_prime generator, and the count and individual prime numbers found in the Fibonacci sequence are
    printed.

    :param is_prime: function (generator) checks if number which is sent to it is prime number
    """
    next(is_prime)
    primes = []
    try:
        while True:
            # get number to check if it is prime number
            number = yield
            if number > 1:
                if is_prime.send(number):
                    primes.append(number)
    except GeneratorExit:
        print("Count of primes in Fibonacci sequence is %d" % len(primes))
        print("Prime numbers in Fibonacci sequence:", end=" ")
        print(primes)
        is_prime.close()


def fibonacci_sequence():
    """Function that represents a generator that retrieves a number from a Fibonacci sequence iterator and sends it
    to a generator that determines if the number is a prime number. If close() is called over this generator,
    the Fibonacci sequence is displayed and close is called over the prime_count generator.

    """
    is_prime = check_prime()
    primes_count = primes_counter(is_prime)
    next(primes_count)
    fibonacci_array = []
    try:
        for number in Fibonacci():
            fibonacci_array.append(number)
            primes_count.send(number)

            # wait here to be called by scheduler
            yield

    except GeneratorExit:
        print("\n----- Primes in Fibonacci co-program -----\n")
        print("Count of numbers in Fibonacci sequence is %d" % len(fibonacci_array))
        print("Numbers in Fibonacci sequence:", end=" ")
        print(fibonacci_array, end="\n\n")
        primes_count.close()
