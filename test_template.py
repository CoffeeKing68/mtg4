import pytest
from template import Template, PointTextLayer, AreaTextLayer, ColorLayer
from attribute import StringAttribute as StrAttr
from attribute import NumericAttribute as NumAttr

class TestPointTextLayer():
    def test_can_make_a_text_layer_without_content(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", left=NumAttr(30), top=NumAttr(45))

    def test_cannot_make_text_layer_with_bad_coords(self):
        with pytest.raises(ValueError):
            PointTextLayer("layer", "Arial", 12, "Black", test=StrAttr("parent.height"), wow=NumAttr(12))

    def test_a_text_layer_requires_1_x_y_coord(self):
        with pytest.raises(ValueError):
            PointTextLayer("layer", "Arial", 12, "Black")
            PointTextLayer("layer", "Arial", 12, "Black", left=NumAttr(40), XP30=NumAttr(20))

    def test_can_make_a_text_layer_with_content(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=NumAttr(45))

    def test_point_text_layer_can_render_when_content_and_parent_is_set(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=NumAttr(45))
        temp = Template("temp", l, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        temp.update_bounds()
        l.render()
        assert l.pre_render is not None

    def test_can_make_a_text_layer_with_percent_bounds(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", YP40=NumAttr(30), XP50_50=StrAttr("title.left"))

# add Groups
# A group is a template in it's current form, except won't set self._template on __init__

class TestTemplateLayer():
    def test_can_make_template_layer(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=NumAttr(45))
        temp = Template("temp", l, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))

    def test_can_have_templates_within_templates(self):
        pt = PointTextLayer("point_text_layer", content="Point Text Layer", font="Arial", size=35, color="Black",
                left=NumAttr(0), top=NumAttr(0))
        bg = ColorLayer("bg", content="Red", left=NumAttr(0),
                width=StrAttr("parent.width"), height=StrAttr("parent.height"), top=NumAttr(0))
        temp = Template("temp",  pt, bg, left=NumAttr(0), right=StrAttr("point_text_layer.right"),
                top=NumAttr(0), height=NumAttr(100))
        temp2 = Template("temp", temp, left=NumAttr(0), right=StrAttr("point_text_layer.right"),
                top=NumAttr(0), height=NumAttr(500))

        temp2.update_bounds()

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
    # PointLayer is abstrac so testing on concrete object PointTextLayer
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

