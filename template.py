from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
from bounds import Bounds
from exceptions import InvalidBoundsError, NotEvaluatedError, NotBoundedError
from exceptions import NotReadyToRenderError

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

# TODO adaptive_sharpen for ImageLayers

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
        self.content = None
        self.template = None
        self.x_bounds = None
        self.y_bounds = None
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
        for key, argument in kwargs.items():
            mapped_key = mapper(key)
            if mapped_key is not None: # is valid bound descriptor
                attributes[key] = argument

        if len(attributes) > amount:
            raise ValueError("You passed in too many coordinates")
        elif len(attributes) < amount:
            raise ValueError("You passed in too few coordinates")
        else:
            return attributes

    def attributes_to_bounds(self, attributes, mapper):
        for attribute in attributes.values():
            attribute.evaluate(self.template, self.parent)
        if all(a.is_evaluated for a in attributes.values()): # all attributes evaled?
            bounds = {}
            for descriptor, attribute in attributes.items():
                bounds[mapper(descriptor)] = attribute.evaluated_value
            return bounds
        else:
            raise NotEvaluatedError(f"Layer {self.name}'s attributes can't be evaluated right now")

    def x_attributes_to_bounds(self):
        return self.attributes_to_bounds(self.x_attributes, self.map_x_bound)

    def y_attributes_to_bounds(self):
        return self.attributes_to_bounds(self.y_attributes, self.map_y_bound)

    @property
    def is_bounded(self):
        return all([self.is_x_bounded, self.is_y_bounded])

    @property
    def is_x_bounded(self):
        return self.x_bounds is not None

    @property
    def is_y_bounded(self):
        return self.y_bounds is not None

    @abstractmethod
    def render(self, fresh=True):
        pass

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
        if mapped_x_key is not None:
            if self.is_x_bounded:
                return self.x_bounds[mapped_x_key]
            else:
                raise NotBoundedError(f"{self.name}.x_bounds have not been initialised.")
        elif mapped_y_key is not None:
            if self.is_y_bounded:
                return self.y_bounds[mapped_y_key]
            else:
                raise NotBoundedError(f"{self.name}.y_bounds have not been initialised.")
        else:
            raise ValueError("Invalid key")

class PointLayer(Layer):
    """
    A PointLayer's bounds are determined by it's content width and height and
    therefore only require 1 x and y bounding descriptor.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.x_attributes = self.validate_attributes(kwargs, self.map_x_bound, 1)
        self.y_attributes = self.validate_attributes(kwargs, self.map_y_bound, 1)
        super().__init__(*args, **kwargs)

    def update_x_bounds(self):
        self.render() # generate a pre_render
        try:
            bounds = self.x_attributes_to_bounds()
            self.x_bounds = Bounds(**bounds, full=self.pre_render.width)
            return self.x_bounds
        except NotEvaluatedError:
            pass

    def update_y_bounds(self):
        self.render() # generate a pre_render
        try:
            bounds = self.y_attributes_to_bounds()
            self.y_bounds = Bounds(**bounds, full=self.pre_render.height)
            return self.y_bounds
        except NotEvaluatedError:
            pass

    def update_bounds(self):
        return self.update_x_bounds(), self.update_y_bounds()

class ShapeLayer(Layer):
    """A ShapeLayer's bounds are determined by the width and height set at initialization
    and therefore requires 2 x and y bounding descriptors."""
    def __init__(self, name, *args, **kwargs):
        self.name = name
        # TODO: remove bounds return from validate_attributes
        self.x_attributes = self.validate_attributes(kwargs, self.map_x_bound, 2)
        self.y_attributes = self.validate_attributes(kwargs, self.map_y_bound, 2)
        super().__init__(*args, **kwargs)

    def update_x_bounds(self):
        try:
            bounds = self.x_attributes_to_bounds()
            self.x_bounds = Bounds(**bounds)
            return self.x_bounds
        except NotEvaluatedError:
            pass

    def update_y_bounds(self):
        try:
            bounds = self.y_attributes_to_bounds()
            self.y_bounds = Bounds(**bounds)
            return self.y_bounds
        except NotEvaluatedError:
            pass

    def update_bounds(self):
        return self.update_x_bounds(), self.update_y_bounds()

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
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            with Drawing() as draw:
                draw.font = self.font
                draw.font_size = self.size
                if not isinstance(self.color, Color):
                    self.color = Color(self.color)
                draw.color = self.color
                draw.text_antialias = True
                # get estimated width and height
                with Image(width=1, height=1) as temp_image:
                    metrics = draw.get_font_metrics(temp_image, self.content)
                    width = int(metrics.text_width)
                    height = int(metrics.text_height)

                img = Image(width=width + 100, height=height + 100)
                draw.text(10, height + 10, self.content)
                draw(img)
            img.trim()
            self.pre_render = img
            return img
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

class AreaTextLayer(ShapeLayer):
    """TextLayer that has a rect (Shape)."""
    def __init__(self, name, font, size, color, *args, **kwargs):
        self.font = font
        self.size = size
        self.color = color
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        pass

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
        # temp_image.save(filename="testing_3.png")

