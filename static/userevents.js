function getevents(){
    var eventchar = document.getElementById("id_events").value;
    temp = String(eventchar).split(";");
    for (i = 0; i < temp.length; i++) {

        var para = document.createElement("p");
        var node = document.createTextNode(temp[i]);
        para.appendChild(node);

        var element = document.getElementById("div1");
        var child = document.getElementById("p1");
        element.insertBefore(para,child);
        document.getElementById("b").disabled = true;
    }
}