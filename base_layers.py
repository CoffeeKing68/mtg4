from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
from bounds import Bounds
from exceptions import InvalidBoundsError, NotEvaluatedError, NotBoundedError
from exceptions import NotReadyToRenderError

class Layer(ABC):
    """Base Layer for all Layers to inherit from. Does most of the heavy
    lifting."""
    x_coords = ["left", "xcenter", "right", "width"]
    y_coords = ["top", "ycenter", "bottom", "height"]

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
        return self.is_x_bounded and self.is_y_bounded

    @property
    def is_x_bounded(self):
        return self.x_bounds is not None

    @property
    def is_y_bounded(self):
        return self.y_bounds is not None

    @abstractmethod
    def render(self, fresh=False):
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


