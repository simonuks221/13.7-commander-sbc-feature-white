from api import *
from examples import argb_audio_example
from segment import *
from enum import IntEnum
from color_utils import *
from time import *
from head import *

'''
class E(IntEnum):
    FRONT_LEFT_FRONT = 0
    FRONT_LEFT_LEFT = 1
    FRONT_LEFT_RIGHT = 2
    FRONT_LEFT_BACK = 3

    FRONT_RIGHT_FRONT = 4
    FRONT_RIGHT_LEFT = 5
    FRONT_RIGHT_RIGHT = 6
    FRONT_RIGHT_BACK = 7

    BACK_LEFT_FRONT = 8
    BACK_LEFT_LEFT = 9
    BACK_LEFT_RIGHT = 10
    BACK_LEFT_BACK = 11
    BACK_RIGHT_FRONT = 12
    BACK_RIGHT_LEFT = 13
    BACK_RIGHT_RIGHT = 14
    BACK_RIGHT_BACK = 15

    BOTTOM_LEFT_LEFT = 16
    BOTTOM_LEFT_RIGHT = 17
    BOTTOM_LEFT_TOP = 18

    BOTTOM_RIGHT_LEFT = 19
    BOTTOM_RIGHT_RIGHT = 20
    BOTTOM_RIGHT_TOP = 21

    BOTTOM_BACK_BACK = 22
    BOTTOM_BACK_FRONT = 23
    BOTTOM_BACK_TOP = 24

    BOTTOM_FRONT_BACK = 25
    BOTTOM_FRONT_FRONT = 26
    BOTTOM_FRONT_TOP = 27

    TOP_LEFT_LEFT = 28
    TOP_LEFT_RIGHT = 29
    TOP_LEFT_TOP = 30
    TOP_LEFT_BOTTOM = 31

    TOP_RIGHT_LEFT = 32
    TOP_RIGHT_RIGHT = 33
    TOP_RIGHT_TOP = 34
    TOP_RIGHT_BOTTOM = 35

    TOP_BACK_BACK = 36
    TOP_BACK_FRONT = 37
    TOP_BACK_TOP = 38
    TOP_BACK_BOTTOM = 39

    TOP_FRONT_BACK = 40
    TOP_FRONT_FRONT = 41
    TOP_FRONT_TOP = 42
    TOP_FRONT_BOTTOM = 43


cube_edges = {}
cube_edges[E.BOTTOM_FRONT_FRONT] = LEDSegment([
    (1, 0, 347, 642),
])
cube_edges[E.BOTTOM_FRONT_TOP] = LEDSegment([
    (1, 0, 25, 317),
])
cube_edges[E.BOTTOM_FRONT_BACK] = LEDSegment([
    (1, 0, 654, 946),
])
cube_edges[E.BOTTOM_RIGHT_RIGHT] = LEDSegment([
    (1, 1, 0, 281),
])
cube_edges[E.BOTTOM_RIGHT_TOP] = LEDSegment([
    (1, 1, 282, 562),
])
cube_edges[E.BOTTOM_RIGHT_LEFT] = LEDSegment([
    (1, 1, 563, 844),
])
cube_edges[E.TOP_FRONT_BOTTOM] = LEDSegment([
    (2, 1, 26, 317),
])
cube_edges[E.TOP_FRONT_FRONT] = LEDSegment([
    (2, 1, 320, 630),
])
'''

FBLpixels = {32, 18, 18, 21, 18, 30}
FBLedges = {}


def cube_init(s: Serial):
    # Setup edges
    curr = 0
    for e in FBLpixels:
        #FBLedges.append(LEDSegment([FBadress, FBLport, curr, curr + e]))
        curr += e

    # Setup argb
    print(enable_argb(s, 1, 0, 1300))
    print(enable_argb(s, 1, 1, 1300))
    print(enable_argb(s, 2, 0, 1300))
    print(enable_argb(s, 2, 1, 1300))
    print(enable_argb(s, 3, 0, 1600))
    print(enable_argb(s, 3, 1, 1600))
    print(enable_argb(s, 4, 0, 1600))
    print(enable_argb(s, 4, 1, 1600))
    print(enable_argb(s, 5, 0, 1600))
    print(enable_argb(s, 5, 1, 1600))
    print(enable_argb(s, 6, 0, 1600))
    print(enable_argb(s, 6, 1, 1600))
    # print(enable_argb(s, 7, 0, 1300))
    # print(enable_argb(s, 7, 1, 1300))
    # print(enable_argb(s, 8, 0, 1300))
    # print(enable_argb(s, 8, 1, 1300))
    # print(enable_argb(s, 9, 0, 1300))
    # print(enable_argb(s, 9, 1, 1300))


def cube_clear_all(s: Serial):
    set_argb(s, 1, 0, 0, 1299, 0, 0, 0)
    set_argb(s, 1, 1, 0, 1299, 0, 0, 0)


def cube_draw_all(s: Serial, r: int, g: int, b: int):
    #set_argb(s, 1, 0, 0, 1299, r, g, b)
    # set_argb(s, 1, 1, 0, 1299, r, g, b)
    set_argb(s, 2, 0, 0, 1299, r, g, b)
    set_argb(s, 2, 1, 0, 1299, r, g, b)
    ##set_argb(s, 3, 0, 0, 1299, r, g, b)
    #set_argb(s, 3, 1, 0, 1299, r, g, b)
    #set_argb(s, 4, 0, 0, 1299, r, g, b)
    #set_argb(s, 4, 1, 0, 1299, r, g, b)
    #set_argb(s, 5, 0, 0, 1299, r, g, b)
    #set_argb(s, 5, 1, 0, 1299, r, g, b)
    #set_argb(s, 6, 0, 0, 1299, r, g, b)
    #set_argb(s, 6, 1, 0, 1299, r, g, b)
    # set_argb(s, 7, 0, 0, 1299, r, g, b)
    # set_argb(s, 7, 1, 0, 1299, r, g, b)
    # set_argb(s, 8, 0, 0, 1299, r, g, b)
    # set_argb(s, 8, 1, 0, 1299, r, g, b)
    # set_argb(s, 9, 0, 0, 1299, r, g, b)
    # set_argb(s, 9, 1, 0, 1299, r, g, b)


def cube_draw_some(kanalas: int, s: Serial, r: int, g: int, b: int):
    set_argb(s, kanalas, 0, 0, 1299, r, g, b)
    set_argb(s, kanalas, 1, 0, 1299, r, g, b)


def cube_color_edge(s: Serial, F: IntEnum, r: int, g: int, b: int):
    segment: LEDSegment = cube_edges[F]
    start_index = 0
    end_index = segment.size() - 1
    segment.set_range(s, start_index, end_index, r, g, b)


def cube_random_all_edges(s: Serial):
    for face in E:
        rgb_color = randomRgb()
        cube_color_edge(s, face, *rgb_color)
    update_all_argb(s)


def cube_snakes(s: Serial, t: int, F: IntEnum, count: int, speed: int, duration: float, fade_amount: int, r: int, g: int, b: int):
    segment: LEDSegment = allEdges[F]
    length = segment.size()
    interval = length / count
    moves = abs(interval / speed)
    time_interval = duration / moves
    pos = 0
    if speed < 0:
        pos = length - 1

    if pos <= interval:
        for i in range(count):
            segment.dim_range(s, 0, length - 1, fade_amount)
            current_pos = pos
            if speed > 0:
                current_pos += (i * interval)
            else:
                current_pos -= (i * interval)
            segment.set_range(s, current_pos, current_pos + speed, r, g, b)
            pos += speed

        sleep(time_interval)

# def cube_color_with_snakes(s: Serial, F: IntEnum, count: int, duration: float, direction: bool, r: int, g: int, b: int):
#     cube_snakes()

# def cube_plane()
