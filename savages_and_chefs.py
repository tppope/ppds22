from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

from adt import Shared


def get_portion_from_pot(savage_id, shared):
    print("savage %02d takes a portion" % savage_id)
    shared.portions -= 1


def eat(savage_id):
    print("savage %02d feasts" % savage_id)
    sleep(randint(1, 10) / 100)


def cook(chef_id):
    print("chef %02d cooks" % chef_id)
    sleep(randint(1, 10) / 100)


def savage(savage_id, shared):
    while True:
        shared.mutex.lock()
        if shared.portions == 0:
            shared.empty_pot.set()
            shared.full_pot.wait()
        get_portion_from_pot(savage_id, shared)
        shared.mutex.unlock()
        eat(savage_id)


def chef(chef_id, shared):
    while True:
        shared.empty_pot.wait()
        cook(chef_id)
        shared.barrier.wait(chef_id, shared)


def main():
    savages_count = 3
    chefs_count = 3
    max_portions = 3
    shared = Shared(chefs_count, max_portions)

    savages = [Thread(savage, savage_id, shared) for savage_id in range(savages_count)]
    chefs = [Thread(chef, chef_id, shared) for chef_id in range(chefs_count)]

    for thread in savages + chefs:
        thread.join()


if __name__ == "__main__":
    main()
