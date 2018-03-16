function alertfunction(){
    var eventchar = document.getElementById("events").value;
    temp = eventchar.split(" ");
    for (i = 0; i < temp.length; i++) {
        document.write(temp[i] + "<br >");
    }
}