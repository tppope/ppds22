"""
    Author: Tomas Popik

    This file contains second variation of using mutex lock synchronization while two threads increment elements in
    array with common index indicator. This variation shows finer granularity for critical area.
"""


def do_increment(shared, mutex):
    """Increment elements which the indicator points to

    :param mutex: abstract date type for synchronization
    :param shared: object with shared variables
    """
    while True:
        mutex.lock()
        if shared.indicator >= len(shared.numbers):
            mutex.unlock()
            break
        shared.numbers[shared.indicator] += 1
        shared.indicator += 1
        mutex.unlock()
