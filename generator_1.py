# GENERATOR 2: DFS MAZE
# https://github.com/Jack92829/Maze-Generation/blob/master/ASCII%20Maze/ASCII-Maze.py

# IMPORTS
import random
import numpy as np
import math
import random
import gen_tools as GT

# PARAMS
VERSION = "v0.1"
ROOMS = {}
ITEMS = {}
ENTITES = {}
META = { 
    "version": VERSION,
    "Generator ID": -1
}
fill_prob = 0.35
generations = 4

def gen_map(shape):
    return None #room_obj

def main(size):
    ROOMS = gen_map((size, size))
    map_id = GT.output_json(ROOMS, ITEMS, ENTITIES, META) # returns filename id
    return map_id

if __name__=='__main__':
    main()