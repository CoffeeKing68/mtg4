import pytest
import template
from attribute import StringAttribute, NumericAttribute

class TestPointTextLayer():
    def test_can_make_a_text_layer_without_content(self):
        l = template.PointTextLayer("layer", left=NumericAttribute(30), top=StringAttribute("45"))

    def test_cannot_make_text_layer_with_bad_coords(self):
        pass

    def test_a_text_layer_requires_1_x_y_coord(self):
        pass

    def test_can_make_a_text_layer_with_content(self):
        l = template.PointTextLayer("layer", content="hello world", left=NumericAttribute(30), top=StringAttribute("45"))

    def test_text_later_will_prerender_when_content_is_set(self):
        l = template.PointTextLayer("layer", content="hello world", left=NumericAttribute(30), top=StringAttribute("45"))
        assert l.pre_render is not None

    def test_can_make_a_text_layer_with_percent_bounds(self):
        l = template.PointTextLayer("layer", YP40=NumericAttribute(30), XP50_50=StringAttribute("45"))
