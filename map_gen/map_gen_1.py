# GENERATOR 0: CELLULAR AUTOMATA
# https://medium.com/@yvanscher/cellular-automata-how-to-create-realistic-worlds-for-your-game-2a9ec35f5ba9

# IMPORTS
import random
import numpy as np
import random
from tqdm import tqdm

# PARAMS
WALL = 0
FLOOR = 1
fill_prob = 0.35
generations = 4

# CELLULAR AUTOMATA GENERATOR
def gen_map(shape):
    
    new_map = np.ones(shape)
    print("----> Create grid")
    for i in tqdm(range(shape[0])):
        for j in range(shape[1]):
            choice = random.uniform(0, 1)
            new_map[i][j] = WALL if choice < fill_prob else FLOOR

    print("----> Run cellular automata generations")
    for generation in tqdm(range(generations)):
        for i in range(shape[0]):
            for j in range(shape[1]):
                submap = new_map[max(i-1, 0):min(i+2, new_map.shape[0]),max(j-1, 0):min(j+2, new_map.shape[1])]
                wallcount_1away = len(np.where(submap.flatten() == WALL)[0])
                submap = new_map[max(i-2, 0):min(i+3, new_map.shape[0]),max(j-2, 0):min(j+3, new_map.shape[1])]
                wallcount_2away = len(np.where(submap.flatten() == WALL)[0])
                if generation < 5:
                    if wallcount_1away >= 11 or wallcount_2away <= 13:
                        new_map[i][j] = WALL
                    else:
                        new_map[i][j] = FLOOR
                else:
                    if wallcount_1away >= 11:
                        new_map[i][j] = WALL
                    else:
                        new_map[i][j] = FLOOR
    outmap = []
    print("----> Create output map")
    for i in tqdm(range(new_map.shape[0])):
        row = []
        for j in range(new_map.shape[1]):
            char = 0 if new_map[i][j] == WALL else 1
            #print(char, end='')
            row.append(char)
        #print()
        outmap.append(row)
    room_obj = {}
    print("----> Create door connections")
    for y in tqdm(range(len(outmap))):
        for x in range(len(outmap[y])):
            if outmap[y][x] == 1:
                room = create_room(x,y,outmap)
                if (room["doors"]["n"] == True or room["doors"]["s"] == True or room["doors"]["e"] == True or room["doors"]["w"] == True):
                    if x not in room_obj: room_obj[x] = {}
                    room_obj[x][y] = room
    return room_obj

# Description creation
def gen_description(x,y,doors):
    adj = ["musty", "dusty", "uneven", "unfinished", "bloodstained", "gray", "green", "mossy", "rough", "dry"]
    brightness = ["dark", "bright", "half-lit", "candle-lit", "lantern-lit", "well-lit", "poorly-lit"]
    size = ["large", "modest", "small", "cramped", "vast"]
    length = ["long", "short"]
    noises = ["croaking", "growling", "the wind", "the room creaking", "footsteps", "hushed conversation"]
    optionals = [
        "Water drips from the [adj] ceiling.",
        "You hear the sound of [noises] in the distance.",
        "The sound of [noises] echos in the distance."
    ]
    templates = [
        "You are in a [brightness] room, the walls and floor are [adj] stone.",
        "You are in a [size], [adj] room.",
        "You are in a [length] [brightness] hallway."
    ]
    t = random.choice(templates)
    if random.randint(1,10) > 5: t = t + random.choice(optionals)
    while "[brightness]" in t: 
        t = t.replace("[brightness]", random.choice(brightness), 1)
    while "[adj]" in t: 
        t = t.replace("[adj]", random.choice(adj), 1)
    while "[size]" in t: 
        t = t.replace("[size]", random.choice(size), 1)
    while "[length]" in t: 
        t = t.replace("[length]", random.choice(length), 1)
    while "[noises]" in t: 
        t = t.replace("[noises]", random.choice(noises), 1)
    return t



def create_room(x,y,new_map):
    doors = {
        "n": False,
        "s": False,
        "e": False,
        "w": False
    }
    # Check if there should be doors at each side
    if y > 1: doors["n"] = (new_map[y-1][x] == 1)
    if y < len(new_map[x]) - 2: doors["s"] = (new_map[y+1][x] == 1)
    if x < len(new_map) - 2: doors["e"] = (new_map[y][x+1] == 1)
    if x > 1: doors["w"] = (new_map[y][x-1] == 1)

    # Create ROOM OBJECT
    new_room = {
        "x": x,
        "y": y,
        "description": gen_description(x,y,doors),
        "items": [],
        "entities": [],
        "doors": doors
    }
    return new_room

def main(size):
    print("--> Generating rooms (map_gen_1)")
    rooms = gen_map((size, size))
    return rooms

def meta():
    return "Cellular Automata Generator (id-1) - v1"