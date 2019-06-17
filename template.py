from base_layers import Layer, ShapeLayer
from text_layers import PointTextLayer
from attribute import StringAttribute, NumericAttribute

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

# TODO adaptive_sharpen for ImageLayers

class ColorLayer(ShapeLayer):
    """"""
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, **kwargs)

    def render(self, fresh=False):
        if fresh and self.pre_render is not None:
            return self.pre_render
        elif self.content is not None:
            if not isinstance(self.content, Color):
                self.content = Color(self.content)
            img = Image(width=int(self["width"]), height=int(self["height"]), background=self.content)
            return img
        else:
            raise NotReadyToRenderError("Content is needed to render ColorLayer.")

class Template(ShapeLayer):
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        super().__init__(name, **kwargs)
        self.template = self
        self.parent = self

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers):
        for l in layers:
            l.parent = self
            l.template = self
        self._layers = layers

    def update_bounds(self):
        tries = 0
        while tries < 3:
            tries += 1
            snbx, snby = not self.is_x_bounded, not self.is_y_bounded
            super().update_bounds()
            if snbx and self.is_x_bounded or snby and self.is_y_bounded:
                tries = 0 # started not bounded, but now x/y bounded
            for l in self.layers:
                nbx, nby = not l.is_x_bounded, not l.is_y_bounded
                l.update_bounds()
                if nbx and l.is_x_bounded or nby and l.is_y_bounded:
                    tries = 0

    def render(self, fresh=False):
        image = Image(width=int(self["width"]), height=int(self["height"]))
        for layer in self.layers:
            img = layer.render()
            if img is not None:
                image.composite(img, left=int(layer["left"]), top=int(layer["top"]))
        return image

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"Template({self.name}, {attributes})"

    def get_layer(self, key):
        if isinstance(key, Layer):
            key = key.name
        if isinstance(key, str):
            for layer in self.layers:
                if layer.name == key:
                    return layer
                elif isinstance(layer, Template):
                    l = layer.get_layer(key)
                    if l is not None:
                        return l
        else:
            raise ValueError("You can only pass in layer names or layers.")

if __name__ == "__main__":
    # at = AreaTextLayer("area_text_layer", content="Area Text Layer", font="Arial", size=35, color="Black",
            # left=NumericAttribute(0), width=NumericAttribute(40), top=NumericAttribute(0), height=NumericAttribute(50))
    pt = PointTextLayer("point_text_layer", content="Point Text Layer", font="Arial", size=35, color="Black",
            left=NumericAttribute(0), top=NumericAttribute(0))
    bg = ColorLayer("bg", content="Red", left=NumericAttribute(0),
            width=StringAttribute("parent.width"), height=StringAttribute("parent.height"), top=NumericAttribute(0))
    temp = Template("temp", bg, pt, left=NumericAttribute(0), right=StringAttribute("point_text_layer.right"),
            top=NumericAttribute(0), height=NumericAttribute(100))
    temp2 = Template("temp", temp, left=NumericAttribute(0), right=StringAttribute("point_text_layer.right"),
            top=NumericAttribute(0), height=NumericAttribute(500))

    # print(temp.template)
    temp2.update_bounds()
    # print("x", temp.x_bounds)
    # print("y", temp.y_bounds)
    # print("x", pt.x_bounds)
    # print("y", pt.y_bounds)
    image = temp2.render()
    with Image(width=image.width, height=image.height, background=Color("White")) as temp_image:
        temp_image.composite(image)
        temp_image.save(filename="test_images/testing_3.png")

