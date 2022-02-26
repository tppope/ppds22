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

## 1. Task - ADT SimpleBarrier using ADT Event

In the first task we are going to execute the same program as in the exercise description, but we will implement a
simple barrier using an abstract data type Event. Event is using functions wait(), clear() and set() for
synchronization. The wait() blocks the thread when the internal value is false. When internal value is true, do nothing.
The clear() resets internal value of Event on false, so that the thread can be blocked when the wait() is called. The
set() changes internal value on true, so all waiting threads can continue on program execution and no thread is blocked
when wait() is called.

```
self.mutex.lock()
self.counter += 1
if self.counter == self.n:
    self.event.set()
    self.counter = 0
self.mutex.unlock()
self.event.wait()
```

It is a simple implementation where the last thread that passes the function calls set() and all threads continue to run
the following code competitively. No clear() function was used as this barrier is not intended to be reused to block
threads.

## 2. Task - Reusable barrier

We will continue in the first task, but now we will try to create a reusable barrier using the synchronization abstract
data type Event. We will use the clear() function, which will change the internal value of the Event to false, and any
call to wait() that will follow clear will then be blocked.  
The clear() function needs to be called when the last thread crosses the barrier, so our first implementation looked
like this.

```
self.mutex.lock()
self.counter += 1
temp_counter = self.counter
if self.counter == self.n:
    self.event.set()
self.mutex.unlock()
self.event.wait()
self.mutex.lock()
self.counter -= 1
if not self.counter:
    self.event.clear()
self.mutex.unlock()
```

When the counter drops to 0, it is clear that the last thread has passed and clear() can be called so that the next
wait() call can be blocked. In this implementation, it is necessary to use two different barriers when reusing, because
until the last thread calls clear(), some threads will not be blocked by calling wait() if they pass it again. Also, the
last condition does not have to be under the mutex lock because it does not matter how many times clear() is called.

```
self.mutex.lock()
self.counter += 1
temp_counter = self.counter
if self.counter == self.n:
    self.counter = 0
    self.event.set()
    self.event.clear()
self.mutex.unlock()
if temp_counter != self.n:
    self.event.wait()
```

On the second attempt, we created an implementation where we use the local variable temp_counter, which will be unique
for each thread, because each thread first increments the value of the counter, which is then stored in temp_counter.
Since the value of the temp_counter variable is unique, we know that the last thread that hits the barrier will have a
temp_counter value equal to the number of threads that the barrier should stop. Therefore, we can use the last condition
to determine that all threads are blocked except the last one. The last thread reset counter, release all pending
threads and call clear(). Unlike the use of a semaphore barrier, where it was necessary to use two different barriers,
because one single thread could decrement the value charged by the signal(n) function, in this implementation it is not
necessary as the last thread must release the lock for the new thread to continue. But it will be clear after the call.
But it will be after calling the call().

PS... It is also possible to create an implementation where the first thread calls clear() and the last thread calls
set().

