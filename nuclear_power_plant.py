"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the nuclear power plant exercise, where 3 sensors (P, T and H) write
    data to the same memory location, from which 8 operators read. The sensors have their own defined space in which
    to write.
"""

from random import randint
from time import sleep
from fei.ppds import print, Thread

from adt import Control, Lightswitch


def monitor(monitor_id, control, lightswitch):
    """Operators use this function to read data written by sensors. Reading time is 50 to 60 milliseconds.

    :param monitor_id: identification number of operator thread that executes this function
    :param control: object with shared abstract data types
    :param lightswitch: Synchronization pattern to gain access to the shared room between sensors and operators
    """
    # waiting for sensors to enter some data to read...
    control.data_ready.wait()

    while True:
        # tourniquet to prevent starvation
        control.tourniquet.wait()
        control.tourniquet.signal()

        # gain access to the room by first operator thread
        monitors_count = lightswitch.switch_on(control.data_access)

        reading_duration = randint(40, 50)
        print('monitor "%02d": monitors_count=%02d, reading_duration=%03d\n' %
              (monitor_id, monitors_count, reading_duration))
        # reading data...
        sleep(reading_duration / 1000)

        # release access to the room by last operator thread
        lightswitch.switch_off(control.data_access)


def sensor(sensor_name, control, lightswitch):
    """Sensors use this function to write data. Writing time is 10 to 20 milliseconds for P and T sensors, 20 to 25
    milliseconds for H sensor.

    :param sensor_name: identification name (P,T or H) of sensor thread that executes this function
    :param control: object with shared abstract data types
    :param lightswitch: Synchronization pattern to gain access to the shared room between sensors and operators
    """
    while True:
        # waiting for writing...
        sleep(randint(50, 60) / 1000)

        # tourniquet to predict starvation and to favor sensors when they want to write data
        control.tourniquet.wait()

        # gain access to the room by first sensor thread
        sensors_count = lightswitch.switch_on(control.data_access)

        control.tourniquet.signal()

        writing_duration = randint(10, 20)
        if sensor_name == "H":
            writing_duration = randint(20, 25)
        print('sensor "%s": sensors_count=%02d, writing_duration=%03d\n' %
              (sensor_name, sensors_count, writing_duration))
        # writing data...
        sleep(writing_duration / 1000)

        # sensors wait for each other due to different write times
        control.barrier.wait()

        # release access to the room by last sensor thread
        lightswitch.switch_off(control.data_access)

        # signal for operators can read because all sensors have written their data
        control.data_ready.set()


def main():
    synch_control = Control()
    monitor_lightswitch = Lightswitch()
    sensor_lightswitch = Lightswitch()

    p_sensor = Thread(sensor, 'P', synch_control, sensor_lightswitch)
    t_sensor = Thread(sensor, 'T', synch_control, sensor_lightswitch)
    h_sensor = Thread(sensor, 'H', synch_control, sensor_lightswitch)

    operators = [Thread(monitor, i, synch_control, monitor_lightswitch) for i in range(8)]

    p_sensor.join()
    t_sensor.join()
    h_sensor.join()

    [operator.join() for operator in operators]


if __name__ == "__main__":
    main()
