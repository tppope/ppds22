from random import randint
from time import sleep

from fei.ppds import Mutex, Event, Semaphore


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
