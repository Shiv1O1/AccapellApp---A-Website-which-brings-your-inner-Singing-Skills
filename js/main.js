var canvas,
    ctx,
    source,
    context,
    analyser,
    fbc_array,
    bar_count,
    bar_pos,
    bar_width,
    bar_height;

var audio = new Audio();

audio.src = "/media/a/vocals.wav/";
audio.controls = true;
audio.loop = false;
audio.autoplay = true;

window.addEventListener(
    "load",
    function() {
        document.getElementById("audio").appendChild(audio);

        context = new AudioContext();
        analyser = context.createAnalyser();
        canvas = document.getElementById("canvas");
        ctx = canvas.getContext("2d");
        source = context.createMediaElementSource(audio);

        canvas.width = window.innerWidth * 0.80;
        canvas.height = window.innerHeight * 0.60;

        source.connect(analyser);
        analyser.connect(context.destination);

        FrameLooper();
    },
    false
);

function FrameLooper() {
    window.RequestAnimationFrame =
        window.requestAnimationFrame(FrameLooper) ||
        window.msRequestAnimationFrame(FrameLooper) ||
        window.mozRequestAnimationFrame(FrameLooper) ||
        window.webkitRequestAnimationFrame(FrameLooper);

    fbc_array = new Uint8Array(analyser.frequencyBinCount);
    bar_count = window.innerWidth / 2;

    analyser.getByteFrequencyData(fbc_array);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FF0000";

    for (var i = 0; i < bar_count; i++) {
        bar_pos = i * 4;
        bar_width = 20;
        bar_height = -fbc_array[i];
        //ctx.fillStyle = "rgb(" + i + ", " + i + ", " + 205 + ")"
        ctx.fillRect(600, canvas.height, bar_width, bar_height);
    }
}