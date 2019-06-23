from abc import ABC, abstractmethod
from re import match
from exceptions import NotBoundedError, NotReadyToEvaluate

class Attribute(ABC):
    negative_char = "-"
    absolute_char = "!" # #/^/*/&

    def __init__(self, attr, negative=False, absolute=False):
        self.evaluated_value = None
        self.dimension = None
        while True:
            if attr[0] == Attribute.negative_char:
                attr = attr[1:]
                negative = True
            elif attr[0] == Attribute.absolute_char:
                attr = attr[1:]
                absolute = True
            else:
                break

        self.attr = attr
        self.negative = negative
        self.absolute = absolute

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

    @property
    def evaluated_value(self):
        return self.last_pass()

    @evaluated_value.setter
    def evaluated_value(self, value):
        self._evaluated_value = value

    def last_pass(self):
        ev = self._evaluated_value
        if ev is not None:
            try:
                ev = self.negate(ev)
                ev = self.absolutify(ev)
            except NotReadyToEvaluate:
                return None
        return ev

    def negate(self, value):
        if self.negative:
            value = -value
        return value

    def absolutify(self, value):
        # print("bounds", self.dimension.layer.name)
        # if not self.absolute and self.dimension.layer.parent is not None: # is relative
        #     try:
        #         pd = self.dimension.layer.parent.dimensions[self.dimension.name]
        #         # print(pd.layer)
        #         value += pd.bounds["start"]
        #     except:
        #         raise NotReadyToEvaluate
        return value

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

# class FunctionAttribute(Attribute):
#     def __init__(self, *attrs, negative=False, absolute=False):
#         self.attrs = attrs
#         for attr in self.attrs:
#             self.dimension = None
#         super().__init__(None, negative, absolute)

#     @property
#     def dimension(self):
#         return self._dimension

#     @dimension.setter
#     def dimension(self, value):
#         self._dimension = value
#         for attr in self.attrs:
#             attr.dimension = value

#     def evaluate(self):
#         for attr in self.attrs:
#             attr.evaluate()

#     @property
#     def is_evaluated(self):
#         return all(attr.is_evaluated for attr in self.attrs)

#     def isValid(attr):
#         """
#         :attr: Be a string and in <layer>.<attribute> format.
#         """
#         return isinstance(attr, Attribute)

# class AddAttribute(FunctionAttribute):
#     @property
#     def evaulated_value(self):
#         try:
#             return sum(attr.evaluated_value for attr in self.attrs)
#         except:
#             return None

#     def __short_class_name__(self):
#         return "AddAttr"

class StringAttribute(Attribute):
    """
    eg. <>.<left/xcenter/right/width/
    :accepted layers: layer.name, template, parent
    :accepted attributes:
        left, xcenter, right, width
        top, ycenter, bottom, height
        XP<pct>, YP<pct>
    """
    def evaluate(self):
        if self.evaluated_value is None:
            l, attr = self.attr.split(".")
            llayer = self.dimension.layer
            if l == "parent" and llayer.parent is not None:
                layer = llayer.parent
            elif l == "template" and llayer.template is not None:
                layer = llayer.template
            else:
                template = llayer.template
                if llayer.template is None:
                    template = llayer
                layer = template.get_layer(l)
            try:
                self.evaluated_value = layer[attr]
                return self.evaluated_value
            except NotBoundedError: # Don't complain if not bounded
                pass # complain if bad key (see Layer.__getitem__)
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

    def evaluate(self):
        if self.evaluated_value is None:
            self.evaluated_value = int(self.attr)
            return self.evaluated_value
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

