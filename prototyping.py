from wand.image import Image
from wand.color import Color

WIDTH = 100

image = Image(filename="resources/svg/B.svg", background=Color("Transparent"),
        width=WIDTH, height=WIDTH)
image2 = Image(filename="resources/svg/B.svg", background=Color("Transparent"),
        resolution=300, width=WIDTH, height=WIDTH)
image.antialias = True
image2.antialias = True
print(image.size)
print(image2.size)
image.save(filename="test.png")
image2.save(filename="test_res_300.png")
