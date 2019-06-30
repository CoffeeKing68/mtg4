from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

WIDTH = 100

# image = Image(filename="resources/art/BFZ/Dust Stalker.jpg", background=Color("Transparent"),
#         width=WIDTH, height=WIDTH)
image = Image(width=WIDTH, height=WIDTH, background=Color("Red"))
with Drawing() as draw:
    draw.fill_color = Color("Green")
    draw.rectangle(left=5, right=94, top=5, bottom=94)
    draw(image)
image.save(filename="prototype.png")
