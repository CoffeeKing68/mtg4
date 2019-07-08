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

from os.path import join
import os
import json
from shutil import copy2

# def apply_mask(image, mask, invert=False):
#     image.alpha_channel = True
#     mask.alpha_channel = True
#     if invert:
#         mask.negate()
#     with Image(width=image.width, height=image.height, background=Color("transparent")) as alpha_image:
#         alpha_image.composite_channel("opacity", mask, "copy_alpha")
#         image.composite_channel("alpha", alpha_image, "screen", 0, 0)

if __name__ == "__main__":
    with Image(filename='rose:') as img:
        img.resize(240, 160)
        with Image(width=img.width,
                   height=img.height,
                   background=Color("white")) as mask:

            with Drawing() as ctx:
                ctx.fill_color = Color("black")
                ctx.rectangle(left=0,
                              top=0,
                              width=mask.width,
                              height=mask.height,
                              radius=mask.width*0.1)  # 10% rounding?
                ctx(mask)
            mask.save(filename="test_images/mask.png")
            img.composite_channel('all_channels', mask, 'screen')
            img.save(filename='test_images/out.png')

