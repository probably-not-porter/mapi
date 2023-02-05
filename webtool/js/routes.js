const api_url = "http://coho.home:5000";


function get_map(id='default'){
            
    document.getElementById("id").innerHTML = "Map #" + id;
    document.getElementById("main-map").innerHTML = ""; //could be loading animation
    
    $.getJSON(api_url + '/get_map?id=' + id, function(data) {
        let map = data.map;
        let wh = Object.keys(map).length; // assume square
        for(y = 1; y <= wh; y++){
            for (x = 1; x <= wh; x++){
                let d = document.createElement("div");
                d.style.width = "10vmin";
                d.style.height = "10vmin";

                

                if (map[y] && map[y][x]){ 
                    d.className = "room";

                    // set up stat event
                    let stat = document.createElement("div");
                    stat.innerHTML = "Room " + map[y][x].x + "-" + map[y][x].y + "<br><br>";
                    stat.innerHTML += map[y][x].description + "<br><br>";
                    
                    let itm = "Items: ";
                    for (j in map[y][x]["items"]){
                        itm += map[y][x]["items"][j] + ", "
                    }
                    itm = itm.slice(0, -2) + "."
                    stat.innerHTML += itm;
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
    }).fail(function() {
        onfail();
    });
}
function new_map(){
    let size = document.getElementById("inp_size").value;
    $.getJSON(api_url + '/post_map?gen=0&size=' + size, function(data) {
        get_map(data.id);
    }).fail(function() {
        onfail();
    });
}
function onfail(){
    alert("Somethings gone wrong. Check the console (f11) for more information.");
    console.error("## THEYRE JAMMING THE RADAR ## - The API connection failed. Check that the API is running and that the address in the 'routes.js' file is correct.");
}
//get_map();  