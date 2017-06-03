#!/usr/bin/python3

"""
A map generator that take way too much command line arguments !
"""

import json
import random
import argparse
import itertools

from noise import noise

arg_parser = argparse.ArgumentParser(description='Generator of maps using perlin noise.')
arg_parser.add_argument('-i', '--side', default=64, help='length of side of map')
arg_parser.add_argument('-t', '--step', default=20, help='step between each vertex of map')
arg_parser.add_argument('-o', '--smoothness', default=15, help='smoothness of the map (more is more smooth)')
arg_parser.add_argument('-e', '--seed', default=None, help='seed for random number generator')
arg_parser.add_argument('-s', '--sea', default=100, help='sea level of the map')
arg_parser.add_argument('-m', '--max', default=130, help='maximum of the map')
args = arg_parser.parse_args()


def treat_map(heightmap: list, side: int, sea: int, alt_max: int) -> list:
    flat_map = list(itertools.chain(*heightmap))
    m_max = max(flat_map)
    m_min = min(flat_map)

    for i in range(len(flat_map)):
        elem = flat_map[i]
        elem = (elem + (-m_min)) * (1. / (-(m_min) + m_max))
        elem = elem * (sea + alt_max)
        elem = elem - sea
        if elem < 0:
            elem = 0
        flat_map[i] = int(elem)

    return flat_map


def main(args):
    side = int(args.side)
    step = int(args.step)
    seed = args.seed
    smoothness = int(args.smoothness)
    sea = int(args.sea)
    alt_max = int(args.max)

    if seed is not None:
        random.seed(seed)

    dict_file = {
        'side': side,
        'step': step
    }

    heightmap = noise(side, smoothness)
    heightmap = treat_map(heightmap, side, sea, alt_max)

    dict_file['heightmap'] = heightmap
    json_file = json.dumps(dict_file)
    print(json_file)


if __name__ == '__main__':
    main(args)
