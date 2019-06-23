from base_layers import Layer, ShapeLayer
from text_layers import PointTextLayer
from attribute import StringAttribute, NumericAttribute

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

from pprint import pprint

# TODO adaptive_sharpen for ImageLayers

class ColorLayer(ShapeLayer):
    """A ShapeLayer that has 1 solid color."""
    # def __init__(self, name, *args, **kwargs):
    #     super().__init__(name, **kwargs)

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

class ColorBackgroundLayer(ShapeLayer):
    def __init__(self, name, *args, **kwargs):
        kwargs["left"] = StringAttribute("parent.left")
        kwargs["right"] = StringAttribute("parent.right")
        kwargs["top"] = StringAttribute("parent.top")
        kwargs["bottom"] = StringAttribute("parent.bottom")
        if "order" not in kwargs:
            kwargs["order"] = -99
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
            raise NotReadyToRenderError("Content is needed to render ColorBackgroundLayer.")

class Template(ShapeLayer):
    """Layers that appear first in *layers arg are rendered first if order is
    not specified (order = 0 by default)."""
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        super().__init__(name, **kwargs)
        # self.template = self
        # self.parent = self

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
            snbx, snby = not self.x.is_bounded, not self.y.is_bounded
            super().update_bounds()
            if snbx and self.x.is_bounded or snby and self.x.is_bounded:
                tries = 0 # started not bounded, but now x/y bounded
            for l in self.layers:
                nbx, nby = not l.x.is_bounded, not l.y.is_bounded
                l.update_bounds()
                if nbx and l.x.is_bounded or nby and l.x.is_bounded:
                    tries = 0

    def render(self, fresh=False):
        image = Image(width=int(self["width"]), height=int(self["height"]))
        for layer in sorted(self.layers, key=lambda l: l.order):
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
    pass

