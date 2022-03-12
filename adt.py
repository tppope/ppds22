from fei.ppds import Mutex, Semaphore, Event


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def switch_on(self, room):
        self.mutex.lock()
        self.counter += 1
        counter = self.counter
        if self.counter == 1:
            room.wait()
        self.mutex.unlock()
        return counter

    def switch_off(self, room):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            room.signal()
        self.mutex.unlock()
