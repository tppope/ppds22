# Parallel programming and distributed systems

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

> **Visit [subject page](https://uim.fei.stuba.sk/predmet/i-ppds) for more info.**

## Objective of the subject

The content of the course is the analysis of various synchronization patterns. Our goal is to offer students the
opportunity to become familiar with various synchronization problems along with their solutions. By synchronization
issues we mean the solution of the coordination of concurrently (perhaps also simultaneously) performed tasks in order
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

## 9. Exercise

> **For more information about exercise
visit [https://uim.fei.stuba.sk/i-ppds/9-cvicenie-cuda-pomocou-numba/](https://uim.fei.stuba.sk/i-ppds/9-cvicenie-cuda-pomocou-numba/)
.**

In this exercise, we demonstrated performing a pixel intensity change in video on graphics card cores using a cuda
framework. Cuda gives us the impression that the code is executed on the graphics card, even though our machine does not
have an Nvidia graphics card.

The function that we want to be performed on the cores of the graphics card is marked with the decorator @cuda.jit.
Subsequently, we use the function cuda.grid(n) to obtain thread indices in n-dimensional space. The CPU synchronously
reads the images from the video and then calls this function to perform a parallel calculation with the pixels of this
image on the cores of the graphics card.

```python
@cuda.jit
def my_kernel_image(image):
    row, column = cuda.grid(2)
    if row < image.shape[0] and column < image.shape[1]:
        pixel = image[row][column]
        intensity = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
        if intensity < 100:
            image[row][column] = 0
        else:
            image[row][column] = 255
```

The number of threads in one block will be 1024 so that the largest possible part of the device hardware is used for a
given kernel (we consider a maximum of 1024 threads for a multiprocessor). This is also a multiple of 32 because the
warp is size 32 and is the smallest thread scheduling unit on the GPU for CUDA systems. Our 1024 threads will be
arranged in a two-dimensional structure (32, 32) because the image is also two-dimensional. Subsequently, we must
calculate how many such blocks, which hold 1024 threads, we need to process the entire image size (64, 64). We will
generally do the calculation for images of any size. Divide the width of the image by the number of threads in the first
dimension of the block and round it up, and divide the height of the image by the number of threads in the second
dimension of the block and round it up. In our example, it turns out that the blocks will be stored in the structure
(2, 2). The image has 64 * 64 = 4096 pixels, and we have 2 * 2 * 32 * 32 = 4096 threads to process it. Each thread
changes the intensity of one pixel. The change is made competitively so that some threads run in parallel and the CPU
would run in series. Therefore, executing instructions on multiple data over the GPU is much faster.

```python
# arrangement of threads in a block
threads_per_block = (32, 32)

for frame in video:
    # arrangement of blocks in a grid
    blocks_per_grid_x = math.ceil(frame.shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(frame.shape[1] / threads_per_block[1])

    # calling a function that will be performed on the graphics card
    my_kernel_image[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block](frame)
```

Below we see the video before and after processing by our program where we give a bright pixel white and a dark black.

<p align="center">
    <img src="Louis_Van_Gaal_0-before.gif" width="256" height="256" alt="Louis Van Gaal before video processing">
    <img src="Louis_Van_Gaal_0-after.gif" width="256" height="256" alt="Louis Van Gaal after video processing">
</p>