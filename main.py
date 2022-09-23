#!./venv/bin/python
import time
import numpy as np
import matplotlib.pyplot as plt
import asyncio
from time import *
from serial import Serial
from random import randrange
from cube import *
from pyramid import *
from dodecahedron import *
from enum import IntEnum
from time import time
from math import sqrt
import random
from head import *
from joint import *
from simonoAnimacijos import *

from audio import AudioFile, AudioMic, smooth_fft_values
# from control_socket import ControlSocket

# from examples import argb_strip_example, argb_fft_example, argb_fft_pygame_example

# soc = ControlSocket("My awesome installation", "http://localhost:8080")

s = Serial('COM6', 460800)
s.timeout = 0.01


head_init(s, allPixels, jointIndexes)
# apacia galas kaire, nulinis desinej

head_clear_all(s)
head_draw_all(s, 0, 0, 0)
update_all_argb(s)
sleep(0.5)


while True:
    # cube_clear_all(s)
    # update_all_argb(s)
    # sleep(1)
    # DrawJoints(s)
    # RandomStripes(s)
    # RandomDimStripes(s)
    # SongAnimations(s)
    #Flash(s, 5)
    r, g, b = GetNeonColor()
    # head_clear_all(s)
    head_draw_all(s, r, g, b)
    update_all_argb(s)
    # print(get_temperature(s, 1))
    #print(sync_time(s, 1))
    sleep(0.1)
