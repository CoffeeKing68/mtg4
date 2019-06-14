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
    def is_evaluted(self):
        return hasattr(self, "evaluated_value")

    def __repr__(self):
        return self.__str__()
        # try:
        #     evaluate = self.evaluated_value
        # except:
        #     evaluate = "NULL"
        # return f"{self.__class__.__name__}: {'-' if self.negative else ''}{self.attr}, evaluated_value: {evaluate}"

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
    # def __init__(self, attrs):
    #     self.attrs = []
    #     for attr in attrs:
    #         self.attrs.append(Attribute.childSort(attr))

    # def evaluate(self, template):
    #     for attr in self.attrs:
    #         attr.evaluate(template)

    # def isValid(attr):


class StringAttribute(Attribute):
    def __init__(self, attr, *args, **kwargs):
        super().__init__(attr, *args, **kwargs)

    def evaluate(self, template):
        layer, attr = self.attr.split(".")
        attribute = template.getLayer(layer).attribute
        if attribute.is_evaluted:
            self.evaluated_value = attribute.evaluated_value
            return self.negate()
        else:
            return None

    def isValid(attr):
        """
        :attr: Be a string and in <layer>.<attribute> format.
        """
        try:
            layer, attribute = attr.split('.')
            return isinstance(attr, str) and match("\D+", layer) and match("\D+", attribute) and "," in attr
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

    def evaluate(self, template):
        self.evaluated_value = int(self.attr)
        return self.negate()

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


if __name__ == "__main__":
    attr = "parent.width"
    sAt = StringAttribute(attr)
    nAt = NumericAttribute("45", negative=True)
    print(sAt)
    print(nAt.evaluate(1))

# GetAttribute("")
# SumAttribute("parent.width", NegateAttribute("text.height"))
# "template.width,-45", "fill:template.width,template.height"
# "get:template.width|negate:45" ""
# SumAttributes(StringAttribute("template.width"), NumericAttribute(45, negative=True))
