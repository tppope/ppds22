"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the "primes in fibonacci" co-program to demonstrate asynchronous
    programming using generators in python.
"""

from math import sqrt


class Fibonacci:
    def __init__(self):
        self.a = 0
        self.b = 1
        self.counter = -1

    def __next__(self):
        if self.counter < 1:
            self.counter += 1
            return self.counter

        self.a, self.b = self.b, self.a + self.b

        return self.b

    def __iter__(self):
        return self


def my_iterator(number):
    for i in range(2, int(sqrt(number)) + 1):
        yield i


def check_prime():
    is_prime = True
    while True:
        number = (yield is_prime)
        is_prime = True
        for i in my_iterator(number):
            if number % i == 0:
                is_prime = False


def primes_counter():
    primes = []
    is_prime = check_prime()
    next(is_prime)
    try:
        while True:
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
    primes_count = primes_counter()
    next(primes_count)
    fibonacci_array = []
    try:
        for number in Fibonacci():
            fibonacci_array.append(number)
            primes_count.send(number)
            yield

    except GeneratorExit:
        print("----- Primes in Fibonacci co-program -----\n")
        print("Count of numbers in Fibonacci sequence is %d" % len(fibonacci_array))
        print("Numbers in Fibonacci sequence:", end=" ")
        print(fibonacci_array, end="\n\n")
        primes_count.close()
