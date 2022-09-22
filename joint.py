from segment import *
from head import *


class SegmentJoint:
    strips: LEDStrips

    def __init__(self, strips: LEDStrips) -> None:
        self.strips = strips


def LightUpAllJoint(s: Serial, joint: SegmentJoint, r: int, g: int, b: int):
    for strip in joint.strips:
        head_color_edge_joint(s, strip, r, g, b)
