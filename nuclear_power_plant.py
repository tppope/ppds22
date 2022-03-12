from random import randint
from time import sleep
from fei.ppds import print, Thread

from adt import Control, Lightswitch


def monitor(monitor_id, control, lightswitch):
    control.data_ready.wait()
    while True:
        control.tourniquet.wait()
        control.tourniquet.signal()

        monitors_count = lightswitch.switch_on(control.data_access)
        reading_duration = randint(40, 50)
        print('monitor "%02d": monitors_count=%02d, reading_duration=%03d\n' %
              (monitor_id, monitors_count, reading_duration))
        sleep(reading_duration / 1000)
        lightswitch.switch_off(control.data_access)


def sensor(sensor_name, control, lightswitch):
    while True:
        sleep(randint(50, 60) / 1000)

        control.tourniquet.wait()

        sensors_count = lightswitch.switch_on(control.data_access)

        control.tourniquet.signal()

        writing_duration = randint(10, 20)
        if sensor_name == "H":
            writing_duration = randint(20, 25)
        print('sensor "%s": sensors_count=%02d, writing_duration=%03d\n' %
              (sensor_name, sensors_count, writing_duration))

        sleep(writing_duration / 1000)

        lightswitch.switch_off(control.data_access)

        control.barrier.wait()

        control.data_ready.set()


if __name__ == "__main__":
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
