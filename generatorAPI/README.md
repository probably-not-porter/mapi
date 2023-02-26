# MAPI - Worldgen API 
## Endpoints
- `http://[HOSTNAME]:5000/post_map?map=[MAP_GENERATOR]&item=[ITEM_GENERATOR]&entity=[ENTITY_GENERATOR]&size=[SIZE]`
- `http://[HOSTNAME]:5000/get_map?id=[MAPID]`
- `http://[HOSTNAME]:5000/get_generators`
- `http://[HOSTNAME]:5000/get_map_list`

## Map Gen
Map generators generate the actual "maze" structure of a map file.

Must have the following functions:
```py
def main(size):
    return {ROOMS}
def meta():
    return "META STRING"
```
Must output the following object:
```json
{
    "1":{
        "1":{ROOM},
        "2":{ROOM}
    },
    "2":{
        "1":{ROOM},
        "2":{ROOM}
    }
}
```

## Item Gen
Item generators create a set of items for the map, as well as placing items in each of the rooms.

Must have the following functions:
```py
def populate({ROOMS}):
    return {ROOMS WITH ITEMS}

def meta():
    return "META STRING"

def load():
    return {ITEMS}

```
Must output the following object:
```json
{
    "1":{ITEM},
    "2":{ITEM},
    "3":{ITEM}
}
```

## Entity Gen
Entity generators create a set of entities for the map, as well as placing entities in each of the rooms.

Must have the following functions:
```py
def populate({ROOMS}):
    return {ROOMS WITH ENTITIES}

def meta():
    return "META STRING"

def load():
    return {ENTITIES}

```
Must output the following object:
```json
{
    "1":{ENTITIES},
    "2":{ENTITIES},
    "3":{ENTITIES}
}
```

## Map files (Map + Items + Entities + Meta)
```json
{
    "map": {
        "1": {      // y coordinate
            "2": {      // x coordinate (contains room)
                "x": 2,
                "y": 1,
                "description": "room description (Minus items)",
                "items": [ // references for items in room
                    "[itemID]", "[itemID]", "[itemID]" 
                ],
                "entities": [ // references for entities in room
                    "[entityID]","[entityID]","[entityID]" 
                ],
                "doors": { // openings into adjacent rooms
                    "n": false, "s": true, "e": false, "w": false
                }
            },
    },
    "items": {
        "1":{
            "name": "Item Name",
            "id": "Item ID",
            "appearance": "Item appearance",
            "visibility": "Item visibility",
            "description": "Item Description",
            "sprite": "Sprite Reference",
            "volume": 1.1,
            "weight": 7.5,
            "max_quantity": 4,
            "rarity": 1
        }
    },
    "entities": {

    },
    "meta{
        // meta information from generators
    }
}
```