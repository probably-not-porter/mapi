# GENERATOR 2: PRIMS ALGORITHM
#  https://github.com/ArneStenkrona/MazeFun/blob/master/maze.py

# IMPORTS
import random
import numpy as np
import math
import random
import map_gen.gen_tools as GT
import json
from PIL import Image, ImageColor
import sys

# PARAMS
VERSION = "v0.1"
ROOMS = {}
ITEMS = {}
ENTITIES = {}
META = { 
    "version": VERSION,
    "Generator ID": 2
}

class Cell:
    """Cell class that defines each walkable Cell on the grid"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.weight = random.random()
        self.doors = {# Left, Right, Up, Down
            "w": False,
            "e": False,
            "n": False,
            "s": False
        }

def main(size):
    # ROOMS = gen_map((size, size))
    ROOMS = {}

    m = Maze(size, size, animate=False)

    for y in range(size):
        ROOMS[y] = {}
        for x in range(size):
            if m.grid[x][y] == True:
                c = {
                    "x": x,
                    "y": y,
                    "description": "sample desc",
                    "items": [1,2,3,4],
                    "entities": [1,2,3,4],
                    "doors": {
                        "n": False,
                        "s": False,
                        "e": False,
                        "w": False
                    }
                }
                if y > 1:
                    if m.grid[x][y-1] == True: c["doors"]["n"] = True
                if y < size-1:
                    if m.grid[x][y+1] == True: c["doors"]["s"] = True
                if x < size-1:
                    if m.grid[x+1][y] == True: c["doors"]["e"] = True
                if x > 1:
                    if m.grid[x-1][y] == True: c["doors"]["w"] = True

                ROOMS[y][x] = c
    

    return ROOMS

class Maze:
    """
    A maze data structure, represented as a boolean grid where
    True = Passage
    False = Wall
    """

    def __init__(self, width, height, scale=3, animate=False):
        self._width = width
        self._height = height
        self._scale = scale
        self.grid = np.zeros((width, height), dtype=bool)

        self.__generate(animate)

    def __frontier(self, x, y):
        """
        Returns the frontier of cell (x, y)
              The frontier of a cell are all walls with exact distance two,
              diagonals excluded.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: set of all frontier cells
        """
        f = set()
        if x >= 0 and x < self._width and y >= 0 and y < self._height:
            if x > 1 and not self.grid[x-2][y]:
                f.add((x-2, y))
            if x + 2 < self._width and not self.grid[x+2][y]:
                f.add((x+2, y))
            if y > 1 and not self.grid[x][y-2]:
                f.add((x, y-2))
            if y + 2 < self._height and not self.grid[x][y+2]:
                f.add((x, y+2))

        return f

    def __neighbours(self, x, y):
        """
        Returns the neighbours of cell (x, y)
                 The neighbours of a cell are all passages with exact distance two,
                 diagonals excluded.
           :param x: x coordinate of the cell
           :param y: y coordinate of the cell
           :return: set of all neighbours
           """
        n = set()
        if x >= 0 and x < self._width and y >= 0 and y < self._height:
            if x > 1 and self.grid[x-2][y]:
                n.add((x-2, y))
            if x + 2 < self._width and self.grid[x+2][y]:
                n.add((x+2, y))
            if y > 1 and self.grid[x][y-2]:
                n.add((x, y-2))
            if y + 2 < self._height and self.grid[x][y+2]:
                n.add((x, y+2))

        return n

    def __connect(self, x1, y1, x2, y2):
        """
        Connects wall (x1, x2) with passage (x2 , x2), who
        are assumed to be of distance two from each other
            Connecting a wall to a passage implies converting
            that wall and the wall between them to passages
        :param x1: x coordinate of the wall
        :param y1: y coordinate of the wall
        :param x2: x coordinate of the passage
        :param y2: y coordinate of the passage
        """
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.grid[x1][y1] = True
        self.grid[x][y] = True


    def __generate(self, animate=False):
        """
        Generates a maze using prim's algorithm
        Pseudo code:
        1. All cells are assumed to be walls
        2. Pick cell (x, y) at random and set it to passage
        3. Get frontier fs of (x, y) and add to set s that contains all frontier cells
        4. while s is not empty:
            4a. Pick a random cell (x, y) from s and remove it from s
            4b. Get neighbours ns of (x, y)
            4c. Connect (x, y) with random neighbour (nx, ny) from ns
            4d. Add the frontier fs of (x, y) to s
        :param animate: animate the maze
        """
        s = set()
        x, y = (random.randint(0, self._width - 1), random.randint(0, self._height - 1))
        self.grid[x][y] = True
        fs = self.__frontier(x, y)
        for f in fs:
            s.add(f)
        while s:
            x, y = random.choice(tuple(s))
            s.remove((x, y))
            ns = self.__neighbours(x, y)
            if ns:
                nx, ny = random.choice(tuple(ns))
                self.__connect(x, y, nx, ny)
            fs = self.__frontier(x, y)
            for f in fs:
                s.add(f)

    def get_img(self, pass_colour=(255,255,255), wall_colour=(0,0,0), highlight=None, highlight_colour=(255,0,0)):
        """
        Fetches an image representation of the maze
        :param pass_colour: colour of the passages
        :param wall_colour: colour of the walls
        :param highlight: desired cell to highlight
        :param highligh_colour: colour of highlight
        :return: image of the maze
        """
        im = Image.new('RGB', (self._width, self._height))
        pixels = im.load()
        for x in range(self._width):
            for y in range(self._height):
                if self.grid[x][y]:
                    pixels[x, y] = pass_colour
                else:
                    pixels[x, y] = wall_colour
        if highlight is not None:
            pixels[highlight] = highlight_colour
        return im

    def draw(self, pass_colour=(255, 255, 255), wall_colour=(0, 0, 0), highlight=None, highlight_colour=(255, 0, 0), waitKey=1):
        """
        Draws an image of the maze with cv2.imshow()
        :param pass_colour: colour of the passages
        :param wall_colour: colour of the walls
        :param highlight: desired cell to highlight
        :param highligh_colour: colour of highlight
        :param waitKey: argument to pass to cv2.waitKey()
        """
        img = self.get_img(pass_colour, wall_colour, highlight, highlight_colour).resize((self._width * self._scale, self._height * self._scale)).convert('RGB')
        imcv = np.asanyarray(img)[:,:,::-1].copy()
        cv2.imwrite('maze.png', imcv)    