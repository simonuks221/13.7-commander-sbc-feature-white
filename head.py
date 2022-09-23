from api import *
from examples import argb_audio_example
from segment import *
from enum import IntEnum
from color_utils import *
from time import *
from joint import *

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

# Jointai
'''
a = len(BOTTOM_BACK_0)
BOTTOM_BACK_0 = [[0, 3, 4, a, a+1], [5, 6, a, a + 2, a + 3], [6, 7, 13], [4, 5, 7, 8, 11, 12], [8, 9, 2, 3],
                 [9, 10, 22, 23, 25, 26], [10, 11, 14, 15], [15, 16, 21, 22, 27, 28], [
    16, 17, 19, 20], [18, 17, 14, 13, 12],
    [18, 19], [20, 21, 29], [23, 24, 1, 2], [24, 25], [26, 27], [28, 29]]

BOTTOM_FRONT_0 = [[0, 6, 7, a + 2, a + 3], [0, 1, 4, 5, a + 1, a + 2], [2, 3, 4, a + 7, a + 8, 12], [4, 5, 11, 13, 14], [6, 7, 10, 11, 15, 16], [8, 9, 10], [12, 13, 18], [14, 15, 17, 18], [16,
                                                                                                                                                                                             17, 9], [3, 19, 20], [20, 21, 23], [24, 25], [25, 26], [26, 27, 39, 40, 43, 44], [28, 29], [30, 31, 33, 34, 28, 39], [34, 35, 36],  [36, 37], [37, 38, 40, 41], [42, 43, 45, 23, 22]]  # kaire
BOTTOM_FRONT_1 = [[1, 2, 5, 6, 11, 12], [3, 4, 5], [0, 6, 7, 9, 10], [8, 9, 14, 15, 17, 18], [10, 11, 13, 14], [12, 13], [14, 15], [15, 16, 18], [17, 18], [19, 20], [
    20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29, 30], [30, 31], [31, 32, 42, 43, 46, 47], [32, 33], [33, 34, 36, 37, 41, 42], [37, 38, 39], [39, 40], [40, 41, 43, 44], [45, 46, 48, 17, 18]]


TOP0 = [[0, 4, 5, a + 4, a + 5], [0, 2, 3, a + 0, a + 2, a + 3], [1, a + 0, a + 1], [1, 2, 11, 12], [3, 4, 10, 11, 13, 14], [
    5, 6, 7, 9, 10], [7, 8, a+6, a+7], [8, 9, 16], [12, 13, 17], [14, 15, 16, 17], [6, a + 5, a + 6, a + 8, a + 9, a + 14]]
TOP1 = [[1, 2, 10, 11], [3, 4, 9, 10, 12, 13],
        [7, 8, 15], [11, 12, 16], [13, 14, 16, 15]]

FACE0 = [[0, a + 0, a + 17, a + 18], [0, 1, 2, 4, 14], [1, a + 1], [2, 3], [3, 4, 5], [5, 6, 12, 13], [6, 7, 19], [7, 8, 10, 11], [8, 9, 21], [9, 10], [11, 12], [13, 14, 15], [15, 16], [16,
                                                                                                                                                                                          17, a + 18, a + 19], [17, 18], [18, 19, 20], [20, 21, 22], [22, 23, 31, 32, a + 19, a + 20], [23, 24, 26, 27], [25, 26, 28, 29], [27, 28, 30, 31], [32, 30, 29, a + 24, a + 25]]  # i kaire
FACE1 = [[0, 1, 2, 4, 14], [2, 3], [3, 4, 5], [5, 6, 12, 13], [6, 7, 19], [7, 8, 10, 11], [
    8, 9, 24], [9, 10], [11, 12], [13, 14, 15], [15, 16], [16, 17, 20, 21], [21, 22], [22, 23, 24]]

SMALL_SIDE_0 = [[0, a + 0, a + 6, a + 7, a + 10, a + 11],
                [0, 1], [1, 2, 4, 5, a + 11], [2, 3], [3, 4, 9], [5, 6, 8, 9], [6, 7, a + 13, a + 14], [7, 8]]
SMALL_SIDE_1 = [[0, 1], [1, 2, 5, 6], [2, 3], [3, 4, 16, 17],
                [4, 5, 7, 8], [8, 9, 15, 14], [9, 10, 12, 13], [17, 18]]

BIG_SIDE_0 = [[0, a + 0, a + 6, a + 7, a + 10, a + 11],
              [0, 1], [1, 2, 7, 8, a + 11], [2, 3], [3, 4, 6, 7, 12, 13], [4, 5], [5, 6, 17], [8, 9, 11, 12], [9, 10, a + 11], [10, 11, 14, 15], [13, 14, 16, 17]]  # i desiine
BIG_SIDE_1 = [[0, 1], [1, 2, 5, 6], [2, 3], [3, 4, 16, 17],
              [4, 5, 7, 8], [8, 9, 15, 14], [9, 10, 12, 13], [17, 18]]

'''
jointIndexes = []

jointai: SegmentJoint = []

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
        set_argb(s, i, 0, 0, 1299, 0, 0, 0)
        set_argb(s, i, 1, 0, 1299, 0, 0, 0)


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


def head_init(s: Serial, allPixels: int, jointIndexes: int):
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

    '''
    for ii in jointIndexes:
        print(ii)
        segments: LEDSegment = []
        for iii in ii:
            segments.append(allEdges[iii])
        jointai.append(SegmentJoint(segments))
    '''
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
