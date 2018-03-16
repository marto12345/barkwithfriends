function getevents(){
    var eventchar = document.getElementById("id_events").value;
    temp = String(eventchar).split(";");
    for (i = 0; i < temp.length; i++) {
        document.write(temp[i] + "<br >");
    }
}