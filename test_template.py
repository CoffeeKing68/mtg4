import pytest
from template import Template, ColorLayer, ColorBackgroundLayer
from text_layers import PointTextLayer, AreaTextLayer
from attribute import StringAttribute as StrAttr
from attribute import NumericAttribute as NumAttr

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

    # def test_this_configuration_can_render(self):
    #     pt = ColorLayer("color_layer", content="Red", left=StrAttr("parent.left"),
    #         top=StrAttr("parent.top"), height=NumAttr(50), width=NumAttr(50))
    #     bg = ColorBackgroundLayer("bg_layer", content="Green")
    #     temp = Template("temp",  pt, bg, XP40=NumAttr(30), right=StrAttr("color_layer.right"),
    #             top=StrAttr("parent.top"), height=NumAttr(100))
    #     temp2 = Template("temp2", temp, left=NumAttr(0), right=NumAttr(200),
    #             top=NumAttr(0), height=NumAttr(200))

    #     temp2.update_bounds()
    #     image = temp2.render()

