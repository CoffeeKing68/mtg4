from bounds import Bounds
from exceptions import NotEvaluatedError

class Dimension():
    def __init__(self, pct, mapping, amount, bounds=None, **attributes):
        self.amount = amount
        self.attributes = self.validate_attributes(attributes)
        self.pct = pct # YP/XP
        self.mapping = mapping # {top: start, right: end, height: full}
        self.bounds = bounds # None if bounds is not present

    def is_evaluated(self):
        """Will check it's attributes if they are all evaluated."""
        return all(attr.is_evaluated for attr in self.attributes.values())

    def map_bound(self, descriptor):
        """Maps dimension specific bound descriptors to standard Bounds
        conventions. eg. left/top -> start, XP40/YP40 -> P40."""
         if descriptor in self.mapping: # if is left, top, height
            return self.mapping[descriptor]
        elif descriptor[:2].upper() == self.pct.upper(): # is pct
            # change . to _ for bounds method
            parsed_pct = str(Bounds.parse_pct(descriptor[1:])).replace(".", "_")
            return f"P{parsed_pct}"

    def validate_attributes(self, attributes):
        """Validates attribute keys to make sure they are valid and that the
        correct amount have been passed in."""
        attributes = {}
        for key, argument in attributes.items():
            mapped_key = self.map_bound(key)
            if mapped_key is not None: # is valid bound descriptor
                attributes[key] = argument

        if len(attributes) > amount:
            raise ValueError("You passed in too many attributes")
        elif len(attributes) < amount:
            raise ValueError("You passed in too few attributes")
        else:
            return attributes

    def attributes_to_bounds(self, layer):
        """If all attributes are evaluated, will return a dict with Standard
        Bound names and the attributes evaluated_value."""
        for attribute in self.attributes.values():
            attribute.evaluate(layer.template, layer.parent)
        if all(a.is_evaluated for a in attributes.values()): # all attributes evaled?
            bounds = {}
            for descriptor, attribute in attributes.items():
                bounds[mapper(descriptor)] = attribute.evaluated_value
            return bounds
        else:
            raise NotEvaluatedError(f"Layer {self.name}'s attributes can't be evaluated right now")

    def is_bounded(self):
        """Returns True if Dimension has a bounds object that is not None."""
        return self.bounds is not None

class XDimension(Dimension):
    def __init__(self, amount, bounds=None, **attributes):
        mapping = {
            "left": "start",
            "xcenter": "center",
            "right": "end"
            "width": "full"
        }
        super().__init__("XP", mapping, amount, bounds, **attributes)

class YDimension(Dimension):
    def __init__(self, amount, bounds=None, **attributes):
        mapping = {
            "top": "start",
            "ycenter": "center",
            "bottom": "end"
            "height": "full"
        }
        super().__init__("YP", mapping, amount, bounds, **attributes)

