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
        var star_value =  document.getElementById("starvalue").innerHTML;
        if(star_value==''){
            alert("Please give a star rating.")
            return
        }

        $.get(uri+'/rate', {'comment': comment, 'star_value': star_value}, function (data) {
        var avg = data['avg'];
        var reviews=data['reviews'];

        for (i = 1; i < 6; i++) {
            document.getElementById(i).innerHTML = data['rates'][i];

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


        load_bars();
        document.getElementById('avg').innerHTML = avg;




   });
}
