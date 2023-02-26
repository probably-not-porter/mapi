import random
import string
import json
from datetime import datetime

# PRINT MAP
def print_map(m):
    for y in m:
        printstr = ""
        for x in y:
            if x == 1: printstr += "[]"
            else: printstr += ".."
        print(printstr)

# OUTPUT JSON
def output_json(m = {},i = {}, e = {}, meta = {}):
    map_id = ''.join(random.choices(string.ascii_letters, k=7))
    now = datetime.now()
    meta["timestring"] = now.strftime("%d/%m/%Y %H:%M:%S")

    data = {
        "map": m,
        "items": i,
        "entities": e,
        "meta": meta
    }
    json_obj = json.dumps(data, indent=4)
    with open("data/" + map_id + "_map.json", "w") as outpath:
        outpath.write(json_obj)
    return map_id

# READ ITEMS
def read_items():
    items = {}
    return items