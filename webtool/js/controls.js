function zoomin(){
    current_zoom += 1;
    get_map(id=current_map_id, current_zoom);
}
function zoomout(){
    current_zoom -= 1;
    get_map(id=current_map_id, current_zoom);
}