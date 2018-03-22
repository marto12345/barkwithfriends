function fivestar(mul){
    document.getElementById("starvalue").innerHTML = mul;
   // console.log($(this));
    //onsole.log(document.getElementById('org'))
    var v = document.getElementById('org').innerHTML;
    //$("#addRatingForm").submit();
    //$.get('/ratings/' + v, {}, function (data) {
        //console.log("data: " + data);
        //console.log(document.getElementById('avg'));
        //document.getElementById("count").innerHTML+=1;
        //

   // });



    //document.getElementById("id_organizer").value = document.getElementById("org").value;
}



function sendAjax(uri) {


    console.log(uri);
        // var comment = document.getElementById('comment').value;
        var comment = document.getElementById('id_comment').value;
        console.log(comment);
        var star_value =  document.getElementById("starvalue").innerHTML;

        $.get(uri+'/rate', {'comment': comment, 'star_value': star_value}, function (data) {
        console.log("data: " + data);
        console.log(data);
        var avg = data['avg'];
        var reviews=data['reviews'];
        //var starsCount= {1:0, 2:0, 3:0, 4:0, 5:0};
        for (i = 1; i < 6; i++) {
            document.getElementById(i).innerHTML = data['rates'][i];
            // avg = 5;
        }
        document.getElementById('avg').innerHTML = avg;
        document.getElementById('reviews').innerHTML = reviews;
        console.log(document.getElementById('avg'));
        load_bars();
        // document.getElementById("count").innerHTML+=1;


   });
}
