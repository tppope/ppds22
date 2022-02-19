def do_increment(shared, mutex):
    """Increment elements which the indicator points to

    :param shared: object with shared variables
    """
    mutex.lock()
    while shared.indicator < len(shared.numbers):
        shared.numbers[shared.indicator] += 1
        shared.indicator += 1
    mutex.unlock()
