from typing import Optional
from serial import Serial

from api import dim_argb, set_argb, set_gradient_argb, update_argb

Color = tuple[int, int, int]

#                addr  port start end
LEDStrip = tuple[int, int, int, int]
LEDStrips = list[LEDStrip]

#                 addr  port pixel
LEDPixel = tuple[int, int, int]


def merge_colors(color1: Color, color2: Color, ratio: float):
    return (
        int(color1[0] * (1-ratio) + color2[0] * ratio),
        int(color1[1] * (1-ratio) + color2[1] * ratio),
        int(color1[2] * (1-ratio) + color2[2] * ratio),
    )


class LEDSegment:
    strips: LEDStrips

    def __init__(self, strips: LEDStrips) -> None:
        self.strips = strips

    def _lookup_strip_by_pixel(self, pix: int):
        offset = 0
        for i in range(len(self.strips)):
            _, _, start, end = self.strips[i]
            if start < end:
                index = start + (pix - offset)
                if index <= end:
                    return i, index
            else:
                index = start - (pix - offset)
                if index >= end:
                    return i, index

            # offset += size
            offset += abs(start - end) + 1

    def get_range(self, start_pix: int, end_pix) -> LEDStrips:
        start_pixel_location = self._lookup_strip_by_pixel(start_pix)
        if start_pixel_location == None:
            raise Exception(f"Pixel '{start_pix}' out of range")

        end_pixel_location = self._lookup_strip_by_pixel(end_pix)
        if end_pixel_location == None:
            raise Exception(f"Pixel '{end_pix}' out of range")

        start_strip_idx, start_idx = start_pixel_location
        end_strip_idx, end_idx = end_pixel_location

        strips = []
        if start_strip_idx != end_strip_idx:
            start_strip = self.strips[start_strip_idx]
            strips.append((
                start_strip[0],
                start_strip[1],
                start_idx,
                start_strip[3]
            ))

            for i in range(start_strip_idx+1, end_strip_idx):
                strips.append(self.strips[i])

            end_strip = self.strips[end_strip_idx]
            strips.append((
                end_strip[0],
                end_strip[1],
                end_strip[2],
                end_idx
            ))
        else:
            strip = self.strips[start_strip_idx]
            strips.append((
                strip[0],
                strip[1],
                start_idx,
                end_idx
            ))

        return strips

    def get_pixel(self, pixel: int) -> LEDPixel:
        pixel_location = self._lookup_strip_by_pixel(pixel)
        if pixel_location == None:
            raise Exception(f"Pixel '{pixel}' out of range")
        strip_idx, idx = pixel_location
        strip = self.strips[strip_idx]
        return (strip[0], strip[1], idx)

    def set_pixel(self, s: Serial, pixel: int, r: int, g: int, b: int):
        addr, port, index = self.get_pixel(pixel)
        set_argb(s, addr, port, index, index, r, g, b)

    def set_range(self, s: Serial, from_pixel: int, to_pixel: int, r: int, g: int, b: int):
        strips = self.get_range(from_pixel, to_pixel)
        for strip in strips:
            set_argb(s, strip[0], strip[1], strip[2], strip[3], r, g, b)

    def set_gradient(self, s: Serial, from_pixel: int, to_pixel: int, from_color: Color, to_color: Color, correction_index: int = 0):
        strips = self.get_range(from_pixel, to_pixel)
        gradient_size = abs(to_pixel - from_pixel) + 1
        offset = 0
        for strip in strips:
            strip_size = abs(strip[2] - strip[3]) + 1
            start_ratio = offset / gradient_size
            end_ratio = (offset + strip_size - 1) / gradient_size

            start_color = merge_colors(from_color, to_color, start_ratio)
            end_color = merge_colors(from_color, to_color, end_ratio)
            set_gradient_argb(s, *strip, *start_color, *
                              end_color, correction_index)
            offset += strip_size

    def dim_range(self, s: Serial, from_pixel: int, to_pixel: int, amount: int):
        strips = self.get_range(from_pixel, to_pixel)
        for strip in strips:
            dim_argb(s, *strip, amount)

    def size(self):
        size = 0
        for _, _, start, end in self.strips:
            size += abs(start - end) + 1
        return size

    def clear(self, s: Serial, from_pixel: Optional[int] = None, to_pixel: Optional[int] = None):
        strips = []
        if from_pixel != None and to_pixel != None:
            strips = self.get_range(from_pixel, to_pixel)
        else:
            strips = self.strips

        for strip in strips:
            set_argb(s, *strip, 0, 0, 0)

    def __len__(self):
        return self.size()
