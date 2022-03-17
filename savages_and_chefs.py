"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the savages and chefs synchronization exercise, where several savages
    take and eat portions from the pot, which are cooked by several chefs when the pot is empty.
"""

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

from adt import Shared


def get_portion_from_pot(savage_id, shared):
    """Removing a portion from the pot.

    :param savage_id: identification number of the savage who takes the portion from the pot
    :param shared: object with shared abstract data types
    """
    print("savage %02d takes a portion" % savage_id)
    shared.portions -= 1


def eat(savage_id):
    """Demonstration like a savage eats

    :param savage_id: identification number of the savage who eats
    """
    print("savage %02d feasts" % savage_id)
    sleep(randint(1, 10) / 100)


def cook(chef_id):
    """Demonstration as a chef cooks.

    :param chef_id: identification number of the chef who cooks
    """
    print("chef %02d cooks" % chef_id)
    sleep(randint(1, 10) / 100)


def savage(savage_id, shared):
    """The savages use this function to demonstrate the synchronization of taking portions from the pot, into which the
    chefs put portions if the pot is empty. Subsequently, they eat the taken portion.

    :param savage_id: identification number of the savage
    :param shared: object with shared abstract data types
    """
    while True:
        shared.mutex.lock()
        if shared.portions == 0:
            shared.empty_pot.set()
            shared.full_pot.wait()
        get_portion_from_pot(savage_id, shared)
        shared.mutex.unlock()
        eat(savage_id)


def chef(chef_id, shared):
    """The chefs use this function to demonstrate the chefs cooking synchronization when the savages have eaten all
    the portions in the pot.

    :param chef_id: identification number of the chef
    :param shared: object with shared abstract data types
    """
    while True:
        shared.empty_pot.wait()
        cook(chef_id)
        shared.barrier.wait(chef_id, shared)


def main():
    """Main function of the savage and chefs module.

    """
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
