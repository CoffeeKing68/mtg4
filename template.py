from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
from bounds import Bounds

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
# import re

class Layer(ABC):
    x_coords = ["left", "xcenter", "right"]
    y_coords = ["top", "ycenter", "bottom"]

    x_width = ["width"]
    y_height = ["height"]

    xpct = "XP"
    ypct = "YP"

    def __init__(self, *args, **kwargs):
        self.pre_render = None
        self.parent = None
        self.template = None
        self._x_bounds = None
        self._y_bounds = None
        if "content" in kwargs:
            self.content = kwargs["content"]

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        self._template = template

    @property
    def pre_render(self):
        return self._pre_render

    @pre_render.setter
    def pre_render(self, pre_render):
        self._pre_render = pre_render

    def content_getter(self):
        return self._content

    def content_setter(self, content):
        self._content = content

    content = property(content_getter, content_setter)

    @staticmethod
    def map_y_bound(bd):
        mapping = {
            "top": "P0",
            "ycenter": "P50",
            "bottom": "P100",
            "height": "full",
        }
        pct = "YP"
        return Layer.map_bound(bd, mapping, pct)

    @staticmethod
    def map_x_bound(bd):
        mapping = {
            "left": "P0",
            "xcenter": "P50",
            "right": "P100",
            "width": "full",
        }
        pct = "XP"
        return Layer.map_bound(bd, mapping, pct)

    @staticmethod
    def map_bound(bd, mapping, pct):
        if bd in mapping: # is sugar
            return mapping[bd]
        elif bd[:2].upper() == pct.upper(): # is pct
            parsed_pct = str(Bounds.parse_pct(bd[1:])).replace(".", "_") # change . to _ for bounds method
            return f"P{parsed_pct}"

    @staticmethod
    def validate_x_attributes(kwargs, amount):
        return Layer.validate_attributes(kwargs, Layer.map_x_bound, amount)

    @staticmethod
    def validate_y_attributes(kwargs, amount):
        return Layer.validate_attributes(kwargs, Layer.map_y_bound, amount)

    @staticmethod
    def validate_attributes(kwargs, mapper, amount):
        """
        :param kwargs: The kwargs passed into the init method for the layer (only the coordinate
        arguments are neccessary).
        :param amount: The amount of bound descriptors to define Layer.
        :returns: dict of standardized bounds
        """
        attributes = {}
        bounds = {}
        for key, argument in kwargs.items():
            mapped_key = mapper(key)
            if mapped_key is not None: # is valid bound descriptor
                bounds[mapped_key] = argument
                attributes[key] = argument

        if len(bounds) > amount:
            raise ValueError("You passed in too many coordinates")
        elif len(bounds) < amount:
            raise ValueError("You passed in too few coordinates")
        else:
            return bounds, attributes

    @abstractmethod
    def attributes_to_bounds(self, x_amount, y_amount):
        x_bounds, _ = self.validate_attributes(self.attributes, layer.map_x_bound, x_amount)
        y_bounds, _ = self.validate_attributes(self.attributes, layer.map_y_bound, y_amount)
        return x_bounds, y_bounds

    def update_bounds(self):
        self._pre_render = self.render(True)
        x_bounds, y_bounds = self.attributes_to_bounds()
        self._x_bounds = Bounds(**x_bounds, full=self.pre_render.width)
        self._y_bounds = Bounds(**y_bounds, full=self.pre_render.height)

    @abstractmethod
    def render():
        pass

    @property
    def x_bounds(self):
        return self._x_bounds

    @x_bounds.setter
    def x_bounds(self, x_bounds):
        self._x_bounds = x_bounds

    @property
    def y_bounds(self):
        return self._y_bounds

    @y_bounds.setter
    def y_bounds(self, y_bounds):
        self._y_bounds = y_bounds

    @property
    def left(self):
        return self.x_bounds.start

    @property
    def xcenter(self):
        return self.x_bounds.center

    @property
    def right(self):
        return self.x_bounds.end

    @property
    def width(self):
        return self.x_bounds.full

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, {attributes})"

class PointLayer(Layer):
    """
    A PointLayer's bounds are determined by it's content width and height and
    therefore only require 1 x and y bounding descriptor.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        _, x_attr = self.validate_attributes(kwargs, self.map_x_bound, 1)
        _, y_attr = self.validate_attributes(kwargs, self.map_y_bound, 1)
        self.attributes = {**x_attr, **y_attr}
        super().__init__(*args, **kwargs)

    def attributes_to_bounds(self):
        return super().attributes_to_bounds(1, 1)

class ShapeLayer(Layer):
    """
    A ShapeLayer's bounds are determined by the width and height set at initialization
    and therefore requires 2 x and y bounding descriptors.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        _, x_attr = self.validate_attributes(kwargs, self.map_x_bound, 2)
        _, y_attr = self.validate_attributes(kwargs, self.map_y_bound, 2)
        self.attributes = {**x_attr, **y_attr}
        # self.x_bounds = Bounds(**x_bounds)
        # self.y_bounds = Bounds(**y_bounds)
        super().__init__(*args, **kwargs)

    def attributes_to_bounds(self):
        return super().attributes_to_bounds(2, 2)

class PointTextLayer(PointLayer):
    """
    A PointTextLayer is only defined by an xy coord.
    The text width is limited only by it's parent's width
    """
    def __init__(self, name, font, size, color, *args, **kwargs):
        self.font = font
        self.size = size
        self.color = color
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        # chech if content is set
        # won't check content, because wand will draw a small pixel if content is None
        # TODO adaptive_sharpen
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        else:
            img = Image()
            with Drawing() as draw:
                draw.font = self.font
                draw.font_size = self.size
                if not isinstance(self.color, Color):
                    self.color = Color(self.color)
                draw.color = self.color
                draw.text_antialias = True
                draw.text(self.parent.width, self.parent.height, self.content)
                draw(img)
            img.trim()
            self.pre_render = img
            return img

    def content_setter(self, content):
        self._content = content
        if self.parent is not None:
            self.update_bounds()

    content = property(Layer.content_getter, content_setter)

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, \"{self.content}\", {attributes})"

class AreaTextLayer(ShapeLayer):
    """
    An AreaTextLayer is defined by it's area.
    """
    def __init__(self, name, content, *args, **kwargs):
        self.content = content
        super().__init__(name, *args, **kwargs)

class Template(ShapeLayer):
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        for l in self.layers:
            l.parent = self
            l.template = self
            print(l)
        super().__init__(name, **kwargs)

    @property
    def layers(self):
        return self.__layers

    @layers.setter
    def layers(self, layers):
        self.__layers = layers

    def render():
        pass

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"Template({self.name}, {attributes})"

if __name__ == "__main__":
    layer = PointTextLayer("title", "Arial", 13, "Black", content="Doom Whisperer", XP40=NumericAttribute(40), top=NumericAttribute(40))
    # print(layer)
#     layers = [layer]
    temp = Template("test", layer, left=NumericAttribute(0), width=NumericAttribute(750), top=NumericAttribute(0),
            height=NumericAttribute(1050))
    # temp.eval_attributes()
    image = layer.render()
    # image.save(filename="testing.png")
#     print(layer)
#     print(temp)
#     temp.setBounds()
