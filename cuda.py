"""
    Author: Tomas Popik
    License: MIT

    This file contains an implementation of code that demonstrates performing a pixel intensity change in video on
    graphics card cores using a cuda framework. Cuda gives us the impression that the code is executed on a graphics
    card, even though our machine does not have an Nvidia graphics card.
"""

import math

import numpy
from numba import cuda
import cv2 as cv
from tqdm import tqdm
from time import perf_counter


@cuda.jit
def my_kernel_image(image):
    """A function that uses each thread on the graphics card to determine the intensity of the rgb pixel in the image
    that belongs to it thanks to the index calculated by the cuda.grid() function. Consequently, if the intensity is
    less than 100, the pixel sets to black, otherwise white.

    :param image: common image for all threads on the graphics card
    """
    row, column = cuda.grid(2)
    iteration_x = image.size // cuda.blockDim.x
    for i in range(iteration_x):
        x = i * cuda.blockDim.x + row
        if x < image.shape[0]:
            iteration_y = image[x].size // cuda.blockDim.y
            for j in range(iteration_y):
                y = j * cuda.blockDim.y + column
                if y < image.shape[1]:
                    pixel = image[x][y]
                    intensity = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
                    if intensity < 100:
                        image[x][y] = 0
                    else:
                        image[x][y] = 255


def get_video_as_array(path):
    """The function loads the video as an array of images, which converts from BGR to RGB color scale and returns
    array of images in three-dimensional dimension.

    :param path: the path to the video to load
    :return: array of images in three-dimensional dimension
    """
    video = numpy.load(path)['colorImages']
    frames = []
    for i in range(video.shape[3]):
        frames.append(
            cv.resize(cv.cvtColor(numpy.ascontiguousarray(video[:, :, :, i], dtype=numpy.uint8), cv.COLOR_BGR2RGB),
                      (64, 64)))
    return numpy.array(frames)


def save_video_as_mp4(name, video):
    """The function receives the video as an array of three-dimensional images that passes in a loop and writes it as
    a mp4 video.

    :param name: the name of the video to be saved as mp4
    :param video: video to be saved as mp4
    """
    video_output = cv.VideoWriter(name + ".mp4", cv.VideoWriter_fourcc(*'mp4v'), 20, (video.shape[2], video.shape[1]),
                                  True)
    for frame in video:
        video_output.write(frame)
    video_output.release()


def get_streams_for_video(video):
    """This function returns a stream for each frame of the video so that the processing of all frames can run in
    parallel.

    :param video: array of video frames
    :return: stream for each frame of the video
    """
    return [cuda.stream() for _ in range(len(video))]


def get_gpu_data(video, cuda_streams):
    """Transaction of video frames from computer memory to global gpu memory.

    :param video: array of video frames
    :param cuda_streams: stream for each frame of the video
    :return: an array of video frames stored in the global gpu memory
    """
    return [cuda.to_device(video[i], stream=cuda_streams[i]) for i in range(len(video))]


def get_host_data(gpu_data, cuda_streams):
    """Transaction of video frames from the global gpu memory to the computer memory.

    :param gpu_data: array of video frames in global gpu memory
    :param cuda_streams: stream for each frame of the video
    :return: an array of video frames stored in the computer memory
    """
    return numpy.array([gpu_data[i].copy_to_host(stream=cuda_streams[i]) for i in range(len(gpu_data))])


def main():
    """The main function that loads the video and sends its images for processing to a function that will be
    performed on the cores of the graphics card and will change the pixel intensity.

    """
    video = get_video_as_array("Louis_Van_Gaal_0.npz")
    save_video_as_mp4("Louis_Van_Gaal_0-before", video)

    # arrangement of threads in a block
    threads_per_block = (32, 32)

    # get streams for parallel run of multiple image processing kernels
    cuda_streams = get_streams_for_video(video)

    # put video on gpu global storage and get this storage
    gpu_data = get_gpu_data(video, cuda_streams)

    start_time = perf_counter()

    # tqdm to show loading bar in console
    for i in tqdm(range(len(video))):
        # arrangement of blocks in a grid
        blocks_per_grid_x = math.ceil(video[i].shape[0] / threads_per_block[0])
        blocks_per_grid_y = math.ceil(video[i].shape[1] / threads_per_block[1])

        # calling a function that will be performed on the graphics card
        my_kernel_image[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block, cuda_streams[i]](gpu_data[i])

    end_time = perf_counter()

    # get video from gpu global storage
    video = get_host_data(gpu_data, cuda_streams)

    save_video_as_mp4("Louis_Van_Gaal_0-after", video)

    print('Total time: %f' % (end_time - start_time))


if __name__ == "__main__":
    main()
