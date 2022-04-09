"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the "first letter capitalized" co-program to demonstrate asynchronous
    programming using generators in python.
"""


def capitalize_first_letter():
    """Function in which a file is opened, and we create generators to which we send lines to capitalize the first
    letter of each word and write it to a new file.

    """
    # generator for write in file
    file_writing = write_file(open("new_text.txt", "w"))
    # generator for capitalize words from file
    capitalize = split_and_capitalize(file_writing)
    # generator for file reading
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
        file_reading.close()


def read_file(capitalize):
    """Function (generator) that reading a file and sending lines to the first letter capitalization function. On
    calling close() on this generator, prints the number of files read and call close() on the capitalize generator.

    :param capitalize: function (generator) for capitalize first letter of words
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
    """Function (generator) that writes capitalized words to an open file and, after calling close() on this
    generator, prints the total number of written words and close opened file.

    :param file: open file for writing
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
    """A function that capitalizes the first letter of words and sends them to the generator for writing. Calling
    close() on this generator prints the number of capitalized words and calls close() on the write generator.

    :param file_writing: function (generator) for write words in file
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
