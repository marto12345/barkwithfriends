function alertfunction() {
var end_time= document.getElementById("end").value;
var start_time = document.getElementById("start").value;


var timestart = new Date();
temp = start_time.split(":");
timestart.setHours((parseInt(temp[0]) - 1 + 24) % 24);
timestart.setMinutes(parseInt(temp[1]));

var timeend = new Date();
temp = end_time.split(":");
timeend.setHours((parseInt(temp[0]) - 1 + 24) % 24);
timeend.setMinutes(parseInt(temp[1]));

if (timeend < timestart)

        var para = document.createElement("p");
        var node = document.createTextNode('INVALID TIMES CHOSEN! Start time should be earlier than end time!');
        para.appendChild(node);

        var element = document.getElementById("div1");
        var child = document.getElementById("p1");
        element.insertBefore(para,child);
    return false;


}

function alert1(){
         alert('INVALID TIMES CHOSEN! Start time should be earlier than end time!');
         return false;
}