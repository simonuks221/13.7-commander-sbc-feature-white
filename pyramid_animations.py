from pyramid_api import *
from random import choice, randrange
from color_utils import *
from api import *

def random_implosion(s: Serial, duration: float):
    rgb_color = randomRgb()
    implosion(s, duration, *rgb_color)

def random_explosion(s: Serial, duration: float):
    rgb_color = randomRgb()
    explosion(s, duration, *rgb_color)

def implosion(s: Serial, duration: float, r: int, g: int, b: int):
    plosion(s, False, duration, r, g, b)

def explosion(s: Serial, duration: float, r: int, g: int, b: int):
    plosion(s, True, duration, r, g, b)

def plosion(s: Serial, direction: bool, duration: float, r: int, g: int, b: int):
    steps = None
    if direction:
        steps = range(3)
    else:
        steps = range(3, 0, -1)
    for step in steps:
        clear_all_rgbw()
        sphere(s, step, r, g, b)
        update_all_rgbw(s)
        sleep(duration / 2)

def vu_pulse(s: Serial, metric: float):
    hue = 120 - int(metric * 120)
    pulse(s, metric, hue)

def pulse(s: Serial, metric: float, hue: int):
    size = int(metric * 510)
    rgb_color = hsv2rgb(hue, 1, metric)
    clear_all_rgbw()
    sphere(s, 0, *rgb_color)
    if size > 255:
        sphere(s, 1, *rgb_color)
    update_all_rgbw(s)

def random_plane_sweep(s: Serial, duration: float):
    rgb_color = randomRgb()
    side = choice([Side.LEFT, Side.RIGHT, Side.BOTTOM, Side.FRONT])
    direction = choice([True, False])
    plane_sweep(s, side, direction, duration, *rgb_color)

def random_plane(s: Serial, r: int, g: int, b: int):
    side = choice([Side.LEFT, Side.RIGHT, Side.BOTTOM, Side.FRONT])
    step = uniform(0, 4)
    plane(s, side, step, r, g, b)
    update_all_rgbw(s)

def random_plane_and_color(s: Serial):
    rgb_color = randomRgb()
    side = choice([Side.LEFT, Side.RIGHT, Side.BOTTOM, Side.FRONT])
    step = uniform(0, 4)
    plane(s, side, step, *rgb_color)
    update_all_rgbw(s)
    
def plane_sweep(s: Serial, side: Side, direction: bool, duration: float, r: int, g: int, b: int):
    steps = None
    if direction:
        steps = range(3)
    else:
        steps = range(3, 0, -1)
    for step in steps:
        clear_all_rgbw()
        plane(s, side, step, r, g, b)
        update_all_rgbw(s)
        sleep(duration / 4)

def vu_meter(s: Serial, metric: float):
    clear_all_rgbw()
    volume = int(metric * 4)
    if volume >= 1:
        plane(s, Side.BOTTOM, 0, 0, 255, 0)
    if volume >= 2:
        plane(s, Side.BOTTOM, 1, 0, 255, 0)
    if volume >= 3:
        plane(s, Side.BOTTOM, 2, 255, 255, 0)
    if volume >= 4:
        plane(s, Side.BOTTOM, 3, 255, 0, 0)
    update_all_rgbw(s)

def random_color(s: Serial, metric: float):
    rgb_color = randomRgb()
    color_all(s, *rgb_color)
    update_all_rgbw(s)

def random_color_with_random_plane_sweep(s: Serial, duration: float):
    rgb_color = randomRgb()
    side = choice([Side.LEFT, Side.RIGHT, Side.BOTTOM, Side.FRONT])
    direction = choice([True, False])
    color_with_plane_sweep(s, side, direction, duration, *rgb_color)

def color_with_plane_sweep(s: Serial, side: Side, direction: bool, duration: float, r: int, g: int, b: int):
    if direction:
        steps = range(3)
    else:
        steps = range(3, 0, -1)
    for step in steps:
        plane(s, side, step, r, g, b)
        update_all_rgbw(s)
        sleep(duration / 4)
