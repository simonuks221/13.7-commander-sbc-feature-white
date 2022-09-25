#!./venv/bin/python
import numpy as np
# import matplotlib.pyplot as plt
from time import *
from serial import Serial
from random import randrange
from enum import IntEnum
from time import time
import random
from head import *
from joint import *
from simonoAnimacijos import SongAnimations
import time
import numpy as np
import matplotlib.pyplot as plt

from audio import AudioFile, AudioMic, smooth_fft_values
# from control_socket import ControlSocket

# from examples import argb_strip_example, argb_fft_example, argb_fft_pygame_example

# soc = ControlSocket("My awesome installation", "http://localhost:8080")

debug: bool = True
muzika: bool = True

if not debug:
    s = Serial('/dev/ttyUSB0', 460800)
    # s = Serial('COM7', 460800)
    s.timeout = 0.01

    head_init(s)
    edges_init(allPixels)
    # jointai.append(SegmentJoint([allEdges[0], allEdges[1]]))

    head_draw_all(s, 0, 0, 0)
    head_clear_all(s)
    update_all_argb(s)
    sleep(0.5)
else:
    s = 0

if muzika:
    song = AudioFile('Armors - DOA.wav')
    song.play()
    plt.ion()  # Stop matplotlib windows from blocking

    # Setup figure, axis and initiate plot
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = ax.plot([], [], 'ro-')

while True:
    if not debug:
        response = head_clear_all(s)
        if (response == ResponseStatus.TIMEOUT):
            head_init(s)
            head_draw_all(s, 0, 0, 0)
            head_clear_all(s)
            update_all_argb(s)
            sleep(0.5)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        blinks = random.randint(1, 5)
        duration = random.random()
        full = random.randint(0, 3)
        print(duration)
        blink_EYEMou(s, blinks, r, g, b)
        sleep(0.1)
        if (blinks == 1):
            head_draw_all(s, r, g, b)
            update_all_argb(s)
            sleep(0.1)
        else:
            sleep(0.1)
            draw_all_exc_EyeMou(s, duration, r, g, b)
            sleep(0.1)
        full = random.randint(0, 8)
        if full == 0:
            FlagsUkraine(s)
            sleep(0.1)
        elif full == 1:
            FlagsLTU(s)
            sleep(0.1)

        gen_rand_stripes(s, 5, r, g, b)
        sleep(0.1)

    if muzika:
        SongAnimations(s, song, ln, fig, ax)
