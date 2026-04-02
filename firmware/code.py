import board
import keypad
import digitalio
import audiobusio
import audiocore
import time
import rotaryio
import audiomixer
import usb_cdc

dac = audiobusio.I2SOut(bit_clock=board.GPIO1028_ADC2, word_select=board.GPIO1028_ADC0, data= board.GPIO1028_ADC1)
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channels=1, bits_per_sample=16, samples_per_frame=512)
dac.play(mixer)

rows = [board.GPIO100, board.GPIO101, board.GPIO102]
cols = [board.GPIO103, board.GPIO104, board.GPIO105, board.GPIO106, board.GPIO107, board.GPIO108, board.GPIO109]

wavef0 = open("pianoC", "rb")
wavef1 = open("pianoD", "rb")
wavef2 = open("pianoE", "rb")
wavef3 = open("pianoF", "rb")
wavef4 = open("pianoG", "rb")
wavef5 = open("pianoA", "rb")
wavef6 = open("pianoB", "rb")
wavef7 = open("pianoC1", "rb")

wav0 = audiocore.WaveFile(wavef0)
wav1 = audiocore.WaveFile(wavef1)
wav2 = audiocore.WaveFile(wavef2)
wav3 = audiocore.WaveFile(wavef3)
wav4 = audiocore.WaveFile(wavef4)
wav5 = audiocore.WaveFile(wavef5)
wav6 = audiocore.WaveFile(wavef6)
wav7 = audiocore.WaveFile(wavef7)

SW1 = 9
SW2 = 10
SW3 = 11
SW4 = 12
SW5 = 13
SW6 = 14
SW7 = 15
SW8 = 16
SW9 = 17
SW10 = 18
SW11 = 19
SW12 = 20
SW13 = 21
SW14 = 22
SW15 = 23
SW16 = 24

iswav0Playing = False
iswav1Playing = False
iswav2Playing = False
iswav3Playing = False
iswav4Playing = False
iswav5Playing = False
iswav6Playing = False
iswav7Playing = False

L = []

L[0], = digitalio.DigitalInOut(board.GPIO10)
L[1], = digitalio.DigitalInOut(board.GPIO11)
L[2], = digitalio.DigitalInOut(board.GPIO12)
L[3], = digitalio.DigitalInOut(board.GPIO13)
L[4], = digitalio.DigitalInOut(board.GPIO14)
L[5], = digitalio.DigitalInOut(board.GPIO15)
L[6], = digitalio.DigitalInOut(board.GPIO16)
L[7], = digitalio.DigitalInOut(board.GPIO17)
L[8], = digitalio.DigitalInOut(board.GPIO18)
L[9]  = digitalio.DigitalInOut(board.GPIO19)

nextKeys = []
nextKeyTimes = []

i = 0

encoder = rotaryio.IncrementalEncoder(board.GPIO20, board.GPIO21)

Freeplay = True


ticks = 20.0

currentTime = time.monotonic()


playingTime = 0.2
accuracy = float


usb_cdc.enable(True)

KeyGroups = {
    1:9, 1:17,
    2:10, 2:18,
    3:11, 3:19,
    4:12, 4:20,
    5:13,5:21,
    6:14,6:22,
    7:15, 7:23,
    8:16, 8:24

}

KeyGroupsToLED = {
    1:5,
    2:0,
    3:6,
    4:1,
    5:7,
    6:2,
    7:8,
    8:3
}

matrix = keypad.KeyMatrix(row_pins=(board.GPIO100, board.GPIO101), column_pins=(board.GPIO109, board.GPIO108, board.GPIO107, board.GPIO106, board.GPIO105, board.GPIO104, board.GPIO103, board.GPIO102))

led_off_times = [0.0] * 10
last_activated_led = 0

while True:

    currentTime = time.monotonic()
    event = matrix.events.get()
    position = encoder.position

    if position != enc_pos:
        enc_pos = position
        volume = position/20.0
        volume = max(0.0, min(1.0, volume))
        mixer.voice.level = volume

    if usb_cdc.console.in_waiting > 1:
        raw_data = usb_cdc.console.readline()
        line = str(raw_data, "utf-8").strip()
        line = str(raw_data, "utf-8").strip()
        if line.startswith("V"):
            try:
                new_vol = float(line[1:]) / 100
                mixer.voice[0].level = new_vol
            except:
                pass
        if line.startswith("F"):
            try:
                Freeplay = bool(line[1:])
            except:
                pass
        if line.startswith("K"):
            try:
                #The user puts in key group
                keyGroup = int(line[1:])
                KeyGroupsToLED[keyGroup].value = True
            except:
                pass
        if line.startswith("T"):
            try:
                #user puts the time in seconds.
                duration = float(line[1:])
                nextKeyTimes[i] = duration + currentTime
            except:
                pass



    if Freeplay == False:
        for idx in range(len(L)):
            if led_off_times[idx] != 0 and currentTime >= led_off_times[idx]:
                L[idx].value = False
                led_off_times[idx] = 0


        if event:
            print(event.key_number, event.pressed)
            if Freeplay:
                match event.key_number:
                    case 9:
                        if iswav0Playing == False:
                            mixer.play(wav0)
                            L[5].value = True
                            nWav0 = time.time()
                            iswav0Playing = True
                    case 10:
                        if iswav1Playing == False:
                            mixer.play(wav1)
                            nWav1 = time.time()
                            L[0].value = True
                            iswav1Playing = True
                    case 11:
                        if iswav2Playing == False:
                            mixer.play(wav2)
                            L[6].value = True
                            nWav2 = time.time()
                            iswav2Playing = True
                    case 12:
                        if iswav3Playing == False:
                            mixer.play(wav3)
                            L[1].value = True
                            nWav3 = time.time()
                            iswav3Playing = True
                    case 13:
                        if iswav4Playing == False:
                            mixer.play(wav4)
                            L[7].value = True
                            nWav4 = time.time()
                            iswav4Playing = True
                    case 14:
                        if iswav5Playing == False:
                            mixer.play(wav5)
                            L[2].value = True
                            nWav5 = time.time()
                            iswav5Playing = True
                    case 15:
                        if iswav6Playing == False:
                            mixer.play(wav6)
                            L[8].value = True
                            nWav6 = time.time()
                            iswav6Playing = True
                    case 16:
                        if iswav7Playing == False:
                            mixer.play(wav7)
                            L[3].value = True
                            nWav7 = time.time()
                            iswav7Playing = True
                    case 17:
                        if iswav0Playing == False:
                            mixer.play(wav0)
                            L[5].value = True
                            nWav0 = time.time()
                            iswav0Playing = True
                    case 18:
                        if iswav1Playing == False:
                            mixer.play(wav1)
                            L[0].value = True

                            nWav1 = time.time()
                            iswav1Playing = True
                    case 19:
                        if iswav2Playing == False:
                            mixer.play(wav1)
                            L[6].value = True
                            nWav2 = time.time()
                            iswav2Playing = True
                    case 20:
                        if iswav3Playing == False:
                            mixer.play(wav3)
                            L[1].value = True
                            nWav1 = time.time()
                            iswav3Playing = True
                    case 21:
                        if iswav4Playing == False:
                            mixer.play(wav4)
                            L[7].value = True
                            nWav4 = time.time()
                            iswav4Playing = True
                    case 22:
                        if iswav5Playing == False:
                            mixer.play(wav5)
                            L[2].value = True
                            nWav5 = time.time()
                            iswav5Playing = True
                    case 23:
                        if iswav6Playing == False:
                            mixer.play(wav6)
                            L[8].value = True
                            nWav6 = time.time()
                            iswav6Playing = True
                    case 24:
                        if iswav7Playing == False:
                            mixer.play(wav7)
                            L[3].value = True
                            nWav7 = time.time()
                            iswav7Playing = True
                    case _:
                        print("unknown")
        if iswav0Playing:
            currTime = time.time() - nWav0;
            if currTime >= playingTime:
                mixer.stop(wav0)
                L[5].value = False

        if iswav1Playing:
            currTime = time.time() - nWav1;
            if currTime >= playingTime:
                mixer.stop(wav1)
                L[0].value = False

        if iswav2Playing:
            currTime = time.time() - nWav2;
            if currTime >= playingTime:
                mixer.stop(wav2)
                L[6].value = False
        if iswav3Playing:
            currTime = time.time() - nWav3;
            if currTime >= playingTime:
                mixer.stop(wav3)
                L[1].value = False
        if iswav4Playing:
            currTime = time.time() - nWav4;
            if currTime >= playingTime:
                mixer.stop(wav4)
                L[7].value = False
        if iswav5Playing:
            currTime = time.time() - nWav5;
            if currTime >= playingTime:
                mixer.stop(wav5)
                L[2].value = False
        if iswav6Playing:
            currTime = time.time() - nWav6;
            if currTime >= playingTime:
                mixer.stop(wav6)
                L[8].value = True
        if iswav7Playing:
            currTime = time.time() - nWav7;
            if currTime >= playingTime:
                L[3].value = True
                mixer.stop(wav7)

    while mixer.playing:
        pass