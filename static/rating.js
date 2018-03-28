function load_bars() {
    console.log('loading bars');
    var sum=0.0;
    var i;
    var count=0;
    var starsCount= {1:0, 2:0, 3:0, 4:0, 5:0};
    var classnames={1:"bar-1",2:"bar-2",3:"bar-3",4:"bar-4",5:"bar-5"};
    for (i = 1; i < 6; i++) {
        starsCount[i] = document.getElementById(i).innerHTML;
        sum += starsCount[i] * i;
    }
    count = document.getElementById("reviews").innerHTML;
    console.log(count);


    for (i = 1; i < 6; i++) {
        var classname = classnames[i];
        var el = document.getElementsByClassName(classname)[0];
        var y =( starsCount[i] / count) * 100;
        el.style.width = String(y) + "%";
    }
    var number = (sum / count).toFixed(2);
}

