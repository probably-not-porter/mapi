# GENERATOR 2: PRIMS ALGORITHM
# 

# IMPORTS
import random
import numpy as np
import math
import random
import gen_tools as GT
import json

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


def gen_map(shape):
    size = shape[0]
    grid = [[Cell(x, y) for x in range(size)] for y in range(size)]
    current = grid[0][0]

    stack = []

    while True:
        if 
    return map_obj

def main(size):
    ROOMS = gen_map((size, size))
    map_id = GT.output_json(ROOMS, ITEMS, ENTITIES, META) # returns filename id
    return map_id

if __name__=='__main__':
    main()