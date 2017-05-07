
"""
This module implement 2D improved perlin noise.
"""

import random
import numpy as np
from typing import Callable

def interpolation_fn(x: np.float32):
    # f(x) -> 6x^5 - 16x^4 + 10x^3
    return (6 * (x ** 5)) - (15 * (x ** 4)) + (10 * (x ** 3))

def noise(size: int, res: int):

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
    # distributed. This field is enough for resolutions >= 1, but generally,
    # we are going to use only a small subset of this grid.
    vector_field = [[gradients[random.randint(0, len(gradients) - 1)] for i in range(size + 1)]
                  for i in range(size + 1)]
    
    def perlin_noise(x: int, y: int):
        i = x // res
        j = y // res   #
                       # We 'zoom' into the vector field using the given resolution.
        x0 = i * res
        y0 = j * res

        dist_s = np.array([x - x0, y - y0])             #
        dist_t = np.array([x - x0 - res, y - y0])       # We calculate the vectors from the current point
        dist_u = np.array([x - x0, y - y0 - res])       # to the local points of the vector field.
        dist_v = np.array([x - x0 - res, y - y0 - res]) #

        s = vector_field[i][j].dot(dist_s / res)         #
        t = vector_field[i + 1][j].dot(dist_t / res)     # We calculate the dot product of the former vector
        u = vector_field[i][j + 1].dot(dist_u / res)     # by the local points of the vector field.
        v = vector_field[i + 1][j + 1].dot(dist_v / res) #
                
        mantissa_x = (x - x0) / res
        Cx = interpolation_fn(mantissa_x) #
                                          # Then we calculate the interpolation between these dot product
        Li1 = s + Cx * (t - s)            # for the final value of our current point.
        Li2 = u + Cx * (v - u)            #

        mantissa_y = (y - y0) / res
        Cy = interpolation_fn(mantissa_y)
        return Li1 + Cy * (Li2 - Li1)
            
    noise_grid = [[i for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            noise_grid[i][j] = perlin_noise(i, j)

    return noise_grid
