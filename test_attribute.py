from attribute import StringAttribute, NumericAttribute
from template import Template, PointTextLayer, ColorLayer
import pytest

# GetAttribute("")
# SumAttribute("parent.width", NegateAttribute("text.height"))
# "template.width,-45", "fill:template.width,template.height"
# "get:template.width|negate:45" ""
# SumAttributes(StringAttribute("template.width"), NumericAttribute(45, negative=True))

class TestStringAttribute():
    def test_can_make_string_attribute(self):
        StringAttribute("layer.width")
        StringAttribute("parent.XP40")
        StringAttribute("template.right")

    def test_can_make_negative_string_attribute(self):
        """Tests if negative StringAttributes can be initialised
        and if the different conventions will produce the same result"""
        negative_str_attr_1 = StringAttribute("-title.right")
        negative_str_attr_2 = StringAttribute("title.right", True)

        # test_layer_1 and test_layer_2 will have same left value
        title = PointTextLayer("title", "Arial", 15, "Black", content="Hello World",
            left=NumericAttribute(0), top=NumericAttribute(0))

        test_layer_1 = ColorLayer("test_layer_1", content="Blue",
            left=negative_str_attr_1, right=StringAttribute("parent.right"),
            top=StringAttribute("title.top"), height=NumericAttribute(20))

        test_layer_2 = ColorLayer("test_layer_2", content="Green",
            left=negative_str_attr_2, right=StringAttribute("parent.right"),
            top=StringAttribute("test_layer_1.top"), height=NumericAttribute(20))

        temp = Template("temp", title, test_layer_1, test_layer_2,
            left=NumericAttribute(0), width=NumericAttribute(100),
            top=NumericAttribute(0), height=NumericAttribute(100))

        temp.update_bounds()
        assert test_layer_1["left"] == test_layer_2["left"]

class TestNumericAttribute():
    def test_can_make_nueric_attribute(self):
        NumericAttribute(40)
        NumericAttribute(-30)
        NumericAttribute(12, True)

    def test_can_make_negative_numeric_attribute(self):
        """Tests if negative NumericAttributes can be initialised
        and if the different conventions will produce the same result"""
        negative_num_attr_1 = NumericAttribute(-30)
        negative_num_attr_2 = NumericAttribute(30, True)

        # test_layer_1 and test_layer_2 will have same left value
        title = PointTextLayer("title", "Arial", 15, "Black", content="Hello World",
            left=NumericAttribute(0), top=NumericAttribute(0))

        test_layer_1 = ColorLayer("test_layer_1", content="Blue",
            left=negative_num_attr_1, right=StringAttribute("parent.right"),
            top=StringAttribute("title.top"), height=NumericAttribute(20))

        test_layer_2 = ColorLayer("test_layer_2", content="Green",
            left=negative_num_attr_2, right=StringAttribute("parent.right"),
            top=StringAttribute("test_layer_1.top"), height=NumericAttribute(20))

        temp = Template("temp", title, test_layer_1, test_layer_2,
            left=NumericAttribute(0), width=NumericAttribute(100),
            top=NumericAttribute(0), height=NumericAttribute(100))

        temp.update_bounds()
        assert test_layer_1["left"] == test_layer_2["left"]

