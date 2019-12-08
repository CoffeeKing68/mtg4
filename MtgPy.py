import re
from os.path import join

from layers.base_layers import XDefinedLayer, PointLayer

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

class Rules():
    def __init__(self, string):
        self.string = string
        self.paragraphs = []
        for paragraph in string.splitlines():
            self.paragraphs.append(Paragraph(paragraph))

    def __str__(self):
        return "Rules:\n" + "\n".join([f" {i} {p.__str__()}" for i, p in enumerate(self.paragraphs)])

class Paragraph():
    pmana = re.compile("{.+?}")
    pital = re.compile("<i>")
    pitalend = re.compile("<\/i>")

    def __str__(self):
        return "Paragraph:\n" + "\n".join([f"  {i} {w}" for i, w in enumerate(self.words)])

    def __init__(self, string):
        self.string = string

        t = string
        ital = False
        self.words = []
        for t in string.split(" "):
            w = []
            while len(t) > 0:
                mmana = Paragraph.pmana.search(t)
                mital = Paragraph.pital.search(t)
                mitalend = Paragraph.pitalend.search(t)

                matches = sorted([mmana, mital, mitalend], key=lambda m: len(t) + 1 if m is None else m.start())
                match = matches[0]

                if match is None:
                    w.append(ItalicsText(t) if ital else Text(t))
                    t = ""
                else:
                    if match.start() > 0:
                        w.append(ItalicsText(t[:match.start()]) if ital else Text(t[:match.start()]))

                    if match.group()[0] == "{": # Mana
                        w.append(ManaText(t[match.start():match.end()]))
                        t = t[match.end():]
                    elif match.group() == "<i>":
                        match1 = matches[1]
                        if match1 is None:
                            w.append(ItalicsText(t[match.end():]))
                            ital = True
                            t = ""
                        else:
                            w.append(ItalicsText(t[match.end():match1.start()]))
                            if match1.group() == "</i>":
                                t = t[match1.end():]
                            else:
                                t = match1.group() + "<i>" + t[match1.end():]
                    elif match.group() == "</i>":
                        t = t[match.end():]
                        ital = False

            self.words.append([ww for ww in w if ww.string])

class Text():
    def __init__(self, string):
        self.string = string

    def getString(self):
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}: '{self.string}'"

    def __str__(self):
        return f"{self.__class__.__name__}: '{self.string}'"

class ItalicsText(Text):
    pass
    # def __str__(self):
    #     return f"ItalicsText: {self.string}"

class ManaText(Text):
    def __init__(self, string):
        super().__init__(string)
        self.mana_string = string[1:-1].replace("/", "")

    def getManaList(mana_list):
        return [ManaText(m) for m in re.findall("({.+?})", mana_list)]

# if __name__ == "__main__":
#     r = "Hexproof\nDevoid <i>(This creature has no color.)</i>\n{3}, {T}: <i>Add {U}{R} to</i> your mana pool."
#     rules = Rules(r)


class ManaCost(PointLayer):
    def __init__(self, name, *args, mana_size=35, mana_gap=2, font=None,
            font_size=None, font_color=None, **kwargs):
        self.mana_size = mana_size
        self.mana_gap = mana_gap
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        if isinstance(self.font_color, Color):
            self.font_color = Color(self.font_color)
        super().__init__(name, *args, **kwargs)

    def render(self, fresh=False):
        if not fresh and self.pre_render is not None: # if fresh is false and there is a pre_render
            return self.pre_render
        if self.content is not None:
            self.mana = ManaText.getManaList(self.content)
            # width = (len(self.mana) * (self.mana_gap + self.mana_size)) - self.mana_gap
            width = int(len(self.mana) * (self.mana_gap + self.mana_size)) + 100
            height = int(self.mana_size) + 100
            image = Image(width=width, height=height)
            # antialias = False
            # img.antialias = antialias
            offset = 0
            for mana in self.mana:
                if mana.mana_string == "DoubleSlash":
                     with Drawing() as draw:
                        # draw.font = "Arial"
                        # draw.font_size = self.mana_size * 1.4
                        # draw.fill_color = Color("White")
                        draw.font = self.font
                        draw.font_size = self.font_size
                        draw.fill_color = self.font_color
                        with Image(width=1, height=1) as img:
                            tw = int(draw.get_font_metrics(img, "//").text_width)
                        draw.text(offset - 1, self.mana_size, "//")
                        draw(image)
                        offset += tw - 1
                else:
                    msrc = join(self.template.resource_dir, self.template.mana_image_format,
                        f"{mana.mana_string}.{self.template.mana_image_format}")
                    mana_image = Image(width=self.mana_size, height=self.mana_size,
                        background=Color("Transparent"), filename=msrc, resolution=300)
                    image.composite(mana_image, left=offset, top=0)
                    offset += self.mana_size + self.mana_gap
            image.trim()
            self.pre_render = image
            return image
        else:
            raise NotReadyToRenderError(f"{self.name} is not ready to render right now.")

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
        self.bottom_base = CY
        image.trim()
        self.pre_render = image
        return image

    def __getitem__(self, key):
        if key == "bottom_base":
            pass
        else:
            return super().__getitem__(key)

# if __name__ == "__main__":
#     s = '<i>({B/P} can be paid with either {B} or 2 life.)</i>\nTarget creature gets -5/-5 until end of turn.\n<i>"You serve Phyrexia. Your pieces would better serve Phyrexia elsewhere."</i>\n<i>—Azax-Azog, the Demon Thane</i>'
#     r = Rules(s)
#     print(r)
