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

## 1. Exercise

> **For more information about exercise visit [exercise page](https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-🐍).**

**Problem:** When we create an array of size 1000 for faster enforceability and the two threads start to increment the
value pointed by the indicator, everything looks good and every element of the array has value 1. If we change size of
array on 1 000 000, problem occurs. Many elements in array have value 2 or 3 but also 0. Sometimes, <u>list index out of
range</u> error occurs. This was due to the switching threads occurred after incrementing the value pointed by the
indicator, and thus the thread that incremented the value didn't increase the indicator.

<p align="center">
    <img src="problem_hist_vis.png" width="608" height="458" alt="Problem histogram visualization">
    <br>
    <img src="problem_hist.png" width="441" height="19" alt="Problem histogram">
</p>

We are going to use the sync tool lock (mutex) to solve this problem. When the thread aquire the lock, than others
threads, that also want to lock it, must wait. In our variation of using lock (mutex) we will not see time differences
because of GIL(Global interpreter lock) in python. GIL prevents the parallel execution of threads, but doesn't prevent
competitive execution, which is sufficient for our needs. Competitive events may or may not run simultaneously. We say
that events in the program are performed competitively if, due to the source code, we cannot determine in what order
they set [[1]](#1).

### 1. Variation

When we acquire lock on start of the while cycle, which iterate over whole array, sometimes <u>list index out of
range</u> error occurs. It is because other thread starts execute another cycle before thread with acquired lock
increment the indicator.

```
while shared.indicator < len(shared.numbers):
    mutex.lock()
    shared.numbers[shared.indicator] += 1
    shared.indicator += 1
    mutex.unlock() 
```

We changed it to acquire lock before while cycle and release it after while cycle ends. Everything works fine, but we
used coarse granularity and our program incremented values serially. The whole incrementation of array was done by
thread, which first acquired lock.

```
mutex.lock()
while shared.indicator < len(shared.numbers):
    shared.numbers[shared.indicator] += 1
    shared.indicator += 1
mutex.unlock()
```

### 2. Variation

Before second variation of using mutex lock, we changed while cycle. We put the condition inside the cycle to create
finer granularity. Now in the while cycle are all threads and take turns executing the code.  
The condition is now in a critical area, which is part of the code that must be executed atomically. We give the
critical area between acquire and release lock. In this variation of using mutex lock isn't possible to occur <u>list
index out of range</u> error, because thread waiting to release lock checks the condition only when thread holding the
lock increment the indicator value and release the lock.

```
while True:
    mutex.lock()
    if shared.indicator >= len(shared.numbers):
        mutex.unlock()
        break
    shared.numbers[shared.indicator] += 1
    shared.indicator += 1
    mutex.unlock()
```

## References

<a id="1">[1]</a>
Matúš Jókay. PPaDS MMXXII.
<a href="https://uim.fei.stuba.sk/wp-content/uploads/2018/02/2022-01.uvod-do-paralelnych-a-distribuovanych-vypoctov.pdf">https://uim.fei.stuba.sk/wp-content/uploads/2018/02/2022-01.uvod-do-paralelnych-a-distribuovanych-vypoctov.pdf </a>