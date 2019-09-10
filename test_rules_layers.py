import pytest
from template import Template, ColorLayer, ColorBackgroundLayer, RulesText
from text_layers import PointTextLayer, AreaTextLayer
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from wand.compat import nested

class TestRulesLayer():
    def test_get_bottom_base_of_rules_layer(self):
        rules_content = "These are\nthe rules."
        bg = ColorBackgroundLayer("bg", content="White")
        sqr = ColorLayer("square", left=NA(0), width=NA(20), top=NA(0), height=NA(20))
        # l = PointTextLayer("l", "Arial", 12, "Black", content="Hpqrs", left=NA(0), base=NA(20))
        # l2 = PointTextLayer("l2", "Arial", 12, "Black", content="e", left=NA(10), median=NA(50))
        # l4 = PointTextLayer("l4", "Arial", 12, "Black", content="l", left=NA(30), cap=NA(50))

        rules = RulesText("rules", "Arial", "Arial", 12, color="Black", left=NA(0),
            width=NA(100), bottom=NA(30), content=rules_content)

        temp = Template("temp", rules, bg, left=NA(0),
                width=NA(100), top=NA(0), height=NA(50))
        temp.update_bounds()
        temp.render().save(filename="test_images/test_get_bottom_base_of_rules_layer.png")

