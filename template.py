from base_layers import Layer, ShapeLayer, PointLayer, XDefinedLayer
from text_layers import PointTextLayer
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA
from attribute import MaxAttribute as MaxA
from attribute import MinAttribute as MinA
from attribute import MultiplyAttribute as MulA
from attribute import DivideAttribute as DivA

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from mtgpy import ManaText, Rules, Text

from os.path import join

class ColorLayer(ShapeLayer):
    """A ShapeLayer that has 1 solid color."""
    def render(self, fresh=False):
        if fresh and self.pre_render is not None:
            return self.pre_render
        elif self.content is not None:
            if not isinstance(self.content, Color):
                self.content = Color(self.content)
            img = Image(width=int(self["width"]), height=int(self["height"]), background=self.content)
            return img
        else:
            raise NotReadyToRenderError("Content is needed to render ColorLayer.")

class ColorBackgroundLayer(ColorLayer):
    def __init__(self, name, *args, **kwargs):
        kwargs["left"] = SA("parent.left")
        kwargs["right"] = SA("parent.right")
        kwargs["top"] = SA("parent.top")
        kwargs["bottom"] = SA("parent.bottom")
        if "order" not in kwargs:
            kwargs["order"] = -99
        super().__init__(name, **kwargs)

class Template(ShapeLayer):
    """Layers that appear first in *layers arg are rendered first if order is
    not specified (order = 0 by default)."""
    def __init__(self, name, *layers, **kwargs):
        self.layers = layers
        super().__init__(name, **kwargs)

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers):
        for l in layers:
            l.parent = self
            l.template = self
        self._layers = layers

    @property
    def are_layers_bounded(self):
        return all(l.is_bounded for l in self.layers)

    def update_bounds(self):
        tries = 0
        def update_dimensions(layer):
            should_reset = False
            for dim in layer.dimensions.values():
                bounded_before = dim.is_bounded
                # if not bounded_before:
                dim.update_bounds()
                if dim.is_bounded and not bounded_before:
                    should_reset = True
            return should_reset

        while tries < 3:
            tries += 1
            if update_dimensions(self):
                tries = 0
            for l in self.layers:
                if isinstance(l, Template):
                    l.update_bounds()
                else:
                    if update_dimensions(l):
                        tries = 0

    def unset_bounds_and_attributes(self):
        super().unset_bounds_and_attributes()
        for l in self.layers:
            l.unset_bounds_and_attributes()

    def render(self, fresh=False):
        image = Image(width=int(self["width"]), height=int(self["height"]))
        for layer in sorted(self.layers, key=lambda l: l.order):
            if layer.content is not None:
                img = layer.render(fresh)
                if img is not None:
                    image.composite(img, left=int(layer["left"]), top=int(layer["top"]))
        return image

    def render_boundary(self):
        image = Image(width=int(self["width"]), height=int(self["height"]),
            background=Color("Transparent"))
        for layer in sorted(self.layers, key=lambda l: l.order):
            img = layer.render_boundary()
            if img is not None:
                image.composite(img, left=int(layer["left"]), top=int(layer["top"]))
        return image

    def __str__(self):
        attributes = ", ".join([f"{key}={attribute.__short_str__()}" for key, attribute in self.attributes.items()])
        return f"Template({self.name}, {attributes})"

    def get_layer(self, key):
        if isinstance(key, Layer):
            key = key.name
        if isinstance(key, str):
            for layer in self.layers:
                if layer.name == key:
                    return layer
                elif isinstance(layer, Template):
                    l = layer.get_layer(key)
                    if l is not None:
                        return l
        else:
            raise ValueError("You can only pass in layer names or layers.")

class ManaCost(PointLayer):
    def __init__(self, name, *args, mana_size=35, mana_gap=2, **kwargs):
        self.mana_size = mana_size
        self.mana_gap = mana_gap
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            self.mana = ManaText.getManaList(self.content)
            width = (len(self.mana) * (self.mana_gap + self.mana_size)) - self.mana_gap
            height = self.mana_size
            img = Image(width=width, height=height)
            antialias = False
            img.antialias = antialias
            offset = self.mana_size
            for mana in self.mana[::-1]:
                msrc = join(self.template.resource_dir, self.template.mana_image_format,
                    f"{mana.mana_string}.{self.template.mana_image_format}")
                mana_image = Image(width=self.mana_size, height=self.mana_size,
                    background=Color("Transparent"), filename=msrc, resolution=300)
                mana_image.antialias = antialias
                img.composite(mana_image, left=width-offset, top=0)
                offset += self.mana_size + self.mana_gap
            self.pre_render = img
            return img
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

class ImageLayer(PointLayer):
    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            img = Image(filename=self.content)
            self.pre_render = img
            return img
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

class ResizeImageLayer(ShapeLayer):
    """Image will be resized to the provided width and height."""
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        # super(ShapeLayer, type(self)).content.fset(self, value)
        if value is None:
            self.initial_width = self.initial_height = 0
        else:
            with Image(filename=value) as img:
                self.initial_width, self.initial_height = img.size

    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            img = Image(filename=self.content)
            img.resize(int(self["width"]), int(self["height"]))
            self.pre_render = img
            return img
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

    def __getitem__(self, key):
        if key == "initial_width":
            return self.initial_width
        elif key == "initial_height":
            return self.initial_height
        else:
            return super().__getitem__(key)

class FitImageLayer(ResizeImageLayer):
    """Sets width and height to fit in shape defined by width and height.
    The ratio of the image is respected."""
    def __init__(self, name, *args, width=None, height=None, **kwargs):
        initial_width = SA("self.initial_width")
        initial_height = SA("self.initial_height")
        ratio_attr = MinA(DivA(width, initial_width), DivA(height, initial_height))
        super().__init__(name, *args, width=MulA(initial_width, ratio_attr),
            height=MulA(initial_height, ratio_attr), **kwargs)

class FillImageLayer(ResizeImageLayer):
    """Sets width and height to fill shape defined by width and height.
    The ratio of the image is respected."""
    def __init__(self, name, *args, width=None, height=None, **kwargs):
        initial_width = SA("self.initial_width")
        initial_height = SA("self.initial_height")
        ratio_attr = MaxA(DivA(width, initial_width), DivA(height, initial_height))
        super().__init__(name, *args, width=MulA(initial_width, ratio_attr),
            height=MulA(initial_height, ratio_attr), **kwargs)

class RulesText(XDefinedLayer):
    def __init__(self, name, font=None, italics_font=None, size=None,
            color=None, mana_size=None, line_gap=None, word_gap=5, mana_gap=2,
            paragraph_gap=2, *args, **kwargs):
        self.font = font
        self.italics_font = italics_font
        self.size = size
        self.color = color
        self.mana_size = mana_size
        self.word_gap = word_gap
        self.line_gap = size if line_gap is None else line_gap
        self.paragraph_gap = paragraph_gap
        self.mana_gap = mana_gap
        super().__init__(name, *args, **kwargs)

    def get_word_width(self, word):
        WW = 0
        for i, text in enumerate(word):
            if isinstance(text, ManaText):
                WW += self.mana_size
                # not last text item in word and next text is mana
                if i < len(word) - 1 and isinstance(word[i + 1], ManaText):
                    WW += self.mana_gap
            else:
                WW += self.get_text_width(text)
        return WW

    def get_text_width(self, text):
        with Drawing() as draw:
            draw.font = self.font
            if type(text) != Text: # if italics
                draw.font = self.italics_font
            draw.font_size = self.size
            with Image(width=1, height=1) as img:
                return draw.get_font_metrics(img, text.string).text_width

    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is None:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")
        self.rules = Rules(self.content)
        self.x.update_bounds() # set width TODO maybe remove this
        r = []
        Y = 0
        for paragraph in self.rules.paragraphs:
            p = []
            s = []
            X = 0 # New line
            for word in paragraph.words:
                WW = self.get_word_width(word)
                if X + WW + self.word_gap > self["width"]: # overflow on width
                    X = WW
                    Y += self.line_gap
                    p.append(s)
                    s = [word]
                else:
                    s.append(word)
                    X += WW + self.word_gap
            p.append(s)
            Y += self.paragraph_gap + self.line_gap
            r.append(p)

        image = Image(background=Color("Transparent"), width=int(self["width"]),
            height=int(Y+self.size+100))
        CY = self.size + 20
        for p in r:
            for s in p:
                CX = 0
                for j, w in enumerate(s):
                    if j > 0:
                        CX += self.word_gap
                    for i, text in enumerate(w):
                        if isinstance(text, ManaText):
                            # not last text item in word and next text is mana
                            mana_image = Image(width=self.mana_size, height=self.mana_size,
                                filename=join(self.template.resource_dir,
                                    self.template.mana_image_format,
                                    f"{text.mana_string}.{self.template.mana_image_format}"),
                                background=Color("Transparent"))
                            mana_image.antialias = True
                            image.composite(mana_image, left=CX, top=CY - self.mana_size + 2)
                            if i < len(w) - 1 and isinstance(w[i + 1], ManaText):
                                CX += 2
                            CX += self.mana_size
                        else:
                            with Drawing() as draw:
                                draw.font = self.font
                                if type(text) != Text: # if italics
                                    draw.font = self.italics_font
                                draw.font_size = self.size
                                draw.fill_color = self.color
                                with Image(width=1, height=1) as img:
                                    tw = int(draw.get_font_metrics(img, text.string).text_width)
                                draw.text(CX, CY, text.string)
                                draw(image)
                                CX += tw
                CY += self.line_gap
            CY += self.paragraph_gap
        image.trim()
        self.pre_render = image
        return image

