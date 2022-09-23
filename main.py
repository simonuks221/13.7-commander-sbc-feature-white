#!./venv/bin/python
import time
import numpy as np
#import matplotlib.pyplot as plt
import asyncio
from time import *
from serial import Serial
from random import randrange
from pyramid import *
from dodecahedron import *
from enum import IntEnum
from time import time
from math import sqrt
import random
from head import *
from joint import *

#from audio import AudioFile, AudioMic, smooth_fft_values
# from control_socket import ControlSocket

# from examples import argb_strip_example, argb_fft_example, argb_fft_pygame_example

# soc = ControlSocket("My awesome installation", "http://localhost:8080")

s = Serial('COM4', 460800)
s.timeout = 0.01


head_init(s, allPixels)
#jointai.append(SegmentJoint([allEdges[0], allEdges[1]]))

head_draw_all(s, 0, 0, 0)
head_clear_all(s)
update_all_argb(s)
sleep(0.5)

while True:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    blinks = random.randint(1, 5)
    duration = random.random()
    full = random.randint(0, 3)
    print(duration)
    blink_EYEMou(s, blinks, r, g, b)
    if (blinks == 1):
        head_draw_all(s, r, g, b)
        update_all_argb(s)
    else:
        draw_all_exc_EyeMou(s, duration, r, g, b)

    gen_rand_stripes(s, 5, r, g, b)
    sleep(0.1)
