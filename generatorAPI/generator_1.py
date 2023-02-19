# GENERATOR 1: DFS MAZE
# https://github.com/Jack92829/Maze-Generation/blob/master/ASCII%20Maze/ASCII-Maze.py

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
    "Generator ID": 1
}

class Cell:
    """Cell class that defines each walkable Cell on the grid"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.doors = {# Left, Right, Up, Down
            "w": False,
            "e": False,
            "n": False,
            "s": False
        }


    def getChildren(self, grid: list) -> list:
        """Check if the Cell has any surrounding unvisited Cells that are walkable"""
        a = [(1, 0), (-1,0), (0, 1), (0, -1)]
        children = []
        for y, x in a:
            if self.x+x in [-1, len(grid)] or self.y+y in [len(grid), -1]:
                continue
            
            child = grid[self.y+y][self.x+x]
            if child.visited:
                continue
            children.append(child)
        return children
    
    def printCell(self):
        print("CELL: " + str(self.x) + ", " + str(self.y) + " | " + str(self.doors))

def removeWalls(current: Cell, choice: Cell):
    """Removeing the wall between two Cells"""
    print("\n===REMOVE WALL===")
    print("current: " + str(current.x) + ", " + str(current.y))
    print("choice: " + str(choice.x) + ", " + str(choice.y))
    if choice.x < current.x:     
        current.doors["e"] = True
        choice.doors["w"] = True
    elif choice.x > current.x:
        current.doors["w"] = True
        choice.doors["e"] = True
    elif choice.y < current.y:
        current.doors["s"] = True
        choice.doors["n"] = True
    elif choice.y > current.y:
        current.doors["n"] = True
        choice.doors["s"] = True

def gen_map(shape):
    # Request the user to input a maze size and initialise the maze, stack and initial Cell
    size = shape[0]
    grid = [[Cell(x, y) for x in range(size)] for y in range(size)]
    current = grid[0][0]
    stack = []


    # Main loop to generate the maze
    while True:
        current.visited = True
        children = current.getChildren(grid)

        if children:
            choice = random.choice(children)
            choice.visited = True

            stack.append(current)

            removeWalls(current, choice)

            current = choice
        
        elif stack:
            current = stack.pop()
        else:
            break

    map_obj = {}
    for x in range(len(grid)):
        for y in range(len(grid)):
            if str(y) not in map_obj: map_obj[str(y)] = {}
            map_obj[str(y)][str(x)] = {
                "x": x,
                "y": y,
                "description": "description test",
                "items": ["Item 1", "Item 2"],
                "entities": ["Entities 1", "Entities 2"],
                "doors": grid[x][y].doors
            }
    return map_obj

def main(size):
    ROOMS = gen_map((size, size))
    map_id = GT.output_json(ROOMS, ITEMS, ENTITIES, META) # returns filename id
    return map_id

if __name__=='__main__':
    main()