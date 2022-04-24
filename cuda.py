import math

import numpy
from numba import cuda
import cv2 as cv
from tqdm import tqdm


@cuda.jit
def my_kernel_image(image):
    """

    :param image:
    """
    row, column = cuda.grid(2)
    if row < image.shape[0] and column < image.shape[1]:
        pixel = image[row][column]
        intensity = 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]
        if intensity < 100:
            image[row][column] = 0
        else:
            image[row][column] = 255


def get_video_as_array(path):
    """

    :param path:
    :return:
    """
    video = numpy.load(path)['colorImages']
    frames = []
    for i in range(video.shape[3]):
        frames.append(
            cv.resize(cv.cvtColor(numpy.ascontiguousarray(video[:, :, :, i], dtype=numpy.uint8), cv.COLOR_BGR2RGB),
                      (64, 64)))
    return numpy.array(frames)


def save_video_as_mp4(name, video):
    """

    :param name:
    :param video:
    """
    video_output = cv.VideoWriter(name + ".mp4", cv.VideoWriter_fourcc(*'mp4v'), 20, (video.shape[2], video.shape[1]),
                                  True)
    for frame in video:
        video_output.write(frame)
    video_output.release()


def main():
    """

    """
    video = get_video_as_array("Louis_Van_Gaal_0.npz")
    save_video_as_mp4("Louis_Van_Gaal_0-before", video)
    threads_per_block = (32, 32)

    for frame in tqdm(video):
        blocks_per_grid_x = math.ceil(frame.shape[0] / threads_per_block[0])
        blocks_per_grid_y = math.ceil(frame.shape[1] / threads_per_block[1])
        my_kernel_image[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block](frame)

    save_video_as_mp4("Louis_Van_Gaal_0-after", video)


if __name__ == "__main__":
    main()
