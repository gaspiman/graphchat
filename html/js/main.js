window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
let finalTranscript = '';
let recognition = new window.SpeechRecognition();

recognition.interimResults = true;
recognition.maxAlternatives = 10;
recognition.continuous = true;

transcriptWindow = document.getElementById("transcript")

recognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';
    for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
            finalTranscript += transcript;
        } else {
            interimTranscript += transcript;
        }
        transcriptWindow.innerHTML += '<p>' + interimTranscript + '</p>'
    }
    call_backend(finalTranscript)
}
recognition.start();

function switch_transcript() {
    $("#transcript").toggle()
}

var last_user_message = ""
var is_recording = true

function call_backend(msg) {
    if (msg == last_user_message) {
        return
    }
    if (msg.length < 3) {
        return
    }
    msg = msg.toLowerCase()
    if (msg.includes("joseph") == true) {
        is_recording = true
        $("#recording_status").addClass("on", 1000).html("RECORDING...")
        return
    }
    if (is_recording == false) {
        return
    }
    is_recording = false
    last_user_message = msg
    $("#recording_status").removeClass("on", 1000).addClass("processing", 1000).html("PROCESSING...")
    var backendAPI = "https://graphchat.westeurope.cloudapp.azure.com/process";
    $.getJSON(backendAPI, {
        message: msg
    }, function (data) {
        hint = data.message
        graph_url = data.url
        draw_graph(hint, graph_url)
        console.log(data)
        return
    });
    setTimeout(function () {
        $("#recording_status").removeClass().html("...")
    }, 2000);
}

function draw_graph(hint, graph_url) {
    $("#hint").html(hint)
    if (graph_url == "") {
        return
    }
    $("#iframe").attr('src', graph_url);
}

function send_chat() {
    text = $('#chat_field').val();
    console.log(text)
    call_backend(text)
}