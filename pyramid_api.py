from random import random
from api import enable_rgbw, disable_rgbw, set_rgbw, clear_rgbw, update_rgbw
from enum import IntEnum
from serial import Serial
from time import *
from color_utils import *
from random import choice, randrange

class Side(IntEnum):
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    FRONT = 3

class T(IntEnum):
    TOP_TOP = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    TOP_BACK = 3
    LEFT_TOP = 4
    LEFT_LEFT = 5
    LEFT_RIGHT = 6
    LEFT_BACK = 7
    RIGHT_TOP = 8
    RIGHT_LEFT = 9
    RIGHT_RIGHT = 10
    RIGHT_BACK = 11
    BACK_TOP = 12
    BACK_LEFT = 13
    BACK_RIGHT = 14
    BACK_BACK = 15

pyramid = {}
pyramid[T.TOP_TOP] = [0x01, 0]
pyramid[T.TOP_LEFT] = [0x01, 1]
pyramid[T.TOP_RIGHT] = [0x02, 0]
pyramid[T.TOP_BACK] = [0x02, 1]
pyramid[T.LEFT_TOP] = [0x03, 0]
pyramid[T.LEFT_LEFT] = [0x03, 1]
pyramid[T.LEFT_RIGHT] = [0x04, 0]
pyramid[T.LEFT_BACK] = [0x04, 1]
pyramid[T.RIGHT_TOP] = [0x05, 0]
pyramid[T.RIGHT_LEFT] = [0x05, 1]
pyramid[T.RIGHT_RIGHT] = [0x06, 0]
pyramid[T.RIGHT_BACK] = [0x06, 1]
pyramid[T.BACK_TOP] = [0x07, 0]
pyramid[T.BACK_LEFT] = [0x07, 1]
pyramid[T.BACK_RIGHT] = [0x08, 0]
pyramid[T.BACK_BACK] = [0x08, 1]

def init_all(s: Serial):
    for address, port in pyramid.values():
        print(enable_rgbw(s, address, port))

def color_all(s: Serial, r: int, g: int, b: int):
    for address, port in pyramid.values():
        set_rgbw(s, address, port, r, g, b, 0)

def random_color_all(s: Serial):
    rgb_color = randomRgb()
    for address, port in pyramid.values():
        set_rgbw(s, address, port, *rgb_color, 0)

def random_color_all_differently(s: Serial):
    for address, port in pyramid.values():
        rgb_color = randomRgb()
        set_rgbw(s, address, port, *rgb_color, 0)

def random_triangle(s: Serial, r: int, g: int, b: int):
    triangle = choice([T.TOP_TOP, T.TOP_LEFT, T.TOP_RIGHT, T.TOP_BACK, T.LEFT_TOP, T.LEFT_LEFT, T.LEFT_RIGHT, T.LEFT_BACK, 
                       T.RIGHT_TOP, T.RIGHT_LEFT, T.RIGHT_RIGHT, T.RIGHT_BACK, T.BACK_TOP, T.BACK_LEFT, T.BACK_RIGHT, T.BACK_BACK])
    set_rgbw(s, *pyramid[triangle], r, g, b, 0)

def sphere(s: Serial, step: int, r: int, g: int, b: int):
    if step == 0:
        set_rgbw(s, *pyramid[T.BACK_RIGHT], r, g, b, 0)
        set_rgbw(s, *pyramid[T.BACK_TOP], r, g, b, 0)
        set_rgbw(s, *pyramid[T.BACK_LEFT], r, g, b, 0)
        set_rgbw(s, *pyramid[T.TOP_BACK], r, g, b, 0)
        set_rgbw(s, *pyramid[T.TOP_LEFT], r, g, b, 0)
        set_rgbw(s, *pyramid[T.TOP_RIGHT], r, g, b, 0)
        set_rgbw(s, *pyramid[T.LEFT_BACK], r, g, b, 0)
        set_rgbw(s, *pyramid[T.LEFT_TOP], r, g, b, 0)
        set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)

    if step >= 1:
        set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)
        set_rgbw(s, *pyramid[T.BACK_BACK], r, g, b, 0)
        set_rgbw(s, *pyramid[T.TOP_TOP], r, g, b, 0)

def plane(s: Serial, side: Side, step: int, r: int, g: int, b: int):
    if side == side.LEFT:
        if step == 0:
            set_rgbw(s, *pyramid[T.BACK_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)

        if step == 1:
            set_rgbw(s, *pyramid[T.LEFT_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_RIGHT], r, g, b, 0)

        if step == 2:
            set_rgbw(s, *pyramid[T.RIGHT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_BACK], r, g, b, 0)

        if step >= 3:
            set_rgbw(s, *pyramid[T.RIGHT_RIGHT], r, g, b, 0)
        
    if side == side.RIGHT:
        if step == 0:
            set_rgbw(s, *pyramid[T.BACK_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_RIGHT], r, g, b, 0)

        if step == 1:
            set_rgbw(s, *pyramid[T.RIGHT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_LEFT], r, g, b, 0)

        if step == 2:
            set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_BACK], r, g, b, 0)

        if step >= 3:
            set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)

    if side == side.BOTTOM:
        if step == 0:
            set_rgbw(s, *pyramid[T.BACK_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_RIGHT], r, g, b, 0)

        if step == 1:
            set_rgbw(s, *pyramid[T.RIGHT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_TOP], r, g, b, 0)

        if step == 2:
            set_rgbw(s, *pyramid[T.TOP_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_BACK], r, g, b, 0)

        if step >= 3:
            set_rgbw(s, *pyramid[T.TOP_TOP], r, g, b, 0)

    if side == side.FRONT:
        if step == 0:
            set_rgbw(s, *pyramid[T.TOP_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_TOP], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.RIGHT_RIGHT], r, g, b, 0)

        if step == 1:
            set_rgbw(s, *pyramid[T.RIGHT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.LEFT_BACK], r, g, b, 0)
            set_rgbw(s, *pyramid[T.TOP_BACK], r, g, b, 0)

        if step == 2:
            set_rgbw(s, *pyramid[T.BACK_LEFT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_RIGHT], r, g, b, 0)
            set_rgbw(s, *pyramid[T.BACK_TOP], r, g, b, 0)

        if step >= 3:
            set_rgbw(s, *pyramid[T.BACK_BACK], r, g, b, 0)
