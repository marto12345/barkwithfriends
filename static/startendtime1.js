function alertfunction() {
    var end_time = document.getElementById("end").value;
    var start_time = document.getElementById("start").value;


    var timestart = new Date();
    temp = start_time.split(":");
    timestart.setHours((parseInt(temp[0]) - 1 + 24) % 24);
    timestart.setMinutes(parseInt(temp[1]));

    var timeend = new Date();
    temp = end_time.split(":");
    timeend.setHours((parseInt(temp[0]) - 1 + 24) % 24);
    timeend.setMinutes(parseInt(temp[1]));

    var diff = (timeend.getTime() - timestart.getTime()) / 1000;
    diff /= 60;
    diff = Math.abs(Math.round(diff));

    if (timeend < timestart) {
        alert('INVALID TIMES CHOSEN! Start time should be earlier than end time!');
        document.getElementById("subm").disabled = true;
    }
    else if (diff < 120) {
        alert("INVALID TIME DURATION!Your event needs to be at least 2 hours long for us to organize it! ")
    }
    else {
        document.getElementById("subm").disabled = false;
    }

}