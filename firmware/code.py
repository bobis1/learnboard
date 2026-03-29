import board
import keypad
import digitalio
import audiobusio
import audiocore
import time

dac = audiobusio.I2SOut(bit_clock=board.GPIO1028_ADC2, word_select=board.GPIO1028_ADC0, data= board.GPIO1028_ADC1)

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

playingTime = 0.25



while True:
    event = matrix.events.get()
    if event:
        print(event.key_number, event.pressed)
        match event.key_number:
            case 9:
                if iswav0Playing == False:
                    dac.play(wav0)
                    nWav0 = time.time()
                    iswav0Playing = True
            case 10:
                if iswav1Playing == False:
                    dac.play(wav0)
                    nWav1 = time.time()
                    iswav1Playing = True
            case 11:
                if iswav2Playing == False:
                    dac.play(wav2)
                    nWav2 = time.time()
                    iswav2Playing = True
            case 12:
                if iswav3Playing == False:
                    dac.play(wav3)
                    nWav3 = time.time()
                    iswav3Playing = True
            case 13:
                if iswav4Playing == False:
                    dac.play(wav4)
                    nWav4 = time.time()
                    iswav4Playing = True
            case 14:
                if iswav5Playing == False:
                    dac.play(wav5)
                    nWav5 = time.time()
                    iswav5Playing = True
            case 15:
                if iswav6Playing == False:
                    dac.play(wav6)
                    nWav6 = time.time()
                    iswav6Playing = True
            case 16:
                if iswav7Playing == False:
                    dac.play(wav7)
                    nWav7 = time.time()
                    iswav7Playing = True
            case 17:
                if iswav0Playing == False:
                    dac.play(wav0)
                    nWav0 = time.time()
                    iswav0Playing = True
            case 18:
                if iswav1Playing == False:
                    dac.play(wav1)
                    nWav1 = time.time()
                    iswav1Playing = True
            case 19:
               if iswav2Playing == False:
                    dac.play(wav1)
                    nWav2 = time.time()
                    iswav2Playing = True
            case 20:
               if iswav3Playing == False:
                    dac.play(wav3)
                    nWav1 = time.time()
                    iswav3Playing = True
            case 21:
               if iswav4Playing == False:
                    dac.play(wav4)
                    nWav4 = time.time()
                    iswav4Playing = True
            case 22:
               if iswav5Playing == False:
                    dac.play(wav5)
                    nWav5 = time.time()
                    iswav5Playing = True
            case 23:
               if iswav6Playing == False:
                    dac.play(wav6)
                    nWav6 = time.time()
                    iswav6Playing = True
            case 24:
                if iswav7Playing == False:
                    dac.play(wav7)
                    nWav7 = time.time()
                    iswav7Playing = True
            case _:
                print("unknown")
    if iswav0Playing:
        currTime = time.time() - nWav0;
        if currTime >= playingTime:
            dac.stop(wav0)
    if iswav1Playing:
        currTime = time.time() - nWav1;
        if currTime >= playingTime:
            dac.stop(wav1)
    if iswav2Playing:
        currTime = time.time() - nWav2;
        if currTime >= playingTime:
            dac.stop(wav2)
    if iswav3Playing:
        currTime = time.time() - nWav3;
        if currTime >= playingTime:
            dac.stop(wav3)
    if iswav4Playing:
        currTime = time.time() - nWav4;
        if currTime >= playingTime:
            dac.stop(wav4)
    if iswav5Playing:
        currTime = time.time() - nWav5;
        if currTime >= playingTime:
            dac.stop(wav5)
    if iswav6Playing:
        currTime = time.time() - nWav6;
        if currTime >= playingTime:
            dac.stop(wav6)
    if iswav7Playing:
        currTime = time.time() - nWav7;
        if currTime >= playingTime:
            dac.stop(wav7)

while dac.playing:
    pass