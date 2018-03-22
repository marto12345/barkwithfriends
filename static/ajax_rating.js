function fivestar(mul){
    document.getElementById("starvalue").innerHTML = mul;

}

function sendAjax(uri) {


    console.log(uri);
        // var comment = document.getElementById('comment').value;
        var comment = document.getElementById('comment').value;
        if(comment==''){
            alert("Please fill out the comment field.")
            return
        }
        //console.log(comment);
        var star_value =  document.getElementById("starvalue").innerHTML;
        if(star_value==''){
            alert("Please give a star rating.")
            return
        }

        $.get(uri+'/rate', {'comment': comment, 'star_value': star_value}, function (data) {
        //console.log("data: " + data);
        //console.log(data);
        var avg = data['avg'];
        var reviews=data['reviews'];
        //var starsCount= {1:0, 2:0, 3:0, 4:0, 5:0};
        for (i = 1; i < 6; i++) {
            document.getElementById(i).innerHTML = data['rates'][i];
            // avg = 5;
        }
        document.getElementById('avg').innerHTML = avg;
        document.getElementById('reviews').innerHTML = reviews;
        document.getElementById('comment').innerHTML='';
        document.getElementById('starvalue').innerHTML='';
        star_value =  document.getElementById("starvalue").innerHTML;
        console.log('star'+star_value)
        comment_div=document.getElementById('comments');
        comment_div.innerHTML='';
        for(i=0; i<data['comments'].length;i++){
              var node=document.createElement('ul');
              node.innerHTML=data['comments'][i];
              comment_div.appendChild(node);
            }

        //console.log(document.getElementById('avg'));
        load_bars();

        // document.getElementById("count").innerHTML+=1;


   });
}
