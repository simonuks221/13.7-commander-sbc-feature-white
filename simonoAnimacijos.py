import time
import numpy as np
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

neonColors = [[199, 36, 177], [77, 77, 255], [224, 231, 34], [
    255, 173, 0], [210, 39, 48], [219, 62, 177], [68, 214, 44]]

r = 255
g = 0
b = 50

neonColorINdex = 0
neonColorINdexNext = 1
neonColorT = 0.1


def GetRandomNeonColor():
    randomas = random.randint(0, len(neonColors) - 1)
    return neonColors[randomas]


def GetNeonColor():
    global neonColorINdex
    global neonColorINdexNext
    global neonColorT

    neonColorT += 0.1

    if (neonColorT >= 1):
        neonColorT = 0.1
        neonColorINdex += 1
        neonColorINdexNext += 1
        if (neonColorINdex == len(neonColors)):
            neonColorINdex = 0
        if (neonColorINdexNext == len(neonColors)):
            neonColorINdexNext = 0
    r = (int)(abs(neonColors[neonColorINdex][0] - neonColors[neonColorINdexNext]
                  [0]) * (neonColorT if neonColors[neonColorINdex][0] < neonColors[neonColorINdexNext][0] else 1 - neonColorT))

    g = (int)(abs(neonColors[neonColorINdex][1] - neonColors[neonColorINdexNext]
                  [1]) * (neonColorT if neonColors[neonColorINdex][1] < neonColors[neonColorINdexNext][1] else 1 - neonColorT))
    b = (int)(abs(neonColors[neonColorINdex][2] - neonColors[neonColorINdexNext]
                  [2]) * (neonColorT if neonColors[neonColorINdex][2] < neonColors[neonColorINdexNext][2] else 1 - neonColorT))
    return (r, g, b)


r = 255
g = 0
b = 50
while False:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    for i in range(0, len(EYE_R)):
        head_color_edge(s, EYE_R[i], r, g, b)
        head_color_edge(s, EYE_L[i], r, g, b)

    for i in range(0, len(MOUTH)):
        head_draw_some(2, 0, s, 0, 0, 0)
        head_color_edge(s, MOUTH[i], r, g, b)
        update_all_argb(s)
        # sleep(0.05)

r = 255
g = 0
b = 60
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


def DrawJoints(s: Serial):
    while True:
        for j in range(0, len(jointai)):

            for ss in range(0, len(jointai[j].strips)):
                head_color_edge_joint(s, jointai[j].strips[ss], 255, 0, 0)
        update_all_argb(s)
        sleep(1)


def RandomStripes(s: Serial):
    # Random red stripes
    head_clear_all(s)
    for r in range(0, 10):
        r, g, b = GetRandomNeonColor()
        stripIndexx = random.randint(0, len(allEdges)-6)
        head_color_edge(s, stripIndexx, r, g, b)
        head_color_edge(s, stripIndexx + 5, r, g, b)


def RandomDimStripes():

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


def Flash(s: Serial, times):
    for i in range(0, times):
        r, g, b = GetRandomNeonColor()
        head_draw_all(s, r, g, b)
        update_all_argb(s)
        sleep(0.05)
        head_clear_all(s)
        update_all_argb(s)
        sleep(0.05)


class SongAnimation(IntEnum):
    NONE = -1
    DRAW_ALL = 0
    DRAW_EYES = 1
    DRAW_MOUTH = 2
    ROLL_ALL = 3
    ROLL_EYES = 4
    ROLL_MOUTH = 5
    DIM = 6
    ALL_RANDOM = 7
    FLASH = 8


lightIndex1 = 1
lightIndex2 = 0


def SongAnimations(s: Serial, song: AudioFile):
    global lightIndex1
    global lightIndex2
    songAnimation = SongAnimation.NONE
    opacity = 1
    useDimming = True
    debug = False

    t = 0

    if True:
        max_metric = 130
        fft_values = []

        # head_clear_all(s)

        if not useDimming:
            opacity = 1
        else:
            new_fft_values = song.get_fft()
            smooth_fft_values(fft_values, new_fft_values, 0.8)
            metric = sum(v for v in fft_values[0: 5])
            opacity = metric / max_metric
            opacity = min(1, opacity)

        # print(metric)
        if (metric > 150):
            songAnimation = SongAnimation.ROLL_ALL
        elif (metric > 70):
            songAnimation = SongAnimation.DRAW_ALL
        else:
            songAnimation = SongAnimation.ALL_RANDOM
        r, g, b = GetNeonColor()
        print(songAnimation, ' ', metric)
        if (not debug):
            head_clear_all(s)
            if (songAnimation == SongAnimation.FLASH):
                Flash(3)
            elif (songAnimation == SongAnimation.DRAW_ALL):

                for i in range(0, len(EYE_R)):
                    head_color_edge(
                        s, EYE_R[i], r, g, b)
                    head_color_edge(
                        s, EYE_L[i], *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                for i in range(0, len(MOUTH)):
                    head_draw_some(2, 0, s, 0, 0, 0)

                    head_color_edge(
                        s, MOUTH[i],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                update_all_argb(s)
            elif songAnimation == SongAnimation.ALL_RANDOM:
                RandomStripes(s)
                update_all_argb(s)
            elif songAnimation == SongAnimation.DRAW_EYES:
                for i in range(0, len(EYE_R)):
                    head_color_edge(
                        s, EYE_R[i],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                    head_color_edge(
                        s, EYE_L[i],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                update_all_argb(s)
            elif songAnimation == SongAnimation.DRAW_MOUTH:
                head_draw_some(2, 0, s, 0, 0, 0)
                for i in range(0, len(MOUTH)):
                    head_color_edge(
                        s, MOUTH[i], *hsv2rgb(rgb2hsv(255, 0, 0)[0], 1, opacity))
            elif songAnimation == SongAnimation.ROLL_ALL:
                head_draw_some(2, 0, s, 0, 0, 0)
                if (lightIndex1 == len(MOUTH)):
                    lightIndex1 = 0
                head_color_edge(
                    s, MOUTH[lightIndex1],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                lightIndex1 += 1
                if (lightIndex2 == len(EYE_R)):
                    lightIndex2 = 0
                head_color_edge(
                    s, EYE_R[lightIndex2],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                head_color_edge(
                    s, EYE_L[lightIndex2],  *hsv2rgb(rgb2hsv(r, g, b)[0], 1, opacity))
                lightIndex2 += 1
            elif songAnimation == SongAnimation.ROLL_EYES:
                if (lightIndex1 == len(EYE_R)):
                    lightIndex1 = 0
                head_color_edge(
                    s, EYE_R[lightIndex1], r, g, b)
                head_color_edge(
                    s, EYE_L[lightIndex1], r, g, b)
                lightIndex1 += 1
                update_all_argb(s)
            elif songAnimation == SongAnimation.ROLL_MOUTH:
                head_draw_some(2, 0, s, 0, 0, 0)
                if (lightIndex1 == len(MOUTH)):
                    lightIndex1 = 0
                oneStep = 1
                for step in range(1, (int)(len(allEdges[MOUTH[lightIndex1]])/oneStep)):
                    head_clear_all(s)
                    # oneStep: int = len(allEdges[MOUTH[lightIndex1]])/5
                    allEdges[MOUTH[lightIndex1]].set_range(
                        s, (int)(oneStep * step), (min)(oneStep * step + 3, len(allEdges[MOUTH[lightIndex1]])-1), *hsv2rgb(rgb2hsv(255, 0, 0)[0], 1, opacity))
                    if (lightIndex1 + 1 >= len(MOUTH)):
                        lightIndex2 = 0
                    else:
                        lightIndex2 = lightIndex1 + 1
                    if (oneStep * step + 3 >= len(allEdges[MOUTH[lightIndex1]])):
                        allEdges[MOUTH[lightIndex2]].set_range(
                            s, 1, (int)(oneStep * step + 3 - len(allEdges[MOUTH[lightIndex1]])+1), *hsv2rgb(rgb2hsv(255, 0, 0)[0], 1, opacity))
                    update_all_argb(s)
                lightIndex1 += 1
            # print('a')
            update_all_argb(s)
            # sleep(0.05)
            t += 0.05
    # finally:
     #   return
        '''

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
    for i in range(0, len(EYE_R)):
        head_color_edge(s, EYE_R[i], hsv2rgb(
            rgb2hsv(255, 0, 0)[0], 1, opacity))
    # cube_draw_all(s, *hsv2rgb(rgb2hsv(255, 0, 0)[0], 1, opacity))
    update_all_argb(s)
    sleep(0.04)
    t += 0.04
    '''


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
