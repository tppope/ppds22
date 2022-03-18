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

## 4. Exercise

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-🚬/](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-🚬/).**

In this exercise, we can see a modified version of the synchronization problem for producers and consumers as chefs wait
until the pot is empty and savages wait until the pot is filled. Since we are modifying the original version of the
savages where instead of one chef there will be several chefs who will help with cooking, we also have a barrier
synchronization problem. The barrier synchronizes all the chefs after cooking and the last chef who cooked his part puts
the portions in the pot.

The savages, as in the basic version, use Semaphore full_pot to wait until the pot is full. The savage who stops at this
Semaphore also holds a mutex lock, so the other savages will wait for the mutex. In our modification, we changed
empty_pot Semaphore to Event abstract data type, as we want to signal all chefs to start cooking.

The chefs are waiting for Event empty_pot until the savages signal to them that the pot is empty. Subsequently, the
chefs will start competing/parallel cooking. After cooking, we use a reusable barrier synchronization pattern using the
abstract Event data type, so that the chefs wait for each other and the last one to put the portions in the pot. The
last chef also calls clear() over the empty_pot Event so that the chefs start waiting again until the pot is empty and
signalizes to the savages that they can start eating.

### Pseudocode

Pseudocode wait() barrier function adapted for use in our savages and chefs exercise.

```
INIT mutex Mutex
INIT n as the number of threads needed to wait for each other
INIT counter as the actual number of threads waiting on the barrier
INIT event Event

FUNCTION barrier.wait
    READ empty_pot, full_pot, portions, max_portions
    
    mutex lock for atomic operation
    counter += 1
    // local variable for each thread, thanks to which we can avoid blocking the last thread, which will make clear
    temp_counter = counter
    
    IF counter == n THEN
        counter = 0
        // the last chef puts the cooked portions in the pot...
        portions = max_portions
        empty_pot clear signal the chefs have to wait again until the pot is empty
        full_pot signal for savages to be able to start taking portions of the pot
        event set
        event clear
    ENDIF
    
    mutex unlock
    
    // do not block the thread that made clear
    IF temp_counter != n THEN
        event wait for all threads
    ENDIF
ENDFUNCTION
```

Pseudocode of functions, which we perform from the main function to the threads of savages and chefs.

```
INIT full_pot Semaphore to 0
INIT mutex Mutex
INIT barrier for synchronizing chefs after cooking
INIT empty_pot Event
INIT max_portions
INIT portions for actual number of portions in the pot

FUNCTION savage
    READ mutex, empty_pot, full_pot, portions
    
    WHILE true
        mutex lock for atomic operation
        
        IF portions == 0 THEN
            empty_pot set to signal the chefs that they can start cooking
            full_pot wait for the savage until the pot is full
        ENDIF
        
        // take portion from the pot...
        portions -= 1
        
        mutex unlock
        
        // eating...
    ENDWHILE
ENDFUNCTION


FUNCTION chef
    READ empty_pot, full_pot, portions, max_portions, barrier,
        
    WHILE true
        empty_pot wait wait until the pot is empty
        // cooking...
        barrier.wait(empty_pot, full_pot, portions, max_portions) to synchronize chefs after cooking
    ENDWHILE
ENDFUNCTION
```