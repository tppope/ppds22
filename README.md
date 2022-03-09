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

## 3. Exercise

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-💡/?%2F](https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-💡/?%2F).**

In this exercise, we had to decide whether to implement and then experiment on the synchronization task of "producers
and consumers" or "readers and writers".

I have chosen implementation and then experimentation on the synchronization task "producers and consumers", who
represent parallel threads accessing a shared space. We will not have any shared memory space in our models, but we will
demonstrate writing and reading by some random delay. The size of the imaginary shared space will be defined by the
initialization of Semaphore "storage", which will take care of synchronizing production to the shared memory space if it
is already full. Semaphore "items", which will take care of synchronizing consumption from the memory location, if there
is nothing to consume. By initializing Semaphore, we will take care of synchronizing consumption from a memory location
if there is nothing to consume.