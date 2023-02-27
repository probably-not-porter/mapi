# GENERATOR 2: PRIMS ALGORITHM
#  https://github.com/ArneStenkrona/MazeFun/blob/master/maze.py

# IMPORTS
import random
import numpy as np
import random
from PIL import Image, ImageColor

def gen_map(size):
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

class Maze:
    def __init__(self, width, height, scale=3, animate=False):
        self._width = width
        self._height = height
        self._scale = scale
        self.grid = np.zeros((width, height), dtype=bool)

        self.__generate(animate)

    def __frontier(self, x, y):
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
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.grid[x1][y1] = True
        self.grid[x][y] = True


    def __generate(self, animate=False):
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

def main(size):
    print("--> Generating rooms (map_gen_3)")
    ROOMS = gen_map(size)
    return ROOMS

def meta():
    return "Prim's Algorithm Generator (id-1) - v1"