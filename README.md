# Paralel programming and distributed systems

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
7. Coprograms - Iterator, generator and carter in Python
8. Async IO - Async IO in Python
9. CUDA
10. CUDA continues

___

## 2. Exercise

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-🚧](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-🚧/).**

In this exercise, we are going to demonstrate a synchronization pattern "barrier". Thanks to the barrier, we can solve
synchronization problems, where when executing a program with multiple threads, we want all threads to wait before
executing a critical part. So in this exercise we will create a simple program where we will use the sleep() function to
demonstrate the execution of a part of the program, after which we will define a place where all threads will wait until
the last thread arrives. Subsequently, all threads will start competitively performing the critical part.

```
sleep(randint(1, 10) / 10)
print("Vlakno %d pred barierou" % thread_id)
barrier.wait()
print("Vlakno %d po bariere" % thread_id)
```

For first demonstration we will use simple barrier which is using abstract data type Semaphore initialized on value 0.
Semaphore is using functions wait() and signal(n). Wait() decrement internal Semaphore value and if it is negative
value, the thread that called it must wait. When some thread calls function signal(n). internal value of Semaphore is
incremented, and when some threads is waiting, n of them will continue, but we don't know in which order they will be.
The thread that called the signal(n) can also continue.

```
self.mutex.lock()
self.counter += 1
if self.counter == self.n:
    self.counter = 0
    self.semaphore.signal(self.n)
self.mutex.unlock()
self.semaphore.wait()
```