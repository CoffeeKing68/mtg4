from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

img = Image()
with Drawing() as draw:
    # draw.font = "Arial"
    draw.font_size = 15
    draw.text_antialias = True
    content = "Hello World"
    draw.text(1, 1, content)
    draw(img)
img.trim()

img.save(filename="testing.png")

