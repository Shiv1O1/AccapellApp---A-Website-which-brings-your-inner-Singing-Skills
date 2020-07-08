var canvas,
    ctx,
    source,
    context,
    analyser,
    fbc_array,
    bar_count,
    bar_pos,
    center_x, 
    center_y, 
    radius,
    x_end,
    y_end,
    bar_width,
    bar_height;

var audio = new Audio();

audio.src = "/media/a/accompaniment.wav";
audio.controls = true;
audio.loop = false;
audio.autoplay = true;

bar_width=2;

window.addEventListener(
    "load",
    function() {
        document.getElementById("audio").appendChild(audio);

        context = new AudioContext();
        analyser = context.createAnalyser();
        canvas = document.getElementById("canvas");
        ctx = canvas.getContext("2d");
        source = context.createMediaElementSource(audio);

        canvas.width = window.innerWidth  * 0.8;
        canvas.height = window.innerHeight * 0.6;

        center_x = canvas.width / 2;
        center_y = canvas.height / 2;
        radius = 150;

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

    // style the background
    var gradient = ctx.createLinearGradient(0,0,0,canvas.height);
    gradient.addColorStop(0,"rgba(35, 7, 77, 1)");
    gradient.addColorStop(1,"rgba(204, 83, 51, 1)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0,0,canvas.width,canvas.height);
        
    //draw a circle
    ctx.beginPath();
    ctx.arc(center_x,center_y,radius,0,2*Math.PI);
    ctx.stroke();

    analyser.getByteFrequencyData(fbc_array);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#ffffff";

    for (var i = 0; i < bar_count; i++) {
        rads = Math.PI * 2 / bar_count;
        bar_height = fbc_array[i]*0.7;

        x = center_x + Math.cos(rads * i) * (radius);
        y = center_y + Math.sin(rads * i) * (radius);
        x_end = center_x + Math.cos(rads * i)*(radius + bar_height);
        y_end = center_y + Math.sin(rads * i)*(radius + bar_height);

        drawBar(x, y, x_end, y_end, bar_width, fbc_array[i])

        //ctx.fillRect(bar_pos, canvas.height, bar_width, bar_height);
    }
}

function drawBar(x1, y1, x2, y2, width,frequency){
    
    var lineColor = "rgb(" + frequency + ", " + frequency + ", " + 205 + ")";
    
    ctx.strokeStyle = lineColor;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
}