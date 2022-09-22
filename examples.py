import random
from typing import Generator
# import pygame
# from pygame import Rect
from serial import Serial
from pydub import AudioSegment
from time import sleep, time
from numpy.fft import rfft
import numpy as np
from math import sqrt

import api
from api import clear_argb, enable_argb, ping, set_argb, set_time, sync_time, disable_argb, update_argb
from audio import AudioFile, AudioMic, smooth_fft_values
from segment import LEDSegment
from utils import sloped_segment

max_brightness = 30
def gen_color():
    return random.randrange(0, max_brightness), \
            random.randrange(0, max_brightness), \
            random.randrange(0, max_brightness)

def test_argb(s: Serial, address: int, port: int, pixel_count: int):
    enable_argb(s, address, port, pixel_count)
    yield
    while True:
        r, g, b = gen_color()
        for i in range(pixel_count):
            set_argb(s, address, port, i, i, r, g, b)
            yield

def get_addreses(led_strips: list[tuple[int, int, int]]) -> set[int]:
    return set(strip[0] for strip in led_strips)

def shrinking_segment_example():
    addr = 0x01
    port = 0x00
    pixel_count = 50
    front_color = (255, 0, 0)
    back_color = (0, 255, 0)

    s = Serial("/dev/ttyUSB0", baud_rates[2])
    s.timeout = 0.1
    enable_argb(s, addr, port, pixel_count)
    segment = LEDSegment([
        (addr, port, 0, pixel_count-1)
    ])

    steps = 60
    for t in range(steps):
        shrink = int((t/steps)*len(segment)/2)
        segment.clear(s)
        segment.set_range(s, 0, len(segment)-1, *back_color)
        sloped_segment(s, segment, shrink, len(segment)-1-shrink, front_color, back_color, 6, 3)
        update_argb(s)
        sleep(1/steps)

def argb_strip_example():
    s = Serial("/dev/ttyUSB0", 115200)
    s.timeout = 0.1
    led_strips = [
    #   Address | port | pixel count
        (0x01,    0x00,    300),
        (0x02,    0x00,    300)
    ]

    for address in get_addreses(led_strips):
        sync_time(s, address)

    coroutines = []
    for strip in led_strips:
        coroutines.append(test_argb(s, strip[0], strip[1], strip[2]))

    try:
        while True:
            for co in coroutines:
                next(co)
    except KeyboardInterrupt:
        for strip in led_strips:
            clear_argb(s, strip[0], strip[1], strip[2])

def test_argb_fft(s: Serial, address: int, port: int, pixel_count: int):
    enable_argb(s, address, port, pixel_count)
    yield
    background = (40, 0, 0)#gen_color()
    foreground = (0, 40, 0)#gen_color()

    prev_pixel_height = 0
    set_argb(s, address, port, 0, pixel_count-1, *background)
    while True:
        fft_values = yield

        value = sum(v for v in fft_values[50:80])
        max_value = sum(v for v in fft_values)

        if max_value > 0:
            percent = value/max_value
            pixel_height = int(percent*pixel_count) - 1
            if pixel_height > prev_pixel_height:
                set_argb(s, address, port, prev_pixel_height, pixel_height, *foreground)
            elif pixel_height < prev_pixel_height:
                set_argb(s, address, port, pixel_height, prev_pixel_height, *background)
            prev_pixel_height = pixel_height

def argb_audio_example():
    addr = 0x01
    port = 0x00
    pixel_count = 50
    front_color = (255, 255, 0)
    back_color = (0, 0, 255)
    use_rms = False

    s = Serial("/dev/ttyUSB0", baud_rates[2])
    s.timeout = 0.1

    enable_argb(s, addr, port, pixel_count)

    segment = LEDSegment([
        (addr, port, 0, pixel_count-1),
    ])

    song = AudioFile('Armors - DOA.wav')

    song.play()

    try:
        max_metric = 0.5
        max_shrink = len(segment) // 3
        fft_values = []
        while True:
            # Get metric
            if use_rms:
                metric = song.get_rms()
            else:
                new_fft_values = song.get_fft()
                smooth_fft_values(fft_values, new_fft_values, 0.9)
                metric = sum(v for v in fft_values[50:80])

            # Normalize metric
            max_metric = max(max_metric, metric)
            metric = metric / max_metric

            # Visualize
            shrink = int(metric * max_shrink)
            segment.clear(s)
            segment.set_range(s, 0, len(segment)-1, *back_color)
            sloped_segment(s, segment, shrink, len(segment)-1-shrink, front_color, back_color, 6, 3)
            update_argb(s)
    finally:
        song.terminate()

def argb_mic_example():
    addr = 0x01
    port = 0x00
    pixel_count = 50
    front_color = (255, 255, 0)
    back_color = (0, 0, 255)
    use_rms = False

    s = Serial("/dev/ttyUSB0", baud_rates[2])
    s.timeout = 0.1

    enable_argb(s, addr, port, pixel_count)

    segment = LEDSegment(s, [
        (addr, port, 0, pixel_count-1),
    ])

    mic = AudioMic()

    try:
        max_metric = 0.5
        max_shrink = len(segment) // 3
        fft_values = []
        while True:
            # Get metric
            if use_rms:
                metric = mic.get_rms()
            else:
                new_fft_values = mic.get_fft()
                smooth_fft_values(fft_values, new_fft_values, 0.9)
                metric = sum(v for v in fft_values[50:80])

            # Normalize metric
            max_metric = max(max_metric, metric)
            metric = metric / max_metric

            # Visualize
            shrink = int(metric * max_shrink)
            segment.clear()
            segment.set_range(0, len(segment)-1, *back_color)
            sloped_segment(segment, shrink, len(segment)-1-shrink, front_color, back_color, 6, 3)
            segment.update()
    finally:
        mic.terminate()
