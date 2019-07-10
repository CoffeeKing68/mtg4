from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

import time
import threading
from terminaltables import AsciiTable
from elapsed_time import ElapsedTimeThread
from template import Template
from template import ColorBackgroundLayer as CBL
from template import ResizeImageLayer as ResizeIL
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA
from bounds import Bounds

from os.path import join
import os
import json
from shutil import copy2
import string
# from string import ascii_lowercase as al
# from string import ascii_uppercase as au
from math import ceil
import numpy as np

# def apply_mask(image, mask, invert=False):
#     image.alpha_channel = True
#     mask.alpha_channel = True
#     if invert:
#         mask.negate()
#     with Image(width=image.width, height=image.height, background=Color("transparent")) as alpha_image:
#         alpha_image.composite_channel("opacity", mask, "copy_alpha")
#         image.composite_channel("alpha", alpha_image, "screen", 0, 0)

def get_indepth_font_metrics(draw, text):
    with Image(width=1, height=1) as temp_image:
        max_descender = 0
        max_ascender = 0
        alpha_metrics = {}
        for l in string.ascii_lowercase + string.ascii_uppercase:
            alpha_metrics[l] = draw.get_font_metrics(temp_image, l, False)
            if alpha_metrics[l].y2 > max_ascender:
                max_ascender = alpha_metrics[l].y2
            if alpha_metrics[l].y1 < max_descender:
                max_descender = alpha_metrics[l].y1

        a_asc = 0
        a_desc = 0
        for l in text:
            if l not in alpha_metrics:
                alpha_metrics[l] = draw.get_font_metrics(temp_image, l, False)
            if alpha_metrics[l].y2 > a_asc:
                a_asc = alpha_metrics[l].y2
            if alpha_metrics[l].y1 < a_desc:
                a_desc = alpha_metrics[l].y1

        ml = draw.get_font_metrics(temp_image, string.ascii_lowercase)
        mu = draw.get_font_metrics(temp_image, string.ascii_uppercase)

        max_ascender = ceil(abs(max_ascender - max(ml.y2, mu.y2)))
        absolute_height = ceil(a_asc) + ceil(- a_desc)

    return {
        "median" : int(ml.y2),
        "descender" : ceil(- max_descender),
        "cap" : int(mu.y2) - int(ml.y2),
        "ascender": int(max_ascender),
        "absolute_height": absolute_height
    }

def main():
    """Find the relationship between baseline and top/bottom"""
    with Drawing() as draw:
        # draw.font_family = 'monospace'
        # draw.font = "resources/fonts/Gotham_medium.ttf" # has + ascender and works
        # draw.font = "resources/fonts/MPlantin.ttf" # adds extra px to bottom
        # draw.font = "resources/fonts/Relay_medium.ttf"
        # draw.font = "resources/fonts/Jace_Beleren_bold.ttf"
        # draw.font = "resources/fonts/Beleren_small_caps.ttf" # not working
        draw.font_size = 25
        num = "".join(str(i) for i in range(10))
        # draw.text_antialias = False

        base = 50
        # text = "k"
        text = string.ascii_lowercase + string.ascii_uppercase
        # img = Image(width=1500, height=100, background=Color("White"))
        # draw.text(10, base, string.ascii_lowercase + string.ascii_uppercase)
        # draw.text(10, base, text)

        median, descender, cap_height, ascender, absolute_height = get_indepth_font_metrics(draw, text).values()
        # if descender > 0:
        #     with Drawing() as d: # Descender
        #         d.fill_color = Color("RGBA(0,255,0,0.4)")
        #         d.rectangle(0, base, width=img.width, height=descender - 1)
        #         d(img)

        # if cap_height > 0:
        #     with Drawing() as d: # Cap height
        #         d.fill_color = Color("RGBA(0,0,255,0.4)")
        #         d.rectangle(0, base - median - cap_height, width=img.width, height=cap_height-1)
        #         d(img)

        # if ascender > 0:
        #     with Drawing() as d: # Ascender
        #         d.fill_color = Color("RGBA(255,165,0,0.4)")
        #         d.rectangle(0, base - median - cap_height - ascender, width=img.width, height=ascender - 1)
        #         d(img)

        # if median > 0:
        #     with Drawing() as d: # Median
        #         d.fill_color = Color("RGBA(255,0,0,0.4)")
        #         d.rectangle(0, base - median, width=img.width, bottom=base-1)
        #         d(img)

        # draw(img)
    print("Ascender", f"{base - median - cap_height - ascender} - {base - median - cap_height} ({ascender})")
    print("Cap height", f"{base - median - cap_height} - {base - median} ({cap_height})")
    print("Median", f"{base - median} - {base} ({median})")
    print("Base", base)
    print("Descender [y1]", f"{base} - {base + descender} ({descender})")
    print("absolute height", absolute_height)
    # img.save(filename="test_images/img.png")
    # img.trim()
    # img.save(filename="test_images/trimmed_img.png")
    # print("actual height", img.height)

