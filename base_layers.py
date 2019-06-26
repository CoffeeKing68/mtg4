from abc import ABC, abstractmethod
from attribute import Attribute
from attribute import NumericAttribute as NA
from attribute import StringAttribute as SA
from bounds import Bounds
from exceptions import InvalidBoundsError, NotEvaluatedError, NotBoundedError
from exceptions import NotReadyToRenderError
from dimensions import XDimension, YDimension
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

class Layer(ABC):
    """Base Layer for all Layers to inherit from. Does most of the heavy
    lifting."""
    def __init__(self, name, x_attrs_req, y_attrs_req, *args, **kwargs):
        self.name = name
        self.x_attributes_required = x_attrs_req
        self.y_attributes_required = y_attrs_req
        self.pre_render = None
        self.order = kwargs.get("order", 0) # default is 0
        self.parent = None
        self.template = None
        self.dimensions = {}
        self.dimensions["x"] = XDimension(self.x_attributes_required, self, **kwargs)
        self.dimensions["y"] = YDimension(self.y_attributes_required, self, **kwargs)
        self.content = kwargs.get("content") # default is None

    @property
    def x(self):
        return self.dimensions["x"]

    @x.setter
    def x(self, value):
        self.dimensions["x"] = value

    @property
    def y(self):
        return self.dimensions["y"]

    @y.setter
    def y(self, value):
        self.dimensions["y"] = value

    @property
    def is_evaluated(self):
        return all(dim.is_evaluated for dim in self.dimensions.values())

    @property
    def is_bounded(self):
        print(dim.is_bounded for dim in self.dimensions.values())
        return all(dim.is_bounded for dim in self.dimensions.values())

    def update_bounds(self):
        return [dim.update_bounds() for dim in self.dimensions.values()]

    @abstractmethod
    def render(self, fresh=False):
        pass

    def render_boundary(self):
        """Draws a rectangle around bounds."""
        img = Image(width=int(self.parent["width"]), background=Color("None"),
            height=int(self.parent["height"]))
        with Drawing() as draw:
            draw.stroke_width = 1
            draw.stroke_color = Color("Red")
            draw.fill_color = Color("None")
            draw.rectangle(left=self["left"], width=self["width"],
                top=self["top"], height=self["height"])
            draw(img)
        img.trim()
        return img

    @property
    def attributes(self):
        attributes = {}
        for dimension in self.dimensions.values():
            attributes.update(dimension.attributes)
        return attributes

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}"
            for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, {attributes})"

    def __getitem__(self, key):
        # identify x or y
        mapped_x_key = self.x.map_bound(key)
        mapped_y_key = self.y.map_bound(key)
        if mapped_x_key is not None:
            if self.x.is_bounded:
                return self.x.bounds[mapped_x_key]
            else:
                raise NotBoundedError(f"{self.name}.x.bounds have not been initialised.")
        elif mapped_y_key is not None:
            if self.y.is_bounded:
                return self.y.bounds[mapped_y_key]
            else:
                raise NotBoundedError(f"{self.name}.y.bounds have not been initialised.")
        else:
            raise ValueError("Invalid key")

class PointLayer(Layer):
    """
    A PointLayer's bounds are determined by it's content width and height and
    therefore only require 1 x and y bounding descriptor.
    """
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 1, 1, *args, **kwargs)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        if value is not None:
            self.pre_render = self.render(True)
            self.dimensions["x"].attributes["width"] = NA(self.pre_render.width)
            self.dimensions["y"].attributes["height"] = NA(self.pre_render.height)
        else:
            self.pre_render = None
            self.dimensions["x"].attributes["width"] = None
            self.dimensions["y"].attributes["height"] = None

class ShapeLayer(Layer):
    """A ShapeLayer's bounds are determined by the width and height set at
    initialization and therefore requires 2 x and y bounding descriptors."""
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 2, 2, *args, **kwargs)

class XDefinedLayer(Layer):
    """An XDefinedLayer's x coords are defined (2 are neccessary), but only y
    coord is required."""
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 2, 1, *args, **kwargs)
        self.dimensions["x"].update_bounds()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        if value is not None:
            self.pre_render = self.render(True)
            self.dimensions["y"].attributes["height"] = NA(self.pre_render.height)
        else:
            self.pre_render = None
            self.dimensions["y"].attributes["height"] = None


