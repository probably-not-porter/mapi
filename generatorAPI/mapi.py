from datetime import date
from flask import Flask, jsonify, request
import json
import os

# Generators 
# must have a main() function that returns a map object
import gen_tools as GT
import map_gen.map_gen_1 as m1
import map_gen.map_gen_2 as m2
import map_gen.map_gen_3 as m3
import item_gen.item_gen_1 as i1
import entity_gen.entity_gen_1 as e1

MAP_GENERATORS = [  # gN where N is the api reference for /gen, and the index in the list.
    [m1, "Cellular Automata Generator"], 
    [m3, "Prim's Algorithm Generator"],
    [m2, "WIP"]
]   
ITEM_GENERATORS = [
    [i1, "Basic Random Item Gen"]
]
ENTITY_GENERATORS = [
    [e1, "Entities 1"]
]

app = Flask(__name__)

@app.route("/get_map_list")
def get_map_list():
    dir_list = os.listdir("data/")
    ob = {
        "map_count": len(dir_list),
        "map_list": dir_list
    }
    data = jsonify(ob)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data

@app.route("/get_generators")
def get_generators():
    ob = {
        "map_generators": list(map(lambda x: x[1:], MAP_GENERATORS)),
        "item_generators": list(map(lambda x: x[1:], ITEM_GENERATORS)),
        "entity_generators": list(map(lambda x: x[1:], ENTITY_GENERATORS))
    }
    data = jsonify(ob)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data

@app.route('/get_map')
def return_map():
    id = request.args.get('id')
    f = open("data/" + id + '_map.json')
    data = jsonify(json.load(f))
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data 

@app.route('/post_map')
def generate_map():
    map_gen = request.args.get('map')
    item_gen = request.args.get('item')
    entity_gen = request.args.get('entity')
    input_size = request.args.get('size')

    map_generator = MAP_GENERATORS[int(map_gen)][0]
    item_generator = ITEM_GENERATORS[int(item_gen)][0]
    entity_generator = ENTITY_GENERATORS[int(entity_gen)][0]

    rooms = map_generator.main(int(input_size)) # size, item generator, entity generator

    rooms = item_generator.populate(rooms)
    items = item_generator.load()

    rooms = entity_generator.populate(rooms)
    entities = entity_generator.load()

    meta = {
        "map_generator": map_generator.meta(),
        "item_generator": item_generator.meta(),
        "entity_generator": entity_generator.meta()
    }
    map_id = GT.output_json(rooms, items, entities, meta)


    data = jsonify({"id":map_id})
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data 


if __name__=='__main__':
    app.run(host="0.0.0.0")
