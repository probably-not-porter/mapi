
# IMPORTS
import random
import numpy as np
import json
import math
import random

import string
import random

# PARAMS
WALL = 0
FLOOR = 1
fill_prob = 0.35
generations = 4
# PRINT MAP
def print_map(m):
    for y in m:
        printstr = ""
        for x in y:
            if x == 1: printstr += "[]"
            else: printstr += ".."
        print(printstr)

# OUTPUT JSON
def output_json(m):
    map_id = ''.join(random.choices(string.ascii_letters, k=7))

    json_obj = json.dumps(m, indent=4)
    with open("data/" + map_id + "_map.json", "w") as outpath:
        outpath.write(json_obj)
    return map_id

# CELLULAR AUTOMATA GENERATOR
def gen_map(shape):
    new_map = np.ones(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            choice = random.uniform(0, 1)
            new_map[i][j] = WALL if choice < fill_prob else FLOOR
    for generation in range(generations):
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
    for i in range(new_map.shape[0]):
        row = []
        for j in range(new_map.shape[1]):
            char = 0 if new_map[i][j] == WALL else 1
            #print(char, end='')
            row.append(char)
        #print()
        outmap.append(row)
    return outmap

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


# ITEM DEFS (rarity?)
ITEM_LIST = {
    "1":{
        "name":"Book of Summoning",
        "rarity": 5
    },
    "2":{
        "name":"Book of The Damned",
        "rarity": 5
    },
    "100":{
        "name":"The One Ring",
        "rarity": 5
    },
    "3":{
        "name":"Small Health Potion",
        "rarity": 1
    },
    "4":{
        "name":"Medium Health Potion",
        "rarity": 2
    },
    "5":{
        "name":"Large Health Potion",
        "rarity": 3
    },
    "6":{
        "name":"Wooden Arrow",
        "rarity": 1
    },
    "7":{
        "name":"Steel Knife",
        "rarity": 1
    },
    "8":{
        "name":"Health Potion6",
        "rarity": 1
    },
    "9":{
        "name":"Health Potion7",
        "rarity": 1
    }
}
def gen_item_occurance():
    occurance_out = []
    occurance_rates = {
        0: 1,
        1: 200,
        2: 40,
        3: 10,
        4: 5,
        5: 1
    }
    for key in ITEM_LIST:
        for x in range(occurance_rates[ITEM_LIST[key]["rarity"]]):
            occurance_out.append(ITEM_LIST[key]["name"])
    random.shuffle(occurance_out)
    return occurance_out

# Item creation
def gen_items(x,y,occ):
    NUM_ITEMS = random.randint(2,8)
    ids_out = []
    for x in range(NUM_ITEMS):
        item = occ.pop()
        ids_out.append(item)
    return ids_out

# Entity creation
def gen_entities(x,y):
    return ["default", "default", "default"]


# GENERATE AND POPULATE A SINGLE ROOM AT X,Y
def create_room(x,y,new_map,occ):
    doors = {
        "n": False,
        "s": False,
        "e": False,
        "w": False
    }
    # DOOR DETECTION
    if y > 1: doors["n"] = (new_map[y-1][x] == 1)
    if y < len(new_map[x]) - 2: doors["s"] = (new_map[y+1][x] == 1)
    if x < len(new_map) - 2: doors["e"] = (new_map[y][x+1] == 1)
    if x > 1: doors["w"] = (new_map[y][x-1] == 1)

    

    # Create ROOM OBJECT
    new_room = {
        "x": x,
        "y": y,
        "description": gen_description(x,y,doors),
        "items": gen_items(x,y,occ),
        "entities": gen_entities(x,y),
        "doors": doors
    }
    return new_room

def main(size):
    room_list = {}
    new_map = gen_map((size, size))
    for y in range(len(new_map)):
        for x in range(len(new_map[y])):
            if new_map[y][x] == 1:
                room = create_room(x,y,new_map,gen_item_occurance())
                if (room["doors"]["n"] == True or room["doors"]["s"] == True or room["doors"]["e"] == True or room["doors"]["w"] == True):
                    if y not in room_list: room_list[y] = {}
                    room_list[y][x] = room
    map_id = output_json(room_list)
    return map_id

if __name__=='__main__':
    main()