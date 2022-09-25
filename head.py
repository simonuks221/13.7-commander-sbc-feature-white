from api import *
#from examples import argb_audio_example
from segment import *
from enum import IntEnum
from color_utils import *
from time import *
from joint import *
import random

allEdges = {}

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

#jointai: SegmentJoint = []

tmp = len(BOTTOM_BACK_0) + len(BOTTOM_FRONT_0) + len(SMALL_SIDE_1) + \
    len(BOTTOM_BACK_1) + len(BOTTOM_FRONT_1) + len(SMALL_SIDE_0) - 1
EYE_R = [7 + tmp, 14 + tmp, 16 + tmp, 17 + tmp, 18 + tmp, 19 + tmp, 20 + tmp]
tmp1 = tmp + len(FACE_0)
EYE_L = [7 + tmp1, 14 + tmp1, 16 + tmp1, 17 +
         tmp1, 22 + tmp1, 23 + tmp1, 24 + tmp1]
tmp2 = len(BOTTOM_BACK_0) + len(BOTTOM_BACK_1) + len(BOTTOM_FRONT_0)
MOUTH = [18 + tmp2, 19 + tmp2, 20 + tmp2, 21 + tmp2, 22 + tmp2,
         23 + tmp2, 24 + tmp2, 25 + tmp2, 26 + tmp2]


class E(IntEnum):
    BOTTOM_BACK = 1
    BOTTOM_FRONT = 2
    SMALL_SIDE = 3
    FACE = 4
    TOP = 5
    BIG_SIDE = 6


def head_color_edge(s: Serial, F: int, r: int, g: int, b: int):
    segment: LEDSegment = allEdges[F]
    start_index = 0
    end_index = segment.size() - 1
    segment.set_range(s, start_index, end_index, r, g, b)


def head_color_edge_joint(s: Serial, segment: LEDSegment, r: int, g: int, b: int):
    start_index = 0
    end_index = segment.size() - 1
    segment.set_range(s, start_index, end_index, r, g, b)


def head_draw_some(kanalas: int, portas: int, s: Serial, r: int, g: int, b: int):
    set_argb(s, kanalas, portas, 0, 1299, r, g, b)


def head_clear_all(s: Serial):
    for i in range(0, 7):
        response = set_argb(s, i, 0, 0, 1299, 0, 0, 0)
        set_argb(s, i, 1, 0, 1299, 0, 0, 0)
        if (response == response.TIMEOUT):
            return ResponseStatus.TIMEOUT
    return ResponseStatus.OK


def head_draw_all(s: Serial, r: int, g: int, b: int):
    set_argb(s, 1, 0, 0, 1299, r, g, b)
    set_argb(s, 1, 1, 0, 1299, r, g, b)
    set_argb(s, 2, 0, 0, 1299, r, g, b)
    set_argb(s, 2, 1, 0, 1299, r, g, b)
    set_argb(s, 3, 0, 0, 1299, r, g, b)
    set_argb(s, 3, 1, 0, 1299, r, g, b)
    set_argb(s, 4, 0, 0, 1299, r, g, b)
    set_argb(s, 4, 1, 0, 1299, r, g, b)
    set_argb(s, 5, 0, 0, 1299, r, g, b)
    set_argb(s, 5, 1, 0, 1299, r, g, b)
    set_argb(s, 6, 0, 0, 1299, r, g, b)
    set_argb(s, 6, 1, 0, 1299, r, g, b)


def edges_init(allPixels: int):
    curr: int = 0
    i: int = 0

    for adress in range(0, 6):
        # Loop per visas dalis
        for port in range(0, 2):  # loop per 2 portus
            for e in allPixels[adress*2 + port]:
                newSegment = LEDSegment([(adress + 1, port, curr, curr + e), ])
                allEdges[i] = newSegment
                curr += e
                i += 1
            curr = 0


def head_init(s: Serial):
    '''
    for e in allPixels:
        newSegment = LEDSegment([(FBadress, FBLport, curr, curr + e), ])
        FFRedges[i] = newSegment    
        curr += e
        i += 1
    '''
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


def draw_all_exc_EyeMou(s: Serial, duration: float, r: int, g: int, b: int):
    head_draw_all(s, r, g, b)
    for i in range(0, len(MOUTH)):
        head_draw_some(2, 0, s, r, g, b)
        head_color_edge(s, MOUTH[i], 0, 0, 0)
    update_all_argb(s)
    for i in range(0, len(EYE_R)):
        head_color_edge(s, EYE_R[i], 0, 0, 0)
        head_color_edge(s, EYE_L[i], 0, 0, 0)
    update_all_argb(s)
    sleep(duration)


def blink_EYEMou(s: Serial, blinks: int, r: int, g: int, b: int):
    for i in range(0, blinks):
        for i in range(0, len(EYE_R)):
            head_color_edge(s, EYE_R[i], r, g, b)
            head_color_edge(s, EYE_L[i], r, g, b)
        for i in range(0, len(MOUTH)):
            head_draw_some(2, 0, s, 0, 0, 0)
            head_color_edge(s, MOUTH[i], r, g, b)
        update_all_argb(s)
        head_clear_all(s)
        update_all_argb(s)


def gen_rand_stripes(s: Serial, probabaility: int, r: int,  g: int, b: int):
    works = 0
    while works != 1:  # Random red stripes
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        works = random.randint(0, probabaility)
        head_clear_all(s)
        for r in range(0, 10):
            stripIndexx = random.randint(0, len(allEdges) - 6)
            head_color_edge(s, stripIndexx, r, g, b)
            head_color_edge(s, stripIndexx + 5, r, g, b)
        update_all_argb(s)


def FlagsLTU(s: Serial):
    head_draw_some(1, 0, s, 255, 0, 0)
    head_draw_some(1, 1, s, 255, 0, 0)
    head_draw_some(2, 0, s, 255, 0, 0)
    head_draw_some(2, 1, s, 255, 0, 0)
    # kairys uzausis. Be jo neveikia sekantis
    head_draw_some(3, 0, s, 0, 255, 0)
    # Virsus didesne dalis desineje skalpo
    head_draw_some(3, 1, s, 255, 255, 0)  # virsus kaire

   # 3 yra supainiuotasn su 5
    head_draw_some(4, 0, s, 0, 255, 0)
    head_draw_some(4, 1, s, 0, 255, 0)
    head_draw_some(5, 0, s, 255, 255, 0)
    head_draw_some(5, 1, s, 0, 255, 0)
    head_draw_some(6, 0, s, 0, 255, 0)
    head_draw_some(6, 1, s, 0, 255, 0)
    update_all_argb(s)


def FlagsUkraine(s: Serial):

    head_draw_some(1, 0, s, 255, 255, 0)
    head_draw_some(1, 1, s, 255, 255, 0)
    head_draw_some(2, 0, s, 255, 255, 0)
    head_draw_some(2, 1, s, 255, 255, 0)
    # kairys uzausis. Be jo neveikia sekantis
    head_draw_some(3, 0, s, 0, 0, 255)
    head_draw_some(3, 1, s, 0, 0, 225)  # Virsus didesne dalis desineje skalpo

   # 3 yra supainiuotasn su 5
    head_draw_some(4, 0, s, 0, 0, 255)
    head_draw_some(4, 1, s, 0, 0, 255)
    head_draw_some(5, 0, s, 0, 0, 255)
    head_draw_some(5, 1, s, 0, 0, 255)
    head_draw_some(6, 0, s, 0, 0, 255)
    head_draw_some(6, 1, s, 0, 0, 255)
    update_all_argb(s)
