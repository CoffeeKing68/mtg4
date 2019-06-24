import pytest
from template import Template, ColorLayer, ColorBackgroundLayer
from text_layers import PointTextLayer, AreaTextLayer
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA

class TestTemplateLayer():
    def test_can_make_template_layer(self):
        l = PointTextLayer("layer", "Arial", 12, "Black", content="hello world", left=NA(30), top=NA(45))
        temp = Template("temp", l, left=NA(0), width=NA(50), top=NA(0), height=NA(50))

    def test_can_have_templates_within_templates(self):
        pt = PointTextLayer("point_text_layer", content="Point Text Layer", font="Arial", size=35, color="Black",
                left=NA(0), top=NA(0))
        bg = ColorLayer("bg", content="Red", left=NA(0),
                width=SA("parent.width"), height=SA("parent.height"), top=NA(0))
        temp = Template("temp",  pt, bg, left=NA(0), right=SA("point_text_layer.right"),
                top=NA(0), height=NA(100))
        temp2 = Template("temp", temp, left=NA(0), right=SA("point_text_layer.right"),
                top=NA(0), height=NA(500))

        temp2.update_bounds()

    def test_this_configuration_can_render(self):
        pt = PointTextLayer("ptl", "Arial", 15, "Black", content="Hello World", left=AA(SA("parent.left"), NA(5)),
            top=SA("parent.top"))
        bg = ColorBackgroundLayer("bg", content="Green")
        temp = Template("temp",  pt, bg, left=NA(10), right=SA("ptl.right"),
                top=SA("parent.top"), height=NA(100))

        temp2 = Template("temp2", temp, left=NA(0), right=NA(100),
                top=NA(0), height=NA(100))

        temp2.update_bounds()
        image = temp2.render()

    def test_template_can_render_boundary(self):
        pt = PointTextLayer("pt", "Arial", 15, "Black", content="Hello World",
            left=NA(0), top=NA(0))
        square = ColorLayer("square", content="Orange", left=NA(20), top=NA(20),
            height=NA(20), width=NA(20))
        bg = ColorBackgroundLayer("bg", content="None")
        temp = Template("temp",  pt, square, bg, left=NA(0), width=NA(100),
            top=NA(0), height=NA(100))
        temp.update_bounds()
        boundary = temp.render_boundary()
        # boundary.save(filename="test_images/test_template_can_render_boundary_b.png")
        image = temp.render()
        # image.save(filename="test_images/test_template_can_render_boundary_r.png")
        # boundary.composite(image)
        # image.save(filename="test_images/test_template_can_render_boundary_c.png")

