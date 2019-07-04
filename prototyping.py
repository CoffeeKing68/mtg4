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
from attributes import StringAttribute as SA
from attributes import NumericAttribute as NA
from attributes import AddAttribute as AA

if __name__ == "__main__":
    # w = 100
    # h = 100

    # image = Image(width=w, height=h, background=Color("Transparent"))

    # with Drawing() as draw:
    #     draw.rectangle(left=0, width=w, top=0, height=h)
    #     draw(image)



