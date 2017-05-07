#!/usr/bin/python3

import pygame
import json
import random
import argparse
from copy import copy
from collections import OrderedDict

#_____ Initialisation of the data used by the script.

arg_parser = argparse.ArgumentParser(description='Topographic visualisation of a map.')
arg_parser.add_argument('-m', '--map', default='map.json', help='map file')
arg_parser.add_argument('-c', '--config', default='conf.json', help='config file')
args = arg_parser.parse_args()

with open(args.config) as config_file:
    config_dct = json.load(config_file)

SCREEN_X = config_dct['screen_width']
SCREEN_Y = config_dct['screen_height']
COLOR_VAR = config_dct['color_variation']

colors = {key: value + [0] for key, value in config_dct['colors'].items()}
thresholds = sorted([(int(key), colors[value]) for key, value in config_dct['thresholds'].items()])
COLOR_THRESHOLDS = OrderedDict(thresholds)

del colors, thresholds, config_dct # let's not pollute our global namespace.

#_____ Body of the program where stuff happens.

class Projection:
    """
    Class holding the projection function and its constants.
    """
    const = 0.5
    const2 = const / 2

    @classmethod
    def proj(cls, coos3D: tuple) -> tuple:
        """
        Projection function, turning 3D coordinates of a point to 2D.
        """
        x = -(cls.const * coos3D[0] - cls.const * coos3D[1]) 
        y = -(coos3D[2] + cls.const2 * coos3D[0] + cls.const2 * coos3D[1])
        return (int(x + (SCREEN_X / 2)), int(y + (SCREEN_Y)))

class Map:
    """
    Represent a map to be rendered.
    """

    @staticmethod
    def choose_color(heights: list, thresholds: dict = COLOR_THRESHOLDS) -> pygame.Color:
        """
        For choosing the color of a polygon, we compute the means of the heights of
        the vertex of said polygon, then select the appropriate color in the 'thresholds' global.
        """
        def randomize_color(color: list, variation: int = COLOR_VAR):
            for i in range(3):
                buf = color[i] + random.randint(-variation, variation)
                if buf >= 0 and buf <= 255:
                    color[i] = buf
            return color

        level = sum(heights) / len(heights)
        selected_threshold = max([key for key in sorted(thresholds) if key <= level])
        color = thresholds[selected_threshold]
        color = randomize_color(copy(color))
        return pygame.Color(*color)

    def get_polygons(self) -> None:
        """
        Define the polygons of the map, in the order in which they will be printed.
        """
        polygons = []
        for y in range(self.side - 2, -1, -1):
            for x in range(self.side - 2, - 1, -1):

                pols = [
                    self.projmap[y][x],
                    self.projmap[y + 1][x],
                    self.projmap[y + 1][x + 1],
                    self.projmap[y][x + 1]
                ]

                # list of the z-axis values of the vertex of the polygon, for color computation.
                pols_height = [
                    self.heightmap[y][x][2],
                    self.heightmap[y + 1][x][2],
                    self.heightmap[y + 1][x + 1][2],
                    self.heightmap[y][x + 1][2]
                ]
                color = self.choose_color(pols_height)

                polygons.append({
                    'vertices': pols,
                    'color': color
                })
        return polygons

    
    def __init__(self, map_file: str) -> None:

        with open(map_file) as f:
            map_dct = json.load(f)

        self.side = map_dct['side']
        self.step = map_dct['step']

        heightmap = map_dct['heightmap']
        heightmap = [heightmap[x : x + self.side] for x in range(0, len(heightmap), self.side)]
        for y in range(self.side):
            for x in range(self.side):
                heightmap[y][x] = (x * self.step, y * self.step, heightmap[y][x])
        # three dimensional coordinates of the vertex of the mesh to be rendered.
        self.heightmap = heightmap

        # two dimensional coordinates of the vertex projected on the screen.
        self.projmap = [list(range(self.side)) for i in range(self.side)]
        for y in range(self.side):
            for x in range(self.side):
                self.projmap[y][x] = Projection.proj(self.heightmap[y][x])

        self.polygons = self.get_polygons()

    def render_polygons(self, surface: pygame.Surface):
        for pol in self.polygons:
            pygame.draw.polygon(surface, pol['color'], pol['vertices'])

#_____ Execution loop.
            
def main(map_file: str) -> None:
    random.seed()
    pygame.init()
    pygame.display.set_caption('pyfdf')
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

    m = Map(map_file)
    m.render_polygons(screen)
        
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()

if __name__ == '__main__':
    main(args.map)
