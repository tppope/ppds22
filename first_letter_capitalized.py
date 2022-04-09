"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the "first letter capitalized" co-program to demonstrate asynchronous
    programming using generators in python.
"""


def capitalize_first_letter():
    """

    """
    file_writing = write_file(open("new_text.txt", "w"))
    capitalize = split_and_capitalize(file_writing)
    file_reading = read_file(capitalize)
    next(file_reading)
    try:
        while True:
            file = open("text.txt", "r")
            file_reading.send(file)
            file.close()
            yield
    except GeneratorExit:
        print("\n----- Fist letter capitalized co-program -----\n")


def read_file(capitalize):
    """

    :param capitalize:
    """
    next(capitalize)
    file_count = 0
    try:
        while True:
            file = yield
            for line in file:
                capitalize.send(line)
            file_count += 1
    except GeneratorExit:
        print("Number of read file: %d" % file_count)
        capitalize.close()


def write_file(file):
    """

    :param file:
    """
    chars_count = 0
    try:
        while True:
            word = yield
            chars_count += len(word)
            file.write(word)
    except GeneratorExit:
        print("Number of written characters: %d" % chars_count)
        file.close()


def split_and_capitalize(file_writing):
    """

    :param file_writing:
    """
    next(file_writing)
    capitalized_words_count = 0
    try:
        while True:
            line = yield
            for word in line.split(" "):
                if "\n" not in word:
                    word += " "
                file_writing.send(word.capitalize())
                capitalized_words_count += 1
    except GeneratorExit:
        print("Number of capitalized words: %d" % capitalized_words_count)
        file_writing.close()
