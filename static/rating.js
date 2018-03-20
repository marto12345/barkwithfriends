var averageRating=0.0;
var sum=0.0;
var count=0.0;
var count5=0;
var starsCount= {1:0, 2:0, 3:0, 4:0, 5:0};
var classnames={1:"bar-1",2:"bar-2",3:"bar-3",4:"bar-4",5:"bar-5"}

function fivestar(mul){
   starsCount[mul]+=1;
   count++;
   sum+=mul;
   var numberR=document.getElementById(String(mul));
   numberR.innerHTML=starsCount[mul];
   for(i=1;i<6;i++)
   {
       var classname=classnames[i];
       var el=document.getElementsByClassName(classname)[0];
       var y = starsCount[i]/count*100;
       el.style.width=String(y)+"%";
   }
   var number=(sum/count).toFixed(2);
   document.getElementById("avg").innerHTML=String(number)+" average based on "+String(count)+" reviews";
   //document.getElementById("starvalue").val(mul);
    document.getElementById("id_starvalue").value=mul;
    document.getElementById("id_organizer").value=document.getElementById("org").value;

   
}


