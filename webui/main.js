let port
let writer

const volumeSlider = document.getElementById("volume")
var songDir = "/Songs"
var loadSongButton = document.getElementById("songSelect")

connectBtn.onclick = async () => {
    try {
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 115200 });
        writer = port.writable.getWriter();
        connectBtn.innerText = "Connected!";
        connectBtn.style.background = "#444";
    } catch (e) {
        console.error("Connection failed", e);
    }
};

async function sendCommand(command) {
    if (writer) {
        const data = new TextEncoder().encode(command + "\n");
        await writer.write(data);
    }
}


async function playSong(songData) {
    for (let note of songData) {
        await new Promise(r => setTimeout(r, note.t));
        sendCommand("S" + note.k);
    }
}

volumeSlider.oninput = v => {
    print(v)
    volDisplay.innerText = val + "%";
    sendCommand("volume" + val);
}


loadSongButton.onclick = async() => {
    try{
        const directoryHandle = await window.showDirectoryPicker();
        
    }
}



