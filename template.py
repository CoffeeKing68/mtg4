from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
from bounds import Bounds, InvalidBoundsError

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
# import re

class Layer(ABC):
    x_coords = ["left", "xcenter", "right", "width"]
    y_coords = ["top", "ycenter", "bottom", "height"]

    # x_width = ["width"]
    # y_height = ["height"]

    # xpct = "XP"
    # ypct = "YP"

    def __init__(self, *args, **kwargs):
        self.pre_render = None
        self.parent = None
        self.template = None
        self.x_bounds = None
        self.y_bounds = None
        self.x_attributes = None
        self.y_attributes = None
        if "content" in kwargs:
            self.content = kwargs["content"]

    @property
    def is_evaluated(self):
        return self.is_x_evaluated and self.is_y_evaluated

    @property
    def is_x_evaluated(self):
        return all(attr.is_evaluated for attr in self.x_attributes.values())

    @property
    def is_y_evaluated(self):
        return all(attr.is_evaluated for attr in self.y_attributes.values())

    def content_getter(self):
        return self._content

    def content_setter(self, content):
        self._content = content

    # have to do it like this for PointTextLayer, who will override setter
    content = property(content_getter, content_setter)

    @staticmethod
    def map_y_bound(bd):
        return Layer.map_bound(bd, {yb:bd for yb, bd in zip(Layer.y_coords, Bounds.standard_bound_names)}, "YP")

    @staticmethod
    def map_x_bound(bd):
        return Layer.map_bound(bd, {xb:bd for xb, bd in zip(Layer.x_coords, Bounds.standard_bound_names)}, "XP")

    @staticmethod
    def map_bound(bd, mapping, pct):
        if bd in mapping: # is sugar
            return mapping[bd]
        elif bd[:2].upper() == pct.upper(): # is pct
            parsed_pct = str(Bounds.parse_pct(bd[1:])).replace(".", "_") # change . to _ for bounds method
            return f"P{parsed_pct}"
        # else:
        #     raise InvalidBoundsError

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
        for descriptor, attribute in x_bounds.items():
            x_bounds[descriptor] = attribute.evaluated_value
        for descriptor, attribute in y_bounds.items():
            y_bounds[descriptor] = attribute.evaluated_value
        return x_bounds, y_bounds

    def update_x_bounds(self):
        self.pre_render = self.render(fresh=False)
        x_bounds, _ = self.attributes_to_bounds()
        self._x_bounds = Bounds(**x_bounds, full=self.pre_render.width)

    def update_y_bounds(self):
        self.pre_render = self.render(fresh=False)
        _, y_bounds = self.attributes_to_bounds()
        self._y_bounds = Bounds(**y_bounds, full=self.pre_render.height)

    @abstractmethod
    def render(self, fresh=True):
        pass

    # @abstractmethod
    # def determine_width_height(self):
    #     pass

    # @property
    # def left(self):
    #     return self.x_bounds.start

    # @property
    # def xcenter(self):
    #     return self.x_bounds.center

    # @property
    # def right(self):
    #     return self.x_bounds.end

    # @property
    # def width(self):
    #     return self.x_bounds.full

    @property
    def attributes(self):
        return {**self.x_attributes, **self.y_attributes}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}"
            for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, {attributes})"

    def __getitem__(self, key):
        # identify x or y
        mapped_x_key = self.map_x_bound(key)
        mapped_y_key = self.map_y_bound(key)
        if map_x_bound is not None:
            return self.x_bounds[map_x_bound]
        elif map_y_bound is not None:
            return self.y_bounds[map_y_bound]
        else:
            raise ValueError("Invalid key")

class PointLayer(Layer):
    """
    A PointLayer's bounds are determined by it's content width and height and
    therefore only require 1 x and y bounding descriptor.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        _, self.x_attributes = self.validate_attributes(kwargs, self.map_x_bound, 1)
        _, self.y_attributes = self.validate_attributes(kwargs, self.map_y_bound, 1)
        super().__init__(*args, **kwargs)

    def attributes_to_bounds(self):
        return super().attributes_to_bounds(1, 1)

    # def determine_width_height(self):
    #     if self.pre_render is None:
    #         self.render
    #     return self.pre_render.width, self.pre_render.height

class ShapeLayer(Layer):
    """
    A ShapeLayer's bounds are determined by the width and height set at initialization
    and therefore requires 2 x and y bounding descriptors.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        _, self.x_attributes = self.validate_attributes(kwargs, self.map_x_bound, 2)
        _, self.y_attributes = self.validate_attributes(kwargs, self.map_y_bound, 2)
        # self.attributes = {**x_attr, **y_attr}
        # self.x_bounds = Bounds(**x_bounds)
        # self.y_bounds = Bounds(**y_bounds)
        super().__init__(*args, **kwargs)

    def attributes_to_bounds(self):
        return super().attributes_to_bounds(2, 2)

    # def determine_width_height(self):
    #     return self.width, self.height # get from bounds

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
        pass
        # chech if content is set
        # won't check content, because wand will draw a small pixel if content is None
        # TODO adaptive_sharpen
        # if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
        #     return self.pre_render
        # else:
        #     img = Image()
        #     with Drawing() as draw:
        #         draw.font = self.font
        #         draw.font_size = self.size
        #         if not isinstance(self.color, Color):
        #             self.color = Color(self.color)
        #         draw.color = self.color
        #         draw.text_antialias = True
        #         draw.text(self.parent.width, self.parent.height, self.content)
        #         draw(img)
        #     img.trim()
        #     self.pre_render = img
        #     return img

    # def content_setter(self, content):
    #     self._content = content
    #     if self.parent is not None:
    #         self.update_bounds()

    # content = property(Layer.content_getter, content_setter)

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for
            key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, \"{self.content}\", {attributes})"

# class AreaTextLayer(ShapeLayer):
#     """
#     An AreaTextLayer is defined by it's area.
#     """
#     def __init__(self, name, content, *args, **kwargs):
#         self.content = content
#         super().__init__(name, *args, **kwargs)

class Template(ShapeLayer):
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        super().__init__(name, **kwargs)

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers):
        for l in layers:
            l.parent = self
            l.template = self
        self._layers = layers

    def render(self, fresh=True):
        pass

    # def evaluate_attributes(self):
    #     self.evaluate_x_attributes()
    #     self.evaluate_y_attributes()

    # def evaluate_x_attributes(self):
    #     evaluation_tries = 0
    #     while evaluation_tries < 10:
    #         for x_attribute in self.x_attributes.values():
    #             if not x_attribute.is_evaluated:
    #                 x_attribute.evaluate(self)
    #                 if x_attribute.is_evaluated:
    #                     evaluation_tries = 0

    #         if self.is_x_evaluated:
    #             self.update_x_bounds()

    #         for layer in self.layers:
    #             for x_attribute in layer.x_attributes.values():
    #                 if not x_attribute.is_evaluated:
    #                     x_attribute.evaluate(layer.template)
    #                     if x_attribute.is_evaluated:
    #                         evaluation_tries = 0
    #             if layer.is_x_evaluted:
    #                 layer.update_x_bounds()
    #             if isinstance(layer, Template):
    #                 layer.evaluate_x_attributes()

    #         evaluation_tries += 1

    # def evaluate_y_attributes(self):
    #     evaluation_tries = 0
    #     while evaluation_tries < 10:
    #         for y_attribute in self.y_attributes.values():
    #             if not y_attribute.is_evaluated:
    #                 y_attribute.evaluate(self)
    #                 if y_attribute.is_evaluated:
    #                     evaluation_tries = 0

    #         for layer in self.layers:
    #             for y_attribute in layer.y_attributes.values():
    #                 if not y_attribute.is_evaluted:
    #                     y_attribute.evaluate(layer.template)
    #                     if y_attribute.is_evaluted:
    #                         evaluation_tries = 0
    #             if isinstance(layer, Template):
    #                 layer.evaluate_y_attributes()

    #         evaluation_tries += 1

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"Template({self.name}, {attributes})"

    def __getitem__(self, key):
        if isinstance(key, Layer):
            key = key.name
        if isinstance(key, str):
            for layer in self.layer:
                if layer.name == key:
                    return layer
                elif isinstance(layer, Template):
                    l = layer.__getitem__(key)
                    if l is not None:
                        return l
        else:
            raise ValueError("You can only pass in layer names or layers.")

if __name__ == "__main__":
    layer = PointTextLayer("title", "Arial", 13, "Black", content="Doom Whisperer", XP40=NumericAttribute(40), top=NumericAttribute(40))
    # print(layer)
#     layers = [layer]
    temp = Template("test", layer, left=NumericAttribute(0), width=NumericAttribute(750), top=NumericAttribute(0),
            height=NumericAttribute(1050))
    image = layer.render()
    # image.save(filename="testing.png")
#     print(layer)
#     print(temp)
#     temp.setBounds()
