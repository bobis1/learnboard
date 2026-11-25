import board
import keypad
import digitalio
import audiobusio
import audiocore
import time
import rotaryio
import audiomixer
import usb_cdc

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

# I2S DAC setup
dac = audiobusio.I2SOut(bit_clock=board.GP26, word_select=board.GP27, data=board.GP28)
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1, bits_per_sample=16, buffer_size=512)
dac.play(mixer)

# Keypad matrix pins (2 rows x 8 columns = 16 keys, numbered 0 to 15 by keypad.KeyMatrix)
rows = [board.GP0, board.GP1]
cols = [board.GP9, board.GP8, board.GP7, board.GP6, board.GP5, board.GP4, board.GP3, board.GP2]

# Load WAV files safely (allows button/LED testing even if WAV files are missing)
try:
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
    AUDIO_READY = True
except OSError as e:
    print("WAV files not found, running in button/LED test mode:", e)
    AUDIO_READY = False

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

# 10 LEDs -> Valid indices are L[0] through L[9]
L = [
    digitalio.DigitalInOut(board.GP10),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP13),
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP15),
    digitalio.DigitalInOut(board.GP16),
    digitalio.DigitalInOut(board.GP17),
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP19),
]

for led in L:
    led.direction = digitalio.Direction.OUTPUT

nextKeys = []
nextKeyTimes = []

encoder = rotaryio.IncrementalEncoder(board.GP20, board.GP21)
enc_pos = encoder.position
volume = 0.5

Freeplay = True
ticks = 20.0
currentTime = time.monotonic()
playingTime = 0.2

startTimes = {k: time.monotonic() for k in range(9, 25)}
nWav0 = nWav1 = nWav2 = nWav3 = nWav4 = nWav5 = nWav6 = nWav7 = 0.0

KeyGroups = {
    9: 17,
    10: 18,
    11: 19,
    12: 20,
    13: 21,
    14: 22,
    15: 23,
    16: 24
}

KeyGroupsToLED = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7
}

matrix = keypad.KeyMatrix(row_pins=rows, column_pins=cols, columns_to_anodes=False)

led_off_times = [0.0] * 10
last_activated_led = 0

L[9].value = True

while True:
    currentTime = time.monotonic()
    event = matrix.events.get()
    position = encoder.position

    if position != enc_pos:
        enc_pos = position
        volume = position / 20.0
        volume = max(0.0, min(1.0, volume))
        mixer.voice[0].level = volume

    if usb_cdc.console.in_waiting > 1:
        raw_data = usb_cdc.console.readline()
        line = str(raw_data, "utf-8").strip()
        if line.startswith("V"):
            try:
                new_vol = float(line[1:]) / 100
                mixer.voice[0].level = new_vol
            except ValueError:
                pass
        if line.startswith("F"):
            try:
                Freeplay = bool(int(line[1:]))
            except ValueError:
                pass
        if line.startswith("K"):
            try:
                keyGroup = int(line[1:])
                L[KeyGroupsToLED[keyGroup]].value = True
            except (ValueError, KeyError):
                pass
        if line.startswith("T"):
            try:
                duration = float(line[1:])
                nextKeyTimes.append(duration + currentTime)
            except ValueError:
                pass

    if not Freeplay:
        for idx in range(len(L)):
            if led_off_times[idx] != 0 and currentTime >= led_off_times[idx]:
                L[idx].value = False
                led_off_times[idx] = 0

    if event and event.pressed:
        k = event.key_number + 9
        print("Raw key:", event.key_number, "Mapped SW key:", k)

        if Freeplay:
            if k == 9:
                if not iswav0Playing:
                    L[5].value = True
                    startTimes[9] = currentTime
            elif k == 10:
                if not iswav1Playing:
                    L[0].value = True
                    startTimes[10] = currentTime
            elif k == 11:
                if not iswav2Playing:
                    L[6].value = True
                    startTimes[11] = currentTime
            elif k == 12:
                if not iswav3Playing:
                    L[1].value = True
                    startTimes[12] = currentTime
            elif k == 13:
                if not iswav4Playing:
                    L[7].value = True
                    startTimes[13] = currentTime
            elif k == 14:
                if not iswav5Playing:
                    L[2].value = True
                    startTimes[14] = currentTime
            elif k == 15:
                if not iswav6Playing:
                    L[8].value = True
                    startTimes[15] = currentTime
            elif k == 16:
                if not iswav7Playing:
                    L[3].value = True
                    startTimes[16] = currentTime

            elif k == 17:
                if not iswav0Playing:
                    startTimes[17] = currentTime
                    dt = max(0.001, startTimes[17] - startTimes[9])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav0)
                    L[5].value = True
                    iswav0Playing = True
                    nWav0 = currentTime
            elif k == 18:
                if not iswav1Playing:
                    startTimes[18] = currentTime
                    dt = max(0.001, startTimes[18] - startTimes[10])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav1)
                    L[0].value = True
                    iswav1Playing = True
                    nWav1 = currentTime
            elif k == 19:
                if not iswav2Playing:
                    startTimes[19] = currentTime
                    dt = max(0.001, startTimes[19] - startTimes[11])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav2)
                    L[6].value = True
                    iswav2Playing = True
                    nWav2 = currentTime
            elif k == 20:
                if not iswav3Playing:
                    startTimes[20] = currentTime
                    dt = max(0.001, startTimes[20] - startTimes[12])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav3)
                    L[1].value = True
                    iswav3Playing = True
                    nWav3 = currentTime
            elif k == 21:
                if not iswav4Playing:
                    startTimes[21] = currentTime
                    dt = max(0.001, startTimes[21] - startTimes[13])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav4)
                    L[7].value = True
                    iswav4Playing = True
                    nWav4 = currentTime
            elif k == 22:
                if not iswav5Playing:
                    startTimes[22] = currentTime
                    dt = max(0.001, startTimes[22] - startTimes[14])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav5)
                    L[2].value = True
                    iswav5Playing = True
                    nWav5 = currentTime
            elif k == 23:
                if not iswav6Playing:
                    startTimes[23] = currentTime
                    dt = max(0.001, startTimes[23] - startTimes[15])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav6)
                    L[8].value = True
                    iswav6Playing = True
                    nWav6 = currentTime
            elif k == 24:
                if not iswav7Playing:
                    startTimes[24] = currentTime
                    dt = max(0.001, startTimes[24] - startTimes[16])
                    VelVolum = min(1.0, max(0.0, volume / dt))
                    mixer.voice[0].level = VelVolum
                    if AUDIO_READY:
                        mixer.voice[0].play(wav7)
                    L[3].value = True
                    iswav7Playing = True
                    nWav7 = currentTime

    # Stop note and turn off LED after playingTime (0.2s)
    if iswav0Playing and (currentTime - nWav0 >= playingTime):
        mixer.voice[0].stop()
        L[5].value = False
        iswav0Playing = False
    if iswav1Playing and (currentTime - nWav1 >= playingTime):
        mixer.voice[0].stop()
        L[0].value = False
        iswav1Playing = False
    if iswav2Playing and (currentTime - nWav2 >= playingTime):
        mixer.voice[0].stop()
        L[6].value = False
        iswav2Playing = False
    if iswav3Playing and (currentTime - nWav3 >= playingTime):
        mixer.voice[0].stop()
        L[1].value = False
        iswav3Playing = False
    if iswav4Playing and (currentTime - nWav4 >= playingTime):
        mixer.voice[0].stop()
        L[7].value = False
        iswav4Playing = False
    if iswav5Playing and (currentTime - nWav5 >= playingTime):
        mixer.voice[0].stop()
        L[2].value = False
        iswav5Playing = False
    if iswav6Playing and (currentTime - nWav6 >= playingTime):
        mixer.voice[0].stop()
        L[8].value = False
        iswav6Playing = False
    if iswav7Playing and (currentTime - nWav7 >= playingTime):
        mixer.voice[0].stop()
        L[3].value = False
        iswav7Playing = False
