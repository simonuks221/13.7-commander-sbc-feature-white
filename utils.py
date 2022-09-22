from serial import Serial
from math import ceil
from colorsys import *
from random import uniform
from segment import LEDSegment

def sloped_segment(
        s: Serial, segment: LEDSegment,
        start_pix: int, end_pix: int,
        start_color: tuple[int, int, int],
        end_color: tuple[int, int, int],
        slope: int,
        correction_index: int = 0
    ):
    segment_size = abs(start_pix - end_pix) + 1
    if segment_size < 2*slope:
        slope = ceil(segment_size/2)

    segment.set_range(s, start_pix, end_pix, *end_color)

    segment.set_gradient(s, start_pix, start_pix+slope, end_color, start_color, correction_index)
    segment.set_gradient(s, end_pix-slope, end_pix, start_color, end_color, correction_index)

    if segment_size > 2*slope:
        segment.set_range(s, start_pix+slope+1, end_pix-slope-1, *start_color)


def rgb2hsv(r: int, g: int, b: int):
    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
    return h*360, s, v

def hsv2rgb(h: float, s: float, v: float):
    r, g, b = hsv_to_rgb(h / 360, s, v)
    return round(r * 255), round(g * 255), round(b * 255)

def random_rgb():
    hue = uniform(0, 360)
    return hsv2rgb(hue, 1, 1)

def random_hsv():
    hue = uniform(0, 360)
    sat = uniform(0, 1)
    val = uniform(0, 1)
    return hue, sat, val
