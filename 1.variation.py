from collections import Counter

from fei.ppds import Thread


class Shared:
    def __init__(self, size):
        self.indicator = 0
        self.zero_numbers = [0] * size


def do_increment(shared):
    while shared.indicator < len(shared.zero_numbers):
        shared.zero_numbers[shared.indicator] += 1
        shared.indicator += 1


shared = Shared(1_000_000)

t1 = Thread(do_increment, shared)
t2 = Thread(do_increment, shared)
t1.join()
t2.join()

counter = Counter(shared.zero_numbers)
print(counter.most_common())
