function fivestar(mul){
    document.getElementById("starvalue").innerHTML = mul;
   // console.log($(this));
    //onsole.log(document.getElementById('org'))
   // var v = document.getElementById('org').innerHTML;
    //$("#addRatingForm").submit();
    //$.get('/ratings/' + v, {}, function (data) {
        //console.log("data: " + data);
        //console.log(document.getElementById('avg'));
        //document.getElementById("count").innerHTML+=1;
        //

   // });
    //document.getElementById("id_organizer").value = document.getElementById("org").value;
}

function change_values() {
    var comment=document.getElementById('#comment').innerHTML;
    var starvalue=document.getElementById('#starvalue').innerHTML;
    var reviews=document.getElementById('#reviews').innerHTML;
    var avg=document.getElementById('#avg').innerHTML;
    if( comment==''||starvalue==''){
        alert('fill in all fields');
    }else{
        document.getElementById('#reviews').innerHTML=reviews+1;
        document.getElementById('#avg').innerHTML=(avg*reviews+starvalue)/(reviews+1);
        document.getElementById(starvalue)=document.getElementById(starvalue).innerHTML+1;
        document.getElementById('#comment').innerHTML('');
        load_bars();

    }


}
