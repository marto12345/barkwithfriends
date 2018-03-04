
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
    alert('INVALID TIMES CHOSEN! Start time should be earlier than end time!');
}
