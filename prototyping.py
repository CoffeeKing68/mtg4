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
    # WIDTH = 200
    # HEIGHT = 200
    # artist_brush = ResizeIL("artist_brush", content=join(RESOURCE_DIR, "artist_brush_white.png"),
    #     width=NA(20), left=NA(0), height=SA("set.height"), bottom=SA("parent.bottom"),
    # artist = PTL("artist", BELEREN_SC, INFO_SIZE, FC, left=AA(SA("artist_brush.right"),
    #         NA(3)), bottom=SA("parent.bottom")),
    # bg = CBL("bg", content="Red")
    # artist_temp = Template("artist_temp", artist_brush, artist, xcenter=NA(WIDTH/2)
    #     )
