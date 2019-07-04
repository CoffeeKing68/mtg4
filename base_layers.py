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
        return all(dim.is_bounded for dim in self.dimensions.values())

    def unset_bounds_and_attributes(self):
        """Method responsible for unsetting evaluated values."""
        for dim in self.dimensions.values():
            dim.bounds = None
            for attributes in dim.attributes.values():
                attributes.unset_evaluated_value()

    def update_bounds(self):
        return [dim.update_bounds() for dim in self.dimensions.values()]

    @abstractmethod
    def render(self, fresh=False):
        pass

    def render_boundary(self):
        """Draws a rectangle around bounds."""
        img = Image(width=int(self.parent["width"]),
            height=int(self.parent["height"]), background=Color("Transparent"))
        with Drawing() as draw:
            draw.stroke_width = 1
            draw.stroke_color = Color("Red")
            draw.fill_color = Color("None")
            draw.rectangle(left=int(self["left"]), width=int(self["width"]),
                top=int(self["top"]), height=int(self["height"]))
            draw(img)
        with Drawing() as draw:
            draw.fill_color = Color("Black")
            draw.font_size = 14
            draw.text(int(self["left"] + 1), int(self["top"] + self["height"] + 1), self.name)
            draw(img)
        img.trim()
        return img

    def color_overlay(self, color, fresh=False):
        # re-render is Fresh == True, you don't own pre_color_overlay or it's None
        if fresh or not hasattr(self, "pre_color_overlay") or self.pre_color_overlay is None:
            if self.pre_render is None:
                pre_render = self.render(fresh=fresh)
            else:
                pre_render = self.pre_render
            color_overlay = pre_render.clone()
            color_overlay.opaque_paint(Color("Transparent"), Color(color), invert=True, channel="RGB")
            self.pre_color_overlay = color_overlay
        return self.pre_color_overlay

    def shadow(self, x, y, radius=2, sigma=4, fresh=False, color="Black"):
        if fresh or not hasattr(self, "pre_shadow") or self.pre_shadow is None:
            shadow = self.color_overlay(color, fresh=False).clone()
            image = Image(width=int(self.template["width"]), height=int(self.template["height"]))
            image.composite(shadow, int(self["left"]) + x, int(self["top"]) + y)
            image.blur(radius, sigma)
            self.pre_shadow = image
        return self.pre_shadow

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
            self.dimensions["x"].attributes["width"] = NA(0)
            self.dimensions["y"].attributes["height"] = NA(0)

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
            self.dimensions["y"].attributes["height"] = NA(0)


