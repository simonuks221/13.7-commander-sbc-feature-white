from time import time
from serial import Serial
from segment import *

class snake:
    pos: int
    speed: int
    count: int
    segment: LEDSegment
    fade_amount: int
    s: Serial


    def __init__(self, s: Serial, fade_amount: int, segment: LEDSegment) -> None:
        self.segment = segment
        self.fade_amount = fade_amount
        self.s = s

    def run_snakes(self, r: int, g: int, b: int):
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
