# Parallel programming and distributed systems

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

> **Visit [subject page](https://uim.fei.stuba.sk/predmet/i-ppds) for more info.**

## Objective of the subject

The content of the course is the analysis of various synchronization patterns. Our goal is to offer students the
opportunity to become familiar with various synchronization problems along with their solutions. By synchronization
problems we mean the solution of the coordination of concurrently (perhaps also simultaneously) performed tasks in order
to ensure the integrity of the data with which the individual tasks work; of course, we also demand that a correct
calculation result be achieved.

In the second part of the semester, we focus on some modern areas of programming that are developing rapidly: parallel
calculations on graphics cards and asynchronous programming.

## Organization

1. Introduction to parallel and distributed computing
2. Mutex, multiplex, turnstile, (reusable) barrier
3. Barrier and Fibonacci revisited - Producer-consumer, readers-writers, turnstile
4. Readers / writers again - Evening philosophers
5. Smokers, savages, scoreboard
6. Barber, H20, crossing the river, caterpillar track
7. Co-programs - Iterator, generator and carter in Python
8. Async IO - Async IO in Python
9. CUDA
10. CUDA continues

___

## 7. Exercise

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/7-cvicenie/](https://uim.fei.stuba.sk/i-ppds/7-cvicenie/).**


In this exercise, we demonstrated asynchronous programming using co-programs. We used generators and advanced generators
in the Python programming language. From version 3.5, each generator can be considered as an extended generator.

The yield keyword in the function creates a generator from the function. Yield works as a return, but when called, the
status of the function is saved as it was before the yield was called. Another function call using next(generator) or
generator.send(value) will trigger the function from the next instruction to yield. Using generator.send(value) we also
send data where the call yield is. Subsequently, calling generator.close() over the generator will raise the
GeneratorExit exception and end the function (generator) run.

We created two co-programs for the demonstration. One looks for prime numbers in the Fibonacci sequence, and the other
reads the lines of the file and writes to the new file the words that the first letter gives uppercase.

In the first co-program, it is worth mentioning the function check_prime(), which receives data as a generator and then
returns the response if it performs operations with them. Of course, this function is made so complicated only for
experiments and demonstrations.

```python
def check_prime():
    is_prime = True
    while True:
        # yield gets the value sent to the generator and the next time it hits the yield,
        # the value is sent out of the generator.
        number = (yield is_prime)
        is_prime = True
        for i in my_iterator(number):
            if number % i == 0:
                is_prime = False
```

In the second co-program we still open the same file in the cycle, but the file we write to is open from the beginning
of the program. Using the call generator.send(value) we send him the words with first letter capitalized.

```python
def write_file(file):
    chars_count = 0
    try:
        while True:
            word = yield
            chars_count += len(word)
            file.write(word)
    except GeneratorExit:
        print("Number of written characters: %d" % chars_count)
        file.close()
```