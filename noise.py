
"""
This module implement 2D improved perlin noise.
"""

import random
import numpy as np


def interpolation_fn(x: float) -> float:
    """
    Interpolation function used for noise generation.
    f(x) -> 6x^5 - 16x^4 + 10x^3
    """
    return (6 * (x ** 5)) - (15 * (x ** 4)) + (10 * (x ** 3))


def perlin_noise(size: int, granularity: int) -> list:
    """
    A homegrown implementation of improved perlin noise.
    Will return a (size * size) 2d list of floats, which are included in the interval [-n, n],
    where n is a value always inferior to 1. Empirically, n is generally between 0.5 and 0.7
    The parameter granularity adjust the granularity of the noise (greater is smoother/less granular).
    """
    unit = 1. / np.sqrt(2.)
    gradients = [                  # The gradients are the eight vectors
        np.array([0, 1]),          # from the center of a square
        np.array([1, 0]),          # to the center of its eight contiguous
        np.array([0, -1]),         # same-size squares.
        np.array([-1, 0]),
        np.array([unit, unit]),
        np.array([unit, -unit]),
        np.array([-unit, -unit]),
        np.array([-unit, unit])
    ]

    # We generate a vector field where the vectors are the gradients, randomly
    # distributed. This field is enough for a granularity >= 1, but generally,
    # we are only going to use a small subset of it.
    vector_field = [[gradients[random.randint(0, len(gradients) - 1)] for i in range(size + 1)]
                    for i in range(size + 1)]

    def noise_in_coordinates(x: int, y: int):
        """
        Calculate the value in the noise_grid at coordinates (x, y).
        """
        i = x // granularity
        j = y // granularity  #
        x0 = i * granularity  # We 'zoom' into the vector field using the given granularity.
        y0 = j * granularity  #

        dist_s = np.array([x - x0, y - y0])                #
        dist_t = np.array([x - x0 - granularity, y - y0])  # We calculate the vectors from the current point
        dist_u = np.array([x - x0, y - y0 - granularity])  # to the local points of the vector field.
        dist_v = np.array([x - x0 - granularity, y - y0 - granularity])

        s = vector_field[i][j].dot(dist_s / granularity)          #
        t = vector_field[i + 1][j].dot(dist_t / granularity)      # We calculate the dot product of the former vectors
        u = vector_field[i][j + 1].dot(dist_u / granularity)      # by the local points of the vector field.
        v = vector_field[i + 1][j + 1].dot(dist_v / granularity)  #

        mantissa_x = (x - x0) / granularity
        Ix = interpolation_fn(mantissa_x)    #
        smooth_a = s + Ix * (t - s)          # Then we calculate the interpolation between these dot product
        smooth_b = u + Ix * (v - u)          # for the final value of our current point.
        mantissa_y = (y - y0) / granularity  #
        Iy = interpolation_fn(mantissa_y)
        return smooth_a + Iy * (smooth_b - smooth_a)

    noise_grid = [[i for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            noise_grid[i][j] = noise_in_coordinates(i, j)

    return noise_grid
