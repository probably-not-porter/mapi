const api_url = "http://coho.home:5000";
let current_map_id = null;
let current_zoom = 10;

function get_map(id='default', zoom=current_zoom){
            
    document.getElementById("id").innerHTML = "Map #" + id;
    document.getElementById("main-map").innerHTML = ""; //could be loading animation
    
    $.getJSON(api_url + '/get_map?id=' + id, function(data) {
        console.info("--> Successfully retreived map.", data);
        render_map(data, zoom)
    }).fail(function() {
        onfail();
    });
}
function render_map(data, zoom){
    console.info("--> Drawing map...")
    current_map_id = id;
    let map = data.map;
    let wh = Object.keys(map).length; // assume square
    for(y = 1; y <= wh; y++){
        for (x = 1; x <= wh; x++){
            let d = document.createElement("div");
            d.style.width = zoom + "vmin";
            d.style.height = zoom + "vmin";

            

            if (map[y] && map[y][x]){ 
                d.className = "room";

                // set up stat event
                let stat = document.createElement("div");
                stat.innerHTML = "Room " + map[y][x].x + "-" + map[y][x].y + "<br><br>";
                stat.innerHTML += map[y][x].description + "<br><br>";
                
                let itm = "Items: ";
                for (j in map[y][x]["items"]){
                    let item_id = map[y][x]["items"][j];

                    if (data["items"][item_id]){
                        itm += data["items"][item_id]["name"] + "(" + item_id + "), "
                    }
                    else{
                        itm += item_id + ", "
                    }
                }

                let ent = "Entities: ";
                for (j in map[y][x]["entities"]){
                    ent += map[y][x]["entities"][j] + ", "
                }

                stat.innerHTML += "Doors: ";
                stat.innerHTML += "n=" + map[y][x].doors.n + ", ";
                stat.innerHTML += "s=" + map[y][x].doors.s + ", ";
                stat.innerHTML += "e=" + map[y][x].doors.e + ", ";
                stat.innerHTML += "w=" + map[y][x].doors.w + "<br>";



                itm = itm.slice(0, -2) + "."
                ent = ent.slice(0, -2) + "."
                stat.innerHTML += "<br><br>";
                stat.innerHTML += itm;
                stat.innerHTML += "<br><br>";
                stat.innerHTML += ent;
                d.appendChild(stat);

                

                if (map[y][x].doors.n){
                    let door = document.createElement("div");
                    door.className = "door_n";
                    d.appendChild(door);
                }
                if (map[y][x].doors.s){
                    let door = document.createElement("div");
                    door.className = "door_s";
                    d.appendChild(door);
                }
                if (map[y][x].doors.e){
                    let door = document.createElement("div");
                    door.className = "door_e";
                    d.appendChild(door);
                }
                if (map[y][x].doors.w){
                    let door = document.createElement("div");
                    door.className = "door_w";
                    d.appendChild(door);
                }
            }


            else { d.className = "empty" }
            document.getElementById("main-map").appendChild(d)
            
        }
        document.getElementById("main-map").innerHTML += "<br>";
        $(".room").mouseover(function(){
            document.getElementById("stat").innerHTML = $(this).children(":first")[0].innerHTML;
        });
    }
}
function new_map(){
    let map_gen = document.getElementById("map_generator_select").value;
    let item_gen = document.getElementById("item_generator_select").value;
    let entity_gen = document.getElementById("entity_generator_select").value;

    let size = document.getElementById("inp_size").value;
    $.getJSON(api_url + '/post_map?map=' + map_gen + '&item=' + item_gen + '&entity=' + entity_gen + '&size=' + size, function(data) {
        console.info("--> Successfully created new map.", data);
        get_map(data.id);
    }).fail(function() {
        onfail();
    });
}
function get_generators(){
    let size = document.getElementById("inp_size").value;
    $.getJSON(api_url + '/get_generators', function(data) {
        console.info("--> Successfully retreived generators.", data);
        for (x = 0; x < data.map_generators.length; x++){
            let opt = document.createElement("option");
            opt.value = x;
            opt.innerText = data.map_generators[x];
            document.getElementById('map_generator_select').appendChild(opt);
        }
        for (x = 0; x < data.item_generators.length; x++){
            let opt = document.createElement("option");
            opt.value = x;
            opt.innerText = data.item_generators[x];
            document.getElementById('item_generator_select').appendChild(opt);
        }
        for (x = 0; x < data.entity_generators.length; x++){
            let opt = document.createElement("option");
            opt.value = x;
            opt.innerText = data.entity_generators[x];
            document.getElementById('entity_generator_select').appendChild(opt);
        }

    }).fail(function() {
        onfail();
    });
}
get_generators();

function onfail(){
    alert("Somethings gone wrong. Check the console (f11) for more information.");
    console.error("## THEYRE JAMMING THE RADAR ## - The API connection failed. Check that the API is running and that the address in the 'routes.js' file is correct.");
}
//get_map();  