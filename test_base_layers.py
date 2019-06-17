import pytest
from template import Template, ColorLayer
from text_layers import PointTextLayer, AreaTextLayer
from attribute import StringAttribute as StrAttr
from attribute import NumericAttribute as NumAttr

class TestShapeLayer():
    # ShapeLayer is abstract so testing using AreaTextLayer
    def area_text_layer(self):
        return AreaTextLayer("area_text_layer", "Arial", 12, "Black", left=NumAttr(0), width=NumAttr(40), bottom=NumAttr(50), height=NumAttr(50))

    def test_can_make_a_shape_layer(self):
        layer = self.area_text_layer()

    def test_can_update_x_bounds(self):
        layer = self.area_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.update_x_bounds()

    def test_can_update_y_bounds(self):
        layer = self.area_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.update_y_bounds()

class TestPointLayer():
    # PointLayer is abstract so testing on concrete object PointTextLayer
    def point_text_layer(self):
        return PointTextLayer("area_text_layer", "Arial", 12, "Black", left=NumAttr(0), bottom=NumAttr(50))

    def test_can_make_a_point_layer(self):
        layer = self.point_text_layer()

    # def test_can_update_x_bounds(self):
    #     layer = self.point_text_layer()
    #     temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
    #     layer.update_x_bounds()

    # def test_can_update_y_bounds(self):
    #     layer = self.point_text_layer()
    #     temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
    #     layer.update_y_bounds()

