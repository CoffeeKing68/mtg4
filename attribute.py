from abc import ABC, abstractmethod
from re import match

class Attribute(ABC):
    @abstractmethod
    def isValid(attr):
        """
        Way to check if attr is a valid attribute
        :return: boolean
        """
        pass

    @abstractmethod
    def evaluate(self, template):
        pass

    @abstractmethod
    def __init__(self, attr, negative=False):
        self.evaluated_value = None
        if attr[0] == '-':
            self.attr = attr[1:]
            self.negative = True
        else:
            self.attr = attr
            self.negative = negative

    def negate(self):
        if self.negative:
            self.evaluated_value = -self.evaluated_value
        return self.evaluated_value

    @property
    def is_evaluated(self):
        return self.evaluated_value is not None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        try:
            evaluate = self.evaluated_value
        except:
            evaluate = "NULL"
        return f"{self.__class__.__name__}({'-' if self.negative else ''}{self.attr}, {evaluate})"

    def __short_str__(self):
        try:
            evaluate = self.evaluated_value
        except:
            evaluate = "NULL"
        return f"{self.__short_class_name__()}({'-' if self.negative else ''}{self.attr}, {evaluate})"


    @abstractmethod
    def __short_class_name__(self):
        pass

class FunctionAttribute(Attribute):
    pass

class StringAttribute(Attribute):
    """
    eg. <>.<left/xcenter/right/width/
    :accepted layers: layer.name, template, parent
    :accepted attributes:
        left, xcenter, right, width
        top, ycenter, bottom, height
        XP<pct>, YP<pct>
    """
    def __init__(self, attr, *args, **kwargs):
        super().__init__(attr, *args, **kwargs)

    def evaluate(self, template, parent):
        if self.evaluated_value is None:
            l, attr = self.attr.split(".")
            if l == "parent":
                layer = parent
            elif l == "template":
                layer = template
            else:
                layer = template.get_layer(l)
            try:
                # TODO might not work
                self.evaluated_value = layer[attr]
                return self.negate()
            except:
                pass
        else:
            return self.evaluated_value

    def isValid(attr):
        """
        :attr: Be a string and in <layer>.<attribute> format.
        """
        try:
            layer, attribute = attr.split('.')
            return isinstance(attr, str) and match(r"\D+", layer) and match(r"\D+", attribute) and "," in attr
        except:
            return False

    def __short_class_name__(self):
        return "StrAttr"

class NumericAttribute(Attribute):
    def __init__(self, attr, *args, **kwargs):
        """
        :param attr: Can be int or str, might make it int only later?
        """
        if isinstance(attr, int): # pass in number
            if int(attr) < 0: # number is negative
                kwargs["negative"] = True
                attr = str(abs(attr))
            else:
                attr = str(attr)
        super().__init__(attr, *args, **kwargs)

    def evaluate(self, template, parent):
        if self.evaluated_value is None:
            self.evaluated_value = int(self.attr)
            return self.negate()
        else:
            return self.evaluated_value

    def isValid(attr):
        """
        :attr: Be numeric
        """
        try:
            val = float(attr)
            return True
        except ValueError:
            return False

    def __short_class_name__(self):
        return "NumAttr"


# if __name__ == "__main__":
#     attr = "parent.width"
#     sAt = StringAttribute(attr)
#     nAt = NumericAttribute("45", negative=True)
#     print(sAt)
#     print(nAt.evaluate(1))

# GetAttribute("")
# SumAttribute("parent.width", NegateAttribute("text.height"))
# "template.width,-45", "fill:template.width,template.height"
# "get:template.width|negate:45" ""
# SumAttributes(StringAttribute("template.width"), NumericAttribute(45, negative=True))
