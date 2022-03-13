
$(document).ready(function(){

    var time = 4;
    setInterval(function() {
    var seconds = time;
    document.getElementById("time").innerHTML = seconds;
    time--;
    if (time < 1){
        document.getElementById("seconds").innerHTML = " second"
    }
    if (time == 0) {
        location.href = "/home";
    }
    }, 1000);

});