from abc import ABC, abstractmethod
from attribute import Attribute, NumericAttribute, StringAttribute
# import re

class Layer(ABC):

    x_coords = ["left", "xcenter", "right"]
    y_coords = ["top", "ycenter", "bottom"]

    x_width = ["width"]
    y_height = ["height"]

    @property
    def acceptable_coords():
        return x_coords + y_coords + x_width + y_height

    @property
    def acceptable_x_coords():
        return x_coords + x_width

    @property
    def acceptable_y_coords():
        return y_coords + y_height

    def validateAttributes(kwargs, coords, amount):
        """
        :param kwargs: The kwargs passed into the init method for the layer (only the coordinate
        arguments are neccessary).
        :param coords: A list of acceptable coords (e.g. Layer.x_coords + Layer.x_width).
        :param amount: The amount of coords neccessary to define Layer.
        :returns: True on valid or ValueError on failure. (Maybe returns attributes for convenience)
        """
        attributes = {}
        for coord in coords: # foreach coord in acceptable coords
            if coord in kwargs: # is this layer defined by this coord?
                if isinstance(kwargs[coord], Attribute): # is this coord an Attribute?
                    attributes[coord] = kwargs[coord]
                else:
                    raise ValueError("You must pass an Attribute object for an coord.")

        if len(attributes) > amount:
            raise ValueError("You passed in too many coordinates")
        elif len(attributes) < amount:
            raise ValueError("You passed in too few coordinates")
        else:
            return attributes

    @abstractmethod
    def render():
        pass

    # @abstractmethod
    def setXBounds():
        """
        Sets the bounds dictionary for layer objects.
        Layer.bounds = dict full of evaluted values for each coord.
        """
        pass

    def setYBounds():
        pass

    @property
    def is_bounded(self):
        return self.is_x_bounded() and self.is_y_bounded()

    @property
    def is_x_bounded(self): # are there at least 2 x coords in bounds?
        pass

    @property
    def is_y_bounded(self):
        pass



    def __repr__(self):
        return self.__str__()

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, {attributes})"

class PointLayer(Layer):
    """
    A PointLayer should only require 1 x and 1 y coord.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        x_attributes = Layer.validateAttributes(kwargs, self.x_coords, 1)
        y_attributes = Layer.validateAttributes(kwargs, self.y_coords, 1)
        self.attributes = {**x_attributes, **y_attributes}

    # def __str__(self):
        # return f"{self.__class__.__name__}: {self.name}"

class ShapeLayer(Layer):
    """
    A ShapeLayer requires 2 x and 2 y coords.
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        x_attributes = Layer.validateAttributes(kwargs, self.x_coords + self.x_width, 2)
        y_attributes = Layer.validateAttributes(kwargs, self.y_coords + self.y_height, 2)
        self.attributes = {**x_attributes, **y_attributes}


    def setBounds():
        Layer.setBounds()
    # def __str__(self):
    #     return f"{self.__class__.__name__}: {self.name}"


class PointTextLayer(PointLayer):
    """
    A PointTextLayer is only defined by an xy coord.
    The text width is limited only by it's parent's width
    """
    def __init__(self, name, content, *args, **kwargs):
        self.content = content
        super().__init__(name, *args, **kwargs)

    def render(fresh=False):
        pass

    def setBounds():
        pass

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"{self.__class__.__name__}({self.name}, \"{self.content}\", {attributes})"


    # def __repr__(self):
    #     return super().__str__()

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
    def layers(self, layers):
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
    layer = PointTextLayer("title", "Doom Whisperer", left=NumericAttribute(40), top=NumericAttribute(40))
    layers = [layer]
    temp = Template("test", *layers, left=NumericAttribute(0), width=NumericAttribute(750), top=NumericAttribute(0),
            height=NumericAttribute(1050))
    print(layer)
    print(temp)
    temp.setBounds()
