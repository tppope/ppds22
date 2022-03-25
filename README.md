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

## 6. Exercise

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/](https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/).**


This exercise will address a similar but somewhat more complex synchronization problem to H2O where we had to wait for 2
molecules of hydrogen and one molecule of oxygen before creating a water molecule. In this problem, we used a mutex not
only to maintain data integrity but also to synchronize threads. After the water molecule was formed, the oxygen
molecule released the mutex so that a new water molecule could begin to form. Our synchronization problem of crossing
hackers and serfs across the river is very similar. The ship has a capacity of 4 and for safety reasons there may be
four hackers or four serfs or two hackers and two serfs on board. Crew members must wait with each other and then one
must declare that the ship can sail. The difference from the H2O synchronization problem is that we knew that the oxygen
thread was one, so he could release the mutex. In our role, we must appoint a captain who will signal that the ship is
filled with four members and can sail. The captain becomes the member who comes to the ship last.

In the main function of the program we will create several threads that will represent hackers and serfs. These threads
will perform functions in an endless cycle that solve the problem of synchronizing the voyage across the river. The
pseudocode below is a modified pseudocode from the lecture [[1]](#1).

```
INIT hackers_count to 0
INIT serfs_count to 0
INIT mutex Mutex
INIT hackers_queue Semaphore to 0
INIT serfs_queue Semaphore to 0
INIT barrier ReusableEventSimpleBarrier
```

It is necessary to initialize the numbers of hackers and serfs to 0 in order to be able to solve the security and
capacity problems of the ship. Initialization of the Mutex, which will not only serve to maintain the integrity of the
data but also to synchronize, giving the last thread (captain) that came to the ship a signal that the ship may be sail
up. Initialize the barrier so that all four threads to be boarded wait for each other. Initialization of the hacker and
serf Semaphore so that we can solve the synchronization of security issues that say that four hackers or four serfs or
two hackers and 2 serfs can go on board.

```
FUNCTION hackers_boating
    READ hackers_count, serfs_count, mutex, hackers_queue, serfs_queue, barrier
    
    // local variable to identify only one captain who will be the last member to board
    is_captain = false
    
    mutex lock
    hackers_count += 1
    IF hackers_count == 4
        is_captain = true
        hackers_count = 0
        hackers_queue signal for 4 waiting hackers
    ELSE IF hackers_count == 2 and serfs_count >= 2
        is_captain = true
        hackers_count = 0
        hackers_queue signal for 2 waiting hackers
        serfs_count -= 2
        serfs_queue signal for 2 waiting serfs
    ELSE
        mutex unlock   
    ENDIF
    
    hackers_queue wait for another crew members
    
    boarding...
    
    # wait for four members...
    barrier wait for four members
    
    // only the captain can signal to sail and release the mutex so that a new group can board after sail up
    IF is_captain == true
        sail out...
        mutex unlock
    ENDIF   
ENDFUNCTION
```

The pseudocode above shows the function that the hacker threads will perform in the cycle. Each hacker thread has its
local variable is_captain initialized to false. When a hacker thread arrives, which is the fourth hacker thread or the
second in a combination of 2 hackers and 2 serfs, he declares himself captain. Sets the number of hackers to 0 and
signals pending hackers that they can board. In a combination of 2 hackers and 2 serfs, the last hacker thread subtracts
the value 2 from the number of serfs and signalizes the waiting serfs that they can board. Subsequently, if 4 threads of
crew members reach the barrier, the captain announces that the ship can sail and releases the mutex so that a new crew
can come to board. The function of serfs looks analogous.

## References

<a id="1">[1]</a>
Matúš Jókay. PPaDS MMXXII.
<a href="https://cdn.discordapp.com/attachments/810800399526395955/956108763016855582/2022-06.holic_h2o_rieka_husenka.pdf">https://cdn.discordapp.com/attachments/810800399526395955/956108763016855582/2022-06.holic_h2o_rieka_husenka.pdf </a>