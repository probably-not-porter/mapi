import csv
import random

ITEM_URL = '../items/items.csv'
ITEM_MIN = 1
ITEM_MAX = 5

def gen_item_occurance(items):
    occurance_out = []
    occurance_rates = {
        0: 1,
        1: 200,
        2: 40,
        3: 10,
        4: 5,
        5: 1
    }
    for itemid, itemval in items.items():
        occ = occurance_rates[int(itemval["rarity"])]
        for j in range(occ):
            occurance_out.append(itemid)

    random.shuffle(occurance_out)
    print(occurance_out)
    return occurance_out

def load():
    ITEMS = {
    }

    with open(ITEM_URL, 'r') as f:
        reader = csv.reader(f)
        header = True
        for row in reader:
            if header == False:
                ITEMS[row[1]] = {
                    "name":row[0],
                    "id": row[1],
                    "appearance": row[2],
                    "visibility": row[3],
                    "description": row[4],
                    "sprite": row[5],
                    "volume": row[6],
                    "weight": row[7],
                    "max_quantity": row[8],
                    "rarity": row[9]
                }
            else:
                header = False
    return ITEMS

def populate(rooms):
    ITEMS = load()
    occurances = gen_item_occurance(ITEMS)

    for y, yval in rooms.items():
        for x, xval in yval.items():
            for i in range(random.randint(ITEM_MIN, ITEM_MAX)):
                rooms[y][x]["items"].append(occurances.pop())
    return rooms



def meta():
    return "Basic Random Item Gen - v1"