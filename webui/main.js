let port
let writer

const volumeSlider = document.getElementById("volume")
const loadSongButton = document.getElementById("songSelect")
const songUpload = document.getElementById("songfile")
const freeplaycheck = document.getElementById("freeplaycheck")
var uploadedSong
const recentSongPlayButton = document.getElementById("CurrentSong")
var isFreeplay = true


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
        sendCommand("K" + note.k);
        sendCommand("T" + note.t);
        console.log("K" + note.k);
        console.log("T" + note.t);
    }
}

volumeSlider.oninput = v => {
  //  volDisplay.innerText = val + "%";
    sendCommand("V" + volumeSlider.value);
    console.log("V" + volumeSlider.value);
}

/*
songDirSelect.onclick = async() => {
    console.log("Song dir select is working")
        const directoryHandle = await window.showFilePicker();
        document.getElementById("songList").innerHTML = ""
        for await(const entry of directoryHandle.values){
            if(entry.kind == 'file' && entry.name.endsWith('.json')){
                const listItem = document.createElement('li')
                listItem.innerHTML = entry.name

            }
        }
}*/

songUpload.addEventListener('change', (event) => {
    uploadedSong = event.target.files[0]
    recentSongPlayButton.textContent = uploadedSong.name
});

CurrentSong.onclick = async() => {
    try{
    loadAndPlaySong(uploadedSong)
    } catch{
        return
    }
}

freeplaycheck.oninput = f => {
    isFreeplay = !isFreeplay
    sendCommand("F" + isFreeplay);
    console.log("F" + isFreeplay);
}

async function loadAndPlaySong(fileHandle) {
    const file = await fileHandle;
    const contents = await file.text();
    try {
        const songData = JSON.parse(contents);
        console.log("Playing:", fileHandle.name);
        playSong(songData);
    } catch (e) {
        console.error("Error parsing song file", e);
    }
}