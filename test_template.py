import pytest
import template
from attribute import StringAttribute, NumericAttribute

class TestPointTextLayer():
    def test_can_make_a_text_layer_without_content(self):
        l = template.PointTextLayer("layer", "Arial", 12, "Black", left=NumericAttribute(30), top=StringAttribute("45"))

    def test_cannot_make_text_layer_with_bad_coords(self):
        with pytest.raises(ValueError):
            template.PointTextLayer("layer", "Arial", 12, "Black", test=StringAttribute("parent.height"), wow=NumericAttribute(12))

    def test_a_text_layer_requires_1_x_y_coord(self):
        with pytest.raises(ValueError):
            template.PointTextLayer("layer", "Arial", 12, "Black")
            template.PointTextLayer("layer", "Arial", 12, "Black", left=NumericAttribute(40), XP30=NumericAttribute(20))

    def test_can_make_a_text_layer_with_content(self):
        l = template.PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumericAttribute(30), top=StringAttribute("45"))

    def test_text_later_will_prerender_when_content_is_set(self):
        l = template.PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NumericAttribute(30), top=StringAttribute("45"))
        assert l.pre_render is not None

    def test_can_make_a_text_layer_with_percent_bounds(self):
        l = template.PointTextLayer("layer", "Arial", 12, "Black", YP40=NumericAttribute(30), XP50_50=StringAttribute("title.left"))

