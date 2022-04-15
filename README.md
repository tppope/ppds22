# Parallel programming and distributed systems

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

> **Visit [subject page](https://uim.fei.stuba.sk/predmet/i-ppds) for more info.**

## Objective of the subject

The content of the course is the analysis of various synchronization patterns. Our goal is to offer students the
opportunity to become familiar with various synchronization problems along with their solutions. By synchronization
problems we mean the solution of the coordination of concurrently (perhaps also simultaneously) performed tasks in order
to ensure the integrity of the data with which the individual tasks work; of course, we also demand that a correct
calculation result be achieved.

In the second part of the semester, we focus on some modern areas of programming that are developing rapidly: parallel
calculations on graphics cards and asynchronous programming.

## Organization

1. Introduction to parallel and distributed computing
2. Mutex, multiplex, turnstile, (reusable) barrier
3. Barrier and Fibonacci revisited - Producer-consumer, readers-writers, turnstile
4. Readers / writers again - Evening philosophers
5. Smokers, savages, scoreboard
6. Barber, H20, crossing the river, caterpillar track
7. Co-programs - Iterator, generator and carter in Python
8. Async IO - Async IO in Python
9. CUDA
10. CUDA continues

___

## 8. Exercise

> **For more information about exercise
visit [https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/](https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/)
.**

In this exercise, we demonstrated asynchronous programming using native coroutine in python. We compared the
performance of asynchronous implementation versus the synchronous version of sending an HTTP request to determine if a
number is a prime number and to find the weather in cities.

In the synchronous version, we call the is_prime function for 4 numbers and the get_weather function for 4 cities, and
we measure how long it took.

```python
[is_prime(number) for number in [10_000_000, 10_000_019, 1_000_000_000, 1_000_000_007]]

[get_weather(city) for city in ["Presov", "Praha", "Bratislava", "Nižná Šebastová"]]
```

In the synchronous function is_prime, we made an HTTP request to the url, where the API returned to us whether the
number
we sent as a parameter is a prime number. We also measured how long it took for the response to come.

```python
start_time = time.perf_counter()
print("Start finding out if the number %d is a prime number" % number)
url = "http://api.prime-numbers.io/is-this-number-prime.php?"
"key=1697f41ae498c98f8dad54d1170fd2e1a26e6c2bcceb3ae0a2c6c98505cc73f4"
"&number=" + str(number) + "&include_explanations=false&include_prime_types_list=false&language=english"
is_p = "is"
if requests.get(url).json()["is_prime"] == 'true':
    is_p = "isn't"

end_time = time.perf_counter()
print("Number %d %s prime number -> elapsed: %0.2fs" % (number, is_p, end_time - start_time))
```

In the synchronous function get_weather, we made an HTTP request to the url, where the API returned the weather of the
city, which we sent as a parameter. We also measured how long it took for the response to come.

```python
print("Start finding out weather in %s" % city)
start_time = time.perf_counter()
url = "https://api.openweathermap.org/data/2.5/weather?"
"q=" + city + "&appid=93e4625bc9fe7c718dfe8a36117b9565"
"&units=metric"
response = requests.get(url).json()
end_time = time.perf_counter()
print("Weather in %s is %0.2f°C, %s -> elapsed: %0.2fs" % (
    city, response["main"]["temp"], response["weather"][0]["description"], end_time - start_time))
```

At the output below, we see how synchronously the individual requests were performed and how long it took. The next
request was executed until the answer from the previous one came and thus the whole program lasted 3.63 seconds.

```
Start finding out if the number 10000000 is a prime number
Number 10000000 is prime number -> elapsed: 1.30s
Start finding out if the number 10000019 is a prime number
Number 10000019 isn't prime number -> elapsed: 0.80s
Start finding out if the number 1000000000 is a prime number
Number 1000000000 is prime number -> elapsed: 0.26s
Start finding out if the number 1000000007 is a prime number
Number 1000000007 isn't prime number -> elapsed: 0.28s
Start finding out weather in Presov
Weather in Presov is 8.62°C, overcast clouds -> elapsed: 0.30s
Start finding out weather in Praha
Weather in Praha is 8.17°C, broken clouds -> elapsed: 0.23s
Start finding out weather in Bratislava
Weather in Bratislava is 12.55°C, few clouds -> elapsed: 0.22s
Start finding out weather in Nižná Šebastová
Weather in Nižná Šebastová is 10.83°C, moderate rain -> elapsed: 0.25s
Total elapsed time: 3.63s
```

Subsequently, we converted these functions to asynchronous functions. We used the async/await construction to create
native coroutines. We used asynchronous HTTP requests using the aiohttp library.
In both the synchronous and asynchronous versions, we measure the execution time of requests. The changed is_prime and
get_weather functions are shown below.

```python
start_time = time.perf_counter()
print("Start finding out if the number %d is a prime number" % number)
url = "http://api.prime-numbers.io/is-this-number-prime.php?"
"key=1697f41ae498c98f8dad54d1170fd2e1a26e6c2bcceb3ae0a2c6c98505cc73f4"
"&number=" + str(number) + "&include_explanations=false&include_prime_types_list=false&language=english"
is_p = "is"
async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
        data = await resp.json()
        if data["is_prime"] == 'true':
            is_p = "isn't"

end_time = time.perf_counter()
print("Number %d %s prime number -> elapsed: %0.2fs" % (number, is_p, end_time - start_time))
```

```python
print("Start finding out weather in %s" % city)
start_time = time.perf_counter()
url = "https://api.openweathermap.org/data/2.5/weather?"
"q=" + city + "&appid=93e4625bc9fe7c718dfe8a36117b9565"
"&units=metric"
async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
        data = await resp.json()
        end_time = time.perf_counter()
        print("Weather in %s is %0.2f°C, %s -> elapsed: %0.2fs" % (
            city, data["main"]["temp"], data["weather"][0]["description"], end_time - start_time))
```

Because we execute requests asynchronously, waiting for a request does not block
the function, but suspends its execution until a response is available and control returns to the event loop.

Using the asyncio library, we call the gather function, which runs our functions asynchronously and creates a loop of
events.

```python
await asyncio.gather(*[is_prime(number) for number in [10_000_000, 10_000_019, 1_000_000_000, 1_000_000_007]] +
                      [get_weather(city) for city in ["Presov", "Praha", "Bratislava", "Nižná Šebastová"]])
```

In the output below we see that the whole program lasted much shorter than with the synchronous version. 3.63 seconds
for the synchronous version versus 0.84 seconds for the asynchronous version. We see that neither function waited for a
response and passed control so that another function could execute the request. Subsequently, the program returned
to the places where the response came first. The fact that HTTP requests were executed asynchronously can also be seen
in the fact that the execution of the program took as long as the longest waiting for a response.

```
Start finding out if the number 10000000 is a prime number
Start finding out if the number 10000019 is a prime number
Start finding out if the number 1000000000 is a prime number
Start finding out if the number 1000000007 is a prime number
Start finding out weather in Presov
Start finding out weather in Praha
Start finding out weather in Bratislava
Start finding out weather in Nižná Šebastová
Weather in Praha is 8.35°C, overcast clouds -> elapsed: 0.23s
Weather in Bratislava is 12.52°C, broken clouds -> elapsed: 0.23s
Weather in Presov is 8.62°C, overcast clouds -> elapsed: 0.31s
Number 1000000000 is prime number -> elapsed: 0.31s
Weather in Nižná Šebastová is 10.72°C, light rain -> elapsed: 0.31s
Number 1000000007 isn't prime number -> elapsed: 0.35s
Number 10000000 is prime number -> elapsed: 0.81s
Number 10000019 isn't prime number -> elapsed: 0.83s
Total elapsed time: 0.84s
```