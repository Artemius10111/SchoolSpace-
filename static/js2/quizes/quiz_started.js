
$(document).ready(function(){
    window.onbeforeunload = function() {
        SendData()
        return "Bye now!";
    };
var SendDataCompleted = false
var time_
var minute
var sec 
var url = (window.location.href)
const QuizBox=document.getElementById("quiz_box")

const QuizForm = document.getElementById("quiz_form")
const csrf = document.getElementsByName('csrfmiddlewaretoken')


if(document.getElementById("quiz_box") != null){
    $.ajax({
    type: 'GET',
    url: url.replace('/action/', '/data/'),
    success: function(response){
        const data = new Set(response.data) 
        data.forEach(element => {
            console.log(element)
            for (const [question, answers] of Object.entries(element)){
                QuizBox.innerHTML += `
                <div class="mb-2">
                <hr>
                <h1>${question}</h1>
                
                </div>
                `
                answers.forEach(answer=>{
                    QuizBox.innerHTML += `
                <div>
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for=${question}>${answer}</label>
                </div>
                `
                })
            }
        });
        document.getElementById('quiz_timer').innerHTML = (response.time) + ' : 00'
        var time = response.time
        minute = time - 1;
        sec = 59;
        setInterval(function() {
            if (minute < 1){
                document.getElementById('quiz_timer').style.color = 'red'
            }
            if (sec<10) {
                document.getElementById("quiz_timer").innerHTML = minute + " : 0" + sec;
                sec--;    
            } else {
                document.getElementById("quiz_timer").innerHTML = minute + " : " + sec;
                sec--; 
            }
            if (sec == 00) {
                if (minute == 0) {
                    
                    SendData()
                } else {
            minute --;
            sec = 59; 
                }
            
            if ((minute == 0) && (sec==0)) {
                SendData()
            }}
        }, 1000);
    
    },
    
    error: function(error){
        console.log(error)
    }
    
})
}

            
const SendData = () =>{
    var time_ = `${minute} min and ${sec} sec`
    const elements = [...document.getElementsByClassName("ans")]
    data = {}
    data["time_sign"] = time_
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(element=>{
        if (element.checked) {
            data[element.name] = element.value
        } else{
            if (!data[element.name]){
                data[element.name] = null
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: url.replace('/action/', '/save/'),
        data: data, 
        success: function(response){
            console.log('success!')
        },
        error: function(response){
            console.log(response)
        }
        
    }) 
    SendDataCompleted = true
    var url_redirect = $("#Url").attr("data-url");
    window.location.href = url_redirect
}


QuizForm.addEventListener("submit", element=>{
    window.onbeforeunload = null;
    element.preventDefault()
    SendData()
})
});
