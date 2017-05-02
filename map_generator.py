#!/usr/bin/python3

import json
import random
import argparse
from copy import copy
from math import sqrt

arg_parser = argparse.ArgumentParser(description='Generator of maps using perlin noise.')
arg_parser.add_argument('-i', '--side', default=50, help='length of side of map')
arg_parser.add_argument('-t', '--step', default=20, help='step between each vertex of map')
arg_parser.add_argument('-o', '--smoothness', default=25., help='smoothness of the map (more is more smooth)')
arg_parser.add_argument('-e', '--seed', default=None, help='seed for random number generator')
arg_parser.add_argument('-s', '--sea', default=100, help='sea level of the map')
arg_parser.add_argument('-m', '--max', default=250, help='maximum of the map')
args = arg_parser.parse_args()


# Yes, I'm writing my own vectors in 2017.
class Vec2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __mul__(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

def map_gen(size, res, alt_max, sea, interpolation_fn):

    unit = 1./sqrt(2)
    gradient = [
        Vec2D(unit, unit),
        Vec2D(unit, -unit),
        Vec2D(-unit, unit),
        Vec2D(-unit, -unit),
        Vec2D(0., 1.),
        Vec2D(0., -1.),
        Vec2D(1., 0.),
        Vec2D(-1., 0.)
    ]

    # construction of a shuffled list of 512 elements distributed from 0-255
    perms = [i for i in range(256)]
    random.shuffle(perms)
    permutable = [perms[i & 255] for i in range(512)]
    
    def perlin_noise(x: float, y: float):

        x = float(x / res)
        y = float(y / res)
        
        x0, y0 = int(x), int(y)
        i, j = x0 & 255, y0 & 255

        grad1 = gradient[permutable[i + permutable[j]] % len(gradient)]
        grad2 = gradient[permutable[i + permutable[j + 1]] % len(gradient)]
        grad3 = gradient[permutable[i + 1 + permutable[j]] % len(gradient)]
        grad4 = gradient[permutable[i + 1 + permutable[j + 1]] % len(gradient)]

        s = grad1 * (Vec2D(x, y) - Vec2D(x0, y0))
        t = grad4 * (Vec2D(x, y) - Vec2D(x0, y0 + 1))
        u = grad2 * (Vec2D(x, y) - Vec2D(x0 + 1, y0))
        v = grad3 * (Vec2D(x, y) - Vec2D(x0 + 1, y0 + 1))

        mantissa_x = x - x0
        Cx = interpolation_fn(mantissa_x)

        Li1 = s + Cx * (t-s)
        Li2 = u + Cx * (v-u)

        mantissa_y = y - y0
        Cy = interpolation_fn(mantissa_y)
        return Li1 + Cy * (Li2 - Li1)

    ret = []
    for i in range(size):
        for j in range(size):
            #fixme: without the multiplication by 5/7, interval seems to be [-1.3337, 1.3337] instead of [-1, 1]
            p = ((perlin_noise(i + 0.5, j + 0.5) * 5./7.) + 1) * 0.5 * (alt_max)
            p = int(p) - sea
            if p < 0:
                p = 0
            ret.append(p)
    return ret
            
def main(args):
    
    side = args.side
    step = args.step
    seed = args.seed
    smooth = args.smoothness
    sea = args.sea
    alt_max = args.max

    if seed is not None:
        random.seed(seed)

    dict_file = {
        'side': side,
        'step': step
    }
    dict_file['heightmap'] = map_gen(side,
                                     smooth,
                                     alt_max,
                                     sea,
                                     lambda x: (3 * (x ** 2)) - (2 * (x ** 3)))
    json_file = json.dumps(dict_file)
    print(json_file)

if __name__ == '__main__':
    main(args)
    
