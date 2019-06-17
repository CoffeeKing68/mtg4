import pytest
from template import Template, ColorLayer
from text_layers import PointTextLayer, AreaTextLayer
from attribute import StringAttribute as StrAttr
from attribute import NumericAttribute as NumAttr

class TestLayer():
    def test_can_order_layers_for_rendering(self):
        kwargs = {
            "left": StrAttr("parent.left"),
            "right": StrAttr("parent.right"),
            "top": StrAttr("parent.top"),
            "bottom": StrAttr("parent.bottom")
        }
        l1 = ColorLayer("layer_1", content="#FF0000", order=1, **kwargs)
        l2 = ColorLayer("layer_1", content="#00FF00", order=2, **kwargs)
        temp = Template("temp", l1, l2, left=NumAttr(0), width=NumAttr(50),
            top=NumAttr(0), height=NumAttr(50))

        temp.update_bounds()

        green_above = temp.render()
        color_of_top_left_most_pixel = green_above.export_pixels(width=1, height=1)
        # RGBA, [1] is green
        assert color_of_top_left_most_pixel[:3] == [0, 255, 0]

        l1.order = 3 # move red above
        red_above = temp.render()
        color_of_top_left_most_pixel = red_above.export_pixels(width=1, height=1)
        assert color_of_top_left_most_pixel[:3] == [255, 0, 0]

    def test_layers_passed_in_first_without_order_are_rendered_first(self):
        kwargs = {
            "left": StrAttr("parent.left"),
            "right": StrAttr("parent.right"),
            "top": StrAttr("parent.top"),
            "bottom": StrAttr("parent.bottom")
        }
        l1 = ColorLayer("layer_1", content="#FF0000", **kwargs) # red
        l2 = ColorLayer("layer_1", content="#00FF00", **kwargs) # green
        # l1 is first, is rendered first; therefore l2 (green) should be on top
        temp = Template("temp", l1, l2, left=NumAttr(0), width=NumAttr(50),
            top=NumAttr(0), height=NumAttr(50))
        temp.update_bounds()

        green_above = temp.render()
        color_of_top_left_most_pixel = green_above.export_pixels(width=1, height=1)
        assert color_of_top_left_most_pixel[:3] == [0, 255, 0] # RGBA, [1] is green

        # remake template, now l2 is first, l1 rendered last
        temp = Template("temp", l2, l1, left=NumAttr(0), width=NumAttr(50),
            top=NumAttr(0), height=NumAttr(50))
        temp.update_bounds()
        red_above = temp.render()

        color_of_top_left_most_pixel = red_above.export_pixels(width=1, height=1)
        assert color_of_top_left_most_pixel[:3] == [255, 0, 0]

class TestShapeLayer():
    # ShapeLayer is abstract so testing using AreaTextLayer
    def area_text_layer(self):
        return AreaTextLayer("area_text_layer", "Arial", 12, "Black", left=NumAttr(0), width=NumAttr(40), bottom=NumAttr(50), height=NumAttr(50))

    def test_can_make_a_shape_layer(self):
        layer = self.area_text_layer()

    def test_can_update_x_bounds(self):
        layer = self.area_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.x.update_bounds()

    def test_can_update_y_bounds(self):
        layer = self.area_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.y.update_bounds()

class TestPointLayer():
    # PointLayer is abstract so testing on concrete object PointTextLayer
    def point_text_layer(self):
        return PointTextLayer("area_text_layer", "Arial", 12, "Black", content="test", left=NumAttr(0), bottom=NumAttr(50))

    def test_can_make_a_point_layer(self):
        layer = self.point_text_layer()

    def test_can_update_x_bounds_when_attributes_are_evaluatable_and_content_is_set(self):
        layer = self.point_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.x.update_bounds()

    def test_can_update_y_bounds_when_attributes_are_evaluatable_and_content_is_set(self):
        layer = self.point_text_layer()
        temp = Template("temp", layer, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        layer.y.update_bounds()

