import csv

ITEM_URL = '../items/items.csv'

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
                    "visibility": row[8],
                    "max_quantity": row[9]
                }
            else:
                header = False
    return ITEMS

def populate(rooms):
    ITEMS = load()
    return rooms



def meta():
    return "Item Gen 1 - v0"