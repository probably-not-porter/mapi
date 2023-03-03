import csv
import random

ITEM_URL = '../item_data/items.csv'
ITEM_MIN = 1
ITEM_MAX = 5

def gen_item_occurance(items, size):
    occurance_out = []
    occurance_rates = {
        0: 1 * size,
        1: 200 * size,
        2: 40 * size,
        3: 10 * size,
        4: 5 * size,
        5: 1 * size
    }
    for itemid, itemval in items.items():
        occ = occurance_rates[int(itemval["rarity"])]
        for j in range(occ):
            occurance_out.append(itemid)

    random.shuffle(occurance_out)
    return occurance_out

def load():
    print("--> Load Items from CSV (item_gen_1)")
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

def populate(rooms, size):
    print("--> Populate room with items (item_gen_1)")
    ITEMS = load()
    occurances = gen_item_occurance(ITEMS, size)

    for y, yval in rooms.items():
        for x, xval in yval.items():
            for i in range(random.randint(ITEM_MIN, ITEM_MAX)):
                rooms[y][x]["items"].append(occurances.pop())
    return rooms



def meta():
    return "Basic Random Item Gen - v1"