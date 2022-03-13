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

> **For more information about exercise visit [https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-🍽%EF%B8%8F/](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-🍽%EF%B8%8F/).**

In this exercise, we will synchronize sensors and operators in a nuclear power plant who read data from the same data
storage through monitors, into which 3 sensors write. Primary circuit coolant flow sensor (P), primary circuit coolant
temperature sensor (T), control rod insertion depth sensor (sensor H). Each sensor has a dedicated space in the common
data storage where it writes data. Each sensor has a dedicated space in the common data storage where it writes data.
Operators are constantly reading data. One data update takes 40 to 50 milliseconds. The sensors write data every 50 to
60 milliseconds, with the P and T sensors taking 10 to 20 milliseconds and the H sensor to take 20 to 25 milliseconds.

### Analysis

For data consistency, we must ensure that monitors cannot read data just when it is the turn of the sensor to write the
new data. The Lightswitch synchronization pattern will help us with that. Monitors and sensors will have their own
lightswitch, thanks to which they will close the room representing the traffic lights. If the first thread of monitors
closes the room, then only the monitors can enter the room and the last one that leaves will release the room. The same
goes for the sensors.

If we use a lightswitch to exclude categories, then one of the categories may be starved. For example, if monitors
always gained access to a room, the sensors would never be able to write new values. We will therefore introduce a
tourniquet represented by a strong traffic light that applies FIFO, so that the threads will be released in the order in
which they were blocked. Since the sensors write every 50 to 60 milliseconds and the monitors read continuously, it is
necessary to favor the sensors at the tourniquet. The monitors will pass through the tourniquet by performing a wait()
and then a signal(), and only then will they try to close the room with a lightswitch. The sensors will not execute a
signal() on the tourniquet until they close the room. This means that the sensor may overtake at a time when the monitor
has executed signal() and was about to close the room. The monitor can no longer overtake it because if the sensor calls
a signal() on the tourniquet, the sensors will already be in the room.

We also use abstract data type Event to give a signal to the monitor at the beginning that all the data has already been
entered into the storage by the sensors, and they can start reading them.

Every 50 to 60 milliseconds, the sensors write data, thus gaining access to the room via a lightswitch. The sensor P and
T takes 10 to 20 milliseconds and the sensor H 20 to 25 milliseconds. Since we assume that the threads run in parallel,
the sensor write will be determined by the thread H write time. Thus, the maximum write time can be 25 milliseconds.
There may be a situation where the sensor threads are not executed in parallel and re-scheduling occurs when performing
to write. As a result, one sensor could write and still wait 50 to 60 milliseconds to re-enter the room while there were
still sensors that had not yet left the room. Therefore, it is necessary that after leaving the room, all the sensors
have to wait for each other and then get the signal to write together again. The synchronization pattern barrier, which
we designed in Exercise 2 and uses the abstract data type Event, will help us with this.

