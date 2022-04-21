"""
    Author: Tomas Popik
    License: MIT

    This file contains the call of the native coroutines and synchronous version and comparing program execution time.
"""

import asyncio
import asynchronous_version
import synchronous_version
import time


def main():
    start_time = time.perf_counter()
    # synchronous_version.main()
    asyncio.run(asynchronous_version.main())
    end_time = time.perf_counter()
    print("Total elapsed time: %0.2fs" % (end_time - start_time))


if __name__ == "__main__":
    main()
