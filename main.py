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

from audio import AudioFile, AudioMic, smooth_fft_values
# from control_socket import ControlSocket

# from examples import argb_strip_example, argb_fft_example, argb_fft_pygame_example

# soc = ControlSocket("My awesome installation", "http://localhost:8080")

'''
 BOTTOM_BACK = 1
    BOTTOM_FRONT = 2
    SMALL_SIDE = 3
    FACE = 4
    TOP = 5
    BIG_SIDE = 6
'''

BOTTOM_BACK_0 = [21, 27, 27, 20, 26, 30, 30,
                 30, 25, 20, 27, 23, 26, 26, 26, 27, 17,
                 26, 24, 26, 23, 33, 39, 31, 35, 41, 41, 36, 36, 29]

BOTTOM_FRONT_0 = [33, 18, 18, 21, 18, 30, 33, 29,
                  30, 27, 20, 21, 21, 25, 30, 26, 36, 18, 18, 18, 27, 23, 21, 33, 31, 24, 24, 27, 28, 24, 22, 25, 25, 18, 34, 21,
                  24, 25, 25, 18, 29, 22, 18]

SMALL_SIDE_0 = [50, 49, 43, 43, 46, 41, 38, 44, 38, 41]

SMALL_SIDE_1 = [44, 43, 30, 22, 23, 37, 49, 39,
                42, 39, 40, 47, 42, 38, 41, 27, 19, 25, 20]

FACE_0 = [23, 43, 49, 49, 47, 35, 14, 15,
          22, 27, 20, 23, 20, 17, 21, 16, 14, 11, 12, 13, 36, 29, 31, 28, 15, 14, 20, 8, 20, 14, 14, 28, 30]

FACE_1 = [23, 43, 48, 49, 48, 32, 14, 15,
          22, 27, 23, 25, 17, 17, 20, 16, 12, 13, 12, 28, 28, 11, 11, 13, 35, 23]  # BOTTOM FRONT 0

BIG_SIDE_0 = [50, 50, 42, 43, 49, 49,
              49, 48, 41, 38, 44, 37, 41, 42, 37, 35, 37, 41]

BIG_SIDE_1 = [44, 43, 30, 23, 24, 39,
              49, 40, 42, 37, 42, 48, 41, 37, 41, 27, 19, 25, 19]


# ledu skaiciai virsuje teorines reiksmes
did = 49
maz = 43

TOP_1 = [maz + 1, maz, did, did, maz, maz, did,
         did, maz, maz, did, did, maz, maz, did, did, maz, maz]
TOP_0 = [maz + 1, maz, did, did, maz, maz,
         did, maz, maz, did, did, maz, maz, did, did, maz, maz]

BOTTOM_BACK_1 = [27, 26, 30, 30, 30, 24, 20,
                 21, 23, 26, 26, 20, 27, 18, 26, 21, 25, 24, 30, 33, 35, 35, 41, 42, 36, 36, 28]

BOTTOM_FRONT_1 = [16, 25, 27, 29, 37, 27, 19,
                  16, 38, 22,  32, 28, 26, 34, 18, 28, 21, 21, 8, 10, 18, 11, 8, 10, 14, 16, 9, 33, 31, 26, 32, 28, 28, 24, 19, 18, 26, 21, 24, 21, 24, 25, 25, 18, 29, 22, 17]

allPixels = [BOTTOM_BACK_0, BOTTOM_BACK_1, BOTTOM_FRONT_0,
             BOTTOM_FRONT_1, SMALL_SIDE_0, SMALL_SIDE_1, FACE_0, FACE_1, TOP_0, TOP_1, BIG_SIDE_0, BIG_SIDE_1]

jointai: SegmentJoint = []


s = Serial('COM6', 460800)
s.timeout = 0.01


head_init(s, allPixels)
jointai.append(SegmentJoint([allEdges[0], allEdges[1]]))

head_draw_all(s, 0, 0, 0)
head_clear_all(s)
update_all_argb(s)
sleep(0.5)

r = 255
g = 0
b = 50
while False:
    r = random.randint(0, 150)
    g = random.randint(0, 150)
    b = random.randint(0, 150)
    sleep(1)
    for i in range(0, 7):
        head_draw_some(i, 1, s, r, g, b)
        head_draw_some(i, 0, s, r, g, b)
        update_all_argb(s)
        sleep(0.03)
    # cube_color_edge(s, E.TOP_FRONT_FRONT, 255, 0, 0)
# cube_random_all_faces(s)
# update_all_argb(s)
r = 0
g = 0
b = 0
while False:
    # head_draw_some(6, 0, s, 255, 10, 10)

    for i in range(0, len(allEdges)):

        if i % 2 == 0:
            r = 255
            b = 0
        else:
            r = 0
            b = 255

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # head_draw_some(allEdges[i].strips[0][0], allEdges[i].strips[0][1], s, 255, 10, 10)

        head_color_edge(s, i, r, g, b)
    # head_draw_all(s, 255, 10, 10)
    update_all_argb(s)
    sleep(0.5)

while False:
    for j in range(0, len(jointai)):
        print(jointai)
        for ss in range(0, len(jointai[j].strips)):
            head_color_edge_joint(s, jointai[j].strips[ss], 255, 0, 0)
    update_all_argb(s)
    sleep(1)
while False:  # Random red stripes
    head_clear_all(s)
    for r in range(0, 2):
        stripIndexx = random.randint(0, len(allEdges)-6)
        head_color_edge(s, stripIndexx, 255, 0, 0)
        head_color_edge(s, stripIndexx + 5, 255, 0, 0)
    update_all_argb(s)

head_clear_all(s)
head_draw_all(s, 0, 0, 0)
update_all_argb(s)

dimSpeed = 0.2
amountOfStripes = 30

randomBitsHue: float = []
randomBitsIndex: int = []
for i in range(0, amountOfStripes):
    randomBitsIndex.append(0)
    randomBitsHue.append(random.random())


while False:  # Random dim stripes
    for r in range(0, amountOfStripes):

        randomBitsHue[r] -= dimSpeed
        if (randomBitsHue[r] <= 0.1):
            head_color_edge(s, randomBitsIndex[r], 0, 0, 0)
            randomBitsIndex[r] = random.randint(0, len(allEdges)-1)
            randomBitsHue[r] = 1

        hue = rgb2hsv(0, 255, 0)[0]
        head_color_edge(s, randomBitsIndex[r],
                        *hsv2rgb(hue, 1, randomBitsHue[r]))

    update_all_argb(s)
    sleep(0.05)


plt.ion()  # Stop matplotlib windows from blocking

# Setup figure, axis and initiate plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro-')

animation_runtime_s = 5
start_time = time()
animation = 0
animation_count = 10

beat_threshold = 0.5

use_rms = False
song = AudioFile('Armors - DOA.wav')
song.play()

hue = 0

try:

    max_metric = 10
    fft_values = []
    last_time = time()
    while True:

        # Get metric
        if use_rms:
            metric = song.get_rms()
        else:
            new_fft_values = song.get_fft()
            smooth_fft_values(fft_values, new_fft_values, 0.8)
            metric = sum(v for v in fft_values[0:5])
            print(fft_values[0:10])

        # Normalize metric
        max_metric = max(max_metric, metric)
        metric = metric / max_metric

        xdata = np.arange(20)
        ydata = fft_values[0:20]

        ln.set_xdata(xdata)
        ln.set_ydata(ydata)

        ax.relim()
        ax.autoscale_view()

        # Update the window
        fig.canvas.draw()
        fig.canvas.flush_events()
       # print(metric)
       # Visualize
        if metric > 1:
            opacity = 1
        else:
            opacity = metric

        # cube_random_all_faces(s)
        cube_draw_all(s, *hsv2rgb(rgb2hsv(255, 0, 0)[0], 1, opacity))
        update_all_argb(s)
        sleep(0.04)

finally:
    song.terminate()

    # # cube_random_all_faces(s)
    # sleep(5)


# song = AudioFile('Armors - DOA.wav')

# song.play()

# try:
#     max_metric = 0.5
#     fft_values = []
#     while True:
#         # Get metric
#         if use_rms:
#             metric = song.get_rms()
#         else:
#             new_fft_values = song.get_fft()
#             smooth_fft_values(fft_values, new_fft_values, 0.9)
#             metric = sum(v for v in fft_values[50:80])

#         # Normalize metric
#         max_metric = max(max_metric, metric)
#         metric = metric / max_metric


# finally:
#     song.terminate()

# max_metric = 0.5
# fft_values = []
# while True:
#     # Get metric
#     if use_rms:
#         metric = mic.get_rms()
#     else:
#         new_fft_values = mic.get_fft()
#         smooth_fft_values(fft_values, new_fft_values, 0.9)
#         metric = sum(v for v in fft_values[10:80])

#     # Normalize metric
#     max_metric = max(max_metric, metric)
#     metric = metric / max_metric

#     if animation == 0:

#     if animation == 1:

#     if animation == 2:

#     if animation == 3:
#         if metric > beat_threshold:

#     if animation == 4:
#         if metric > beat_threshold:

#     if animation == 5:
#         if metric > beat_threshold:

#     if (start_time + animation_runtime_s) < time():
#         animation += 1
#         if animation >= animation_count:
#             animation = 0


# @soc.animation
# def red():
#     set_argb(s, 0x01, 0x00, 0, 299, 200, 0, 0)

# @soc.animation
# def green():
#     set_argb(s, 0x01, 0x00, 0, 299, 0, 200, 0)

# @soc.animation
# def blue():
#     set_argb(s, 0x01, 0x00, 0, 299, 0, 0, 200)

# @soc.animation
# def random():
#     set_argb(s, 0x01, 0x00, 0, 299, *gen_color())

# @soc.animation
# def stop():
#     clear_argb(s, 0x01, 0x00, 300)

# s = Serial("/dev/ttyUSB0", api.baud_rates[2])
# s.timeout = 0.1

# @soc.animation
# def default():
#     enable_argb(s, 0x01, 0x00, 50)

#     segment = LEDSegment(s, [
#         (0x01, 0x00, 0, 40),
#     ])

#     segment.clear()
#     segment.set_range(0, 10, 255, 0, 0)
#     update_argb(s, 0x01)

#     # song.play()
#     print(list_input_devices())

#     front_color = (255, 255, 0)
#     back_color = (0, 0, 255)
#     use_rms = True
#     try:
#         max_metric = 0.5
#         max_shrink = len(segment) // 3
#         fft_values = []
#         while True:
#             metric = mic.get_rms()
#             # Get metric
#             # if use_rms:
#             #     metric = song.get_rms()
#             # else:
#             #     new_fft_values = song.get_fft()
#             #     smooth_fft_values(fft_values, new_fft_values, 0.9)
#             #     metric = sum(v for v in fft_values[50:80])

#             # Normalize metric
#             max_metric = max(max_metric, metric)
#             metric = metric / max_metric

#             # Visualize
#             shrink = int(metric * max_shrink)
#             segment.clear()
#             segment.set_range(0, len(segment)-1, *back_color)
#             sloped_segment(segment, shrink, len(segment)-1-shrink, front_color, back_color, 6, 3)
#             segment.update()
#     finally:
#         song.terminate()
#         mic.terminate()

# # Delete this when you don't need it
# @soc.animation
# def example():
#     shrinking_segment_example()

# soc.run_animation("default")

# Uncomment this line, so that sbc could connect to central server
# asyncio.run(soc.listen())
