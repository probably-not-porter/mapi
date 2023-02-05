# <img src="webtool/img/mapi_logo.png">
### <img src="webtool/img/favicon.png"><img src="webtool/img/favicon.png"><img src="webtool/img/favicon.png"> Flask Worldgen API <img src="webtool/img/favicon.png"><img src="webtool/img/favicon.png"><img src="webtool/img/favicon.png">

## Endpoints
- `http://[HOSTNAME]:5000/post_map?gen=[GENERATOR]&size=[SIZE]`
- `http://[HOSTNAME]:5000/get_map?id=[MAPID]`
- `http://[HOSTNAME]:5000/get_generators`
- `http://[HOSTNAME]:5000/get_map_list`

## Generators
`generator.main(size)` - Writes a map file (`abcd_map.json`) and returns an id (`abcd`) to the API.

## Map files
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
            "visibility": 1.0,
            "max_quantity": 4
        }
    },
    "entities": {

    }
}
```