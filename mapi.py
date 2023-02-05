from datetime import date
from flask import Flask, jsonify, request
import json
import os



# Generators 
# must have a main() function that returns a map object
import generator_0 as g0
GENERATORS = [g0.main]   # gN where N is the api reference for /gen, and the index in the list.

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
        "gen_list": list(range(len(GENERATORS)))
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
    gen = request.args.get('gen')
    size = request.args.get('size')
    print(gen, size)
    #width = request.args.get('width')
    map_id = GENERATORS[int(gen)](int(size))
    data = jsonify({"id":map_id})
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data 


if __name__=='__main__':
    app.run(host="0.0.0.0")
