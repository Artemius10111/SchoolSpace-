$(document).ready(function(){
    $.ajax({
        //...        
        success: function(data, textStatus, xhr) {
            console.log(xhr.status);
        },
        complete: function(xhr, textStatus) {
            console.log(xhr.status);
        } 
    });
});