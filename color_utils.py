from colorsys import *
from random import uniform

def rgb2hsv(r: int, g: int, b: int):
    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
    return h*360, s, v
    
def hsv2rgb(h: int, s: float, v: float):
    r, g, b = hsv_to_rgb(h / 360, s, v)
    return round(r * 255), round(g * 255), round(b * 255)

def randomRgb():
    hue = uniform(0, 360)
    return hsv2rgb(hue, 1, 1)

def randomHsv():
    hue = uniform(0, 360)
    sat = uniform(0, 1)
    val = uniform(0, 1)
    return hue, sat, val