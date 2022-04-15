"""
    Author: Tomas Popik
    License: MIT

    This file contains the implementation of the synchronous version of checking if the numbers are prime numbers and
    finding weather for cities.
"""

import time

import requests


def is_prime(number):
    """Function that makes a request to the API that returns to us whether the number we sent as parameter in the url
    is a prime number or not.

    :param number: number to check if it is a prime number
    """
    start_time = time.perf_counter()
    print("Start finding out if the number %d is a prime number" % number)
    url = "http://api.prime-numbers.io/is-this-number-prime.php?" \
          "key=1697f41ae498c98f8dad54d1170fd2e1a26e6c2bcceb3ae0a2c6c98505cc73f4" \
          "&number=" + str(number) + "&include_explanations=false&include_prime_types_list=false&language=english"
    is_p = "is"
    if requests.get(url).json()["is_prime"] == 'true':
        is_p = "isn't"

    end_time = time.perf_counter()
    print("Number %d %s prime number -> elapsed: %0.2fs" % (number, is_p, end_time - start_time))
    print()


def get_weather(city):
    """Function that makes a request to the API that returns to us weather in city we sent as parameter in the url.

    :param city: the city we are looking for the weather for
    """
    print("Start finding out weather in %s" % city)
    start_time = time.perf_counter()
    url = "https://api.openweathermap.org/data/2.5/weather?" \
          "q=" + city + "&appid=93e4625bc9fe7c718dfe8a36117b9565" \
                        "&units=metric"
    response = requests.get(url).json()
    end_time = time.perf_counter()
    print("Weather in %s is %0.2f°C, %s -> elapsed: %0.2fs" % (
        city, response["main"]["temp"], response["weather"][0]["description"], end_time - start_time))
    print()


def main():
    """Main function.

    """
    [is_prime(number) for number in [10_000_000, 10_000_019, 1_000_000_000, 1_000_000_007]]

    [get_weather(city) for city in ["Presov", "Praha", "Bratislava", "Nižná Šebastová"]]
