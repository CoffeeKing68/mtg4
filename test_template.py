import pytest
from template import Template, PointTextLayer
from attribute import StringAttribute as StrAttr
from attribute import NumericAttribute as NumAttr

class TestPointTextLayer():
    def test_can_make_a_text_layer_without_content(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", left=NumAttr(30), top=StrAttr("45"))

    def test_cannot_make_text_layer_with_bad_coords(self):
        with pytest.raises(ValueError):
            PointTextLayer("layer", "Arial", 12, "Black", test=StrAttr("parent.height"), wow=NumAttr(12))

    def test_a_text_layer_requires_1_x_y_coord(self):
        with pytest.raises(ValueError):
            PointTextLayer("layer", "Arial", 12, "Black")
            PointTextLayer("layer", "Arial", 12, "Black", left=NumAttr(40), XP30=NumAttr(20))

    def test_can_make_a_text_layer_with_content(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=StrAttr("45"))

    def test_point_text_layer_can_render_when_content_and_parent_is_set(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=StrAttr("45"))
        temp = Template("temp", l, left=NumAttr(0), width=NumAttr(50), top=NumAttr(0), height=NumAttr(50))
        l.render(True)
        assert l.pre_render is not None

    def test_can_make_a_text_layer_with_percent_bounds(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", YP40=NumAttr(30), XP50_50=StrAttr("title.left"))

# add Groups
# A group is a template in it's current form, except won't set self._template on __init__

class TestTemplateLayer():
    def test_can_make_template_layer(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumAttr(30), top=StrAttr("45"))
        temp = Template("temp", l, left=NumAttr(0), width=NumAttr(50),
                top=NumAttr(0), height=NumAttr(50))

