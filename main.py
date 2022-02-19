from collections import Counter

from fei.ppds import Thread, Mutex
from matplotlib import pyplot

import first_variation


class Shared:
    """Wrapper of the shared variables among threads"""

    def __init__(self, size):
        """Initialize indicator and set size of array with zero numbers

        :param size: size of numbers array
        """
        self.indicator = 0
        self.numbers = [0] * size


def make_histogram(data):
    """Make histogram and print it in console

    :param data: data for histogram
    """
    counter = Counter(data)
    print("Histogram: %s" % (counter.most_common()))


def make_visual_histogram(data):
    """Make visual histogram and show it in graph

    :param data: data for histogram
    """
    pyplot.hist(x=data)
    pyplot.xticks(range(max(data) + 1))
    pyplot.title('Count of numbers in array')
    pyplot.xlabel('Numbers')
    pyplot.ylabel('Count')
    pyplot.show()


shared = Shared(1_000_000)
mutex = Mutex()
t1 = Thread(first_variation.do_increment, shared, mutex)
t2 = Thread(first_variation.do_increment, shared, mutex)
t1.join()
t2.join()

make_histogram(shared.numbers)
make_visual_histogram(shared.numbers)