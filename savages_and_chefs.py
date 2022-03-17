from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)


def get_portion_from_pot(savage_id, shared):
    print("savage %2d takes a portion" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("savage %2d feasts" % savage_id)
    sleep(randint(1, 10) / 100)


def savage(savage_id, shared):
    while True:
        shared.mutex.lock()
        if shared.servings == 0:
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_portion_from_pot(savage_id, shared)
        shared.mutex.unlock()
        eat(savage_id)


def put_servings_in_pot(chef_id):
    print("chef %2d cooks" % chef_id)
    sleep(randint(1, 10) / 1000)


def cook(chef_id, max_portions, shared):
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(chef_id)
        shared.servings += max_portions
        shared.full_pot.signal()


def main():
    savages_count = 3
    max_portions = 3
    shared = Shared()

    savages = [Thread(savage, savage_id, shared) for savage_id in range(savages_count)]
    chefs = [Thread(cook, chef_id, max_portions, shared) for chef_id in range(1)]

    for thread in savages + chefs:
        thread.join()


if __name__ == "__main__":
    main()
