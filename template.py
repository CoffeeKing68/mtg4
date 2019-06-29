from base_layers import Layer, ShapeLayer, PointLayer, XDefinedLayer
from text_layers import PointTextLayer
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from mtgpy import ManaText, Rules, Text

from os.path import join

class ColorLayer(ShapeLayer):
    """A ShapeLayer that has 1 solid color."""
    # def __init__(self, name, *args, **kwargs):
    #     super().__init__(name, **kwargs)

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

    def update_bounds(self):
        tries = 0
        while tries < 3:
            tries += 1
            snbx, snby = not self.x.is_bounded, not self.y.is_bounded
            super().update_bounds()
            if snbx and self.x.is_bounded or snby and self.x.is_bounded:
                tries = 0 # started not bounded, but now x/y bounded
            for l in self.layers:
                nbx, nby = not l.x.is_bounded, not l.y.is_bounded
                l.update_bounds()
                if nbx and l.x.is_bounded or nby and l.x.is_bounded:
                    tries = 0

    def render(self, fresh=False):
        image = Image(width=int(self["width"]), height=int(self["height"]))
        for layer in sorted(self.layers, key=lambda l: l.order):
            if layer.content is not None:
                img = layer.render()
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
    def render(self, fresh=False):
        self.mana_size = 35
        self.mana_gap = 2
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
            img.save(filename=join("test_images", "no_antialias.bmp"))
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

class RulesText(XDefinedLayer):
    def __init__(self, name, font=None, italics_font=None, size=None,
            color=None, mana_size=None, *args, **kwargs):
        self.font = font
        self.italics_font = italics_font
        self.size = size
        self.color = color
        self.mana_size = mana_size
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
        self.word_gap = 5
        self.line_gap = self.size
        self.paragraph_gap = 2
        self.mana_gap = 2
        self.x.update_bounds() # set width
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
                                filename=f"resources/svg/{text.mana_string}.svg",
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

