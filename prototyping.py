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

if __name__ == "__main__":
    # c = Color("RGBA(30, 160, 73, 0.5)")
    c = Color("#00000000")
    print(c.normalized_string)
    print(c.string)
    # w = 100
    # h = 100

    # image = Image(width=w, height=h, background=Color("Transparent"))

    # with Drawing() as draw:
    #     draw.rectangle(left=0, width=w, top=0, height=h)
    #     draw(image)



