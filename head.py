from api import *
from examples import argb_audio_example
from segment import *
from enum import IntEnum
from color_utils import *
from time import *

allEdges = {}


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


def head_init(s: Serial, allPixels: int):
    curr: int = 0
    FBadress = 6
    FBLport = 1
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
