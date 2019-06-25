from wand.image import Image
from wand.color import Color

img = Image(width=100, height=100, filename="resources/svg/BR.svg",
    background=Color("Transparent"))
# export = img.export_pixels(x=0, width=1, y=0, height=1)
# print(export)

print(img.size)
img.trim()
img.save(filename="test_images/svg_test.png")
