from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
from bounds import Bounds
# import re

class Layer(ABC):
    x_coords = ["left", "xcenter", "right"]
    y_coords = ["top", "ycenter", "bottom"]

    x_width = ["width"]
    y_height = ["height"]

    xpct = "XP"
    ypct = "YP"

    def __init__(self, *args, **kwargs):
        if "content" in kwargs:
            self.content = kwargs["content"]

    def content_getter(self):
        return self._content

    def content_setter(self, content):
        self._content = content

    content = property(content_getter, content_setter)

    @property
    def acceptable_coords():
        return x_coords + y_coords + x_width + y_height

    @property
    def acceptable_x_coords():
        return x_coords + x_width

    @property
    def acceptable_y_coords():
        return y_coords + y_height

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
    def render():
        pass

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
        self._x_bounds, x_attr = self.validate_attributes(kwargs, self.map_x_bound, 1)
        self._y_bounds, y_attr = self.validate_attributes(kwargs, self.map_y_bound, 1)
        self.attributes = {**x_attr, **y_attr}
        super().__init__(*args, **kwargs)

class ShapeLayer(Layer):
    """
    A ShapeLayer's bounds are determined by the width and height set at initialization
    and therefore requires 2 x and y bounding descriptors.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        x_attributes = Layer.validateAttributes(kwargs, self.x_coords + self.x_width, 2)
        y_attributes = Layer.validateAttributes(kwargs, self.y_coords + self.y_height, 2)
        self.attributes = {**x_attributes, **y_attributes}


    def setBounds():
        Layer.setBounds()

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

    def render(fresh=False):
        # chech if content is set
        pass

    def content_setter(self, content):
        self._content = content
        # self._pre_render = self.render(fresh=True)
        # self._x_bounds = (**self._x_bounds, full=self._pre_render.width)
        # self._y_bounds = (**self._y_bounds, full=self._pre_render.height)
        # gonna do some more stuff here later

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

    def setBounds():
        pass

class Template(ShapeLayer):
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        super().__init__(name, **kwargs)

    @property
    def layers(self):
        return self.__layers

    @layers.setter
    def layers(self, *layers):
        self.__layers = layers

    def setBounds(self):
        for attribute in self.attributes.values():
            if not attributes.is_evaluted: # does this attribute not have an ev?
                attribute.evaluate(self)

        if all(attribute.is_evaluted for attribute in self.attributes.values()):
            # if all attributes are evaluated
            super().setBounds()

    def render():
        pass

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"Template({self.name}, {attributes})"

if __name__ == "__main__":
    layer = PointTextLayer("title", "Arial", 13, content="Doom Whisperer", XP40=NumericAttribute(40), top=NumericAttribute(40))
    print(layer)
#     layers = [layer]
#     temp = Template("test", *layers, left=NumericAttribute(0), width=NumericAttribute(750), top=NumericAttribute(0),
#             height=NumericAttribute(1050))
#     print(layer)
#     print(temp)
#     temp.setBounds()
