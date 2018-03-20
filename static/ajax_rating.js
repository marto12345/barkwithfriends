function fivestar(mul){
    document.getElementById("starvalue").innerHTML = mul;
   // console.log($(this));
    //onsole.log(document.getElementById('org'))
    var v = document.getElementById('org').innerHTML;
    $("#addRatingForm").submit();
    $.get('/ratings/' + v, {}, function (data) {
        //console.log("data: " + data);
        //console.log(document.getElementById('avg'));
        //document.getElementById("count").innerHTML+=1;
        //

    });
    //document.getElementById("id_organizer").value = document.getElementById("org").value;
}
