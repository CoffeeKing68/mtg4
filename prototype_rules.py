from mtgpy import Rules, ItalicsText, ManaText, Text
from os.path import join
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
from pprint import pprint

# r = "Hexproof\nDevoid <i>(This creature has no color.)</i>\n{3}, {T}: <i>Add {U}{R} to</i> your mana pool."
r = "Devoid <i>(This card has no color.)</i>\nHaste\nAt the beginning of each end step, if you control no other colorless creatures, return Dust Stalker to its owner's hand."
rules = Rules(r)

RESOURCE_DIR = "resources"
MPLANTIN = join(RESOURCE_DIR, "fonts", "MPlantin.ttf")
MPLANTIN_ITAL = join(RESOURCE_DIR, "fonts", "MPlantin_italic.ttf")
FONT_SIZE = 30
MANA_SIZE = FONT_SIZE
MANA_GAP = 2
PARAGRAPH_GAP = 5
LINE_GAP = FONT_SIZE
WIDTH = 650
WORD_GAP = 6

def get_word_width(word):
    WW = 0
    for i, text in enumerate(word):
        if isinstance(text, ManaText):
            WW += MANA_SIZE
            # not last text item in word and next text is mana
            if i < len(word) - 1 and isinstance(word[i + 1], ManaText):
                WW += MANA_GAP
        else:
            WW += get_text_width(text)
        return WW

def get_text_width(text):
    with Drawing() as draw:
        draw.font = MPLANTIN
        if type(text) != Text: # if italics
            draw.font = MPLANTIN_ITAL
        draw.font_size = FONT_SIZE
        with Image(width=1, height=1) as img:
            return draw.get_font_metrics(img, text.string).text_width

def main():
    r = []
    Y = 0
    for paragraph in rules.paragraphs:
        p = []
        s = []
        X = 0 # New line
        for word in paragraph.words:
            WORD_WIDTH = get_word_width(word)

            if X + WORD_WIDTH + WORD_GAP > WIDTH: # overflow on width
                X = WORD_WIDTH
                Y += LINE_GAP
                p.append(s)
                s = [word]
            else:
                s.append(word)
                X += WORD_WIDTH + WORD_GAP
        p.append(s)
        Y += PARAGRAPH_GAP + LINE_GAP
        r.append(p)

    image = Image(width=int(WIDTH), height=int(Y+FONT_SIZE+100), background=Color("White"))
    CY = FONT_SIZE + 20
    for p in r:
        for s in p:
            CX = 0
            for j, w in enumerate(s):
                if j > 0:
                    CX += WORD_GAP
                for i, text in enumerate(w):
                    if isinstance(text, ManaText):
                        # not last text item in word and next text is mana
                        mana_image = Image(width=MANA_SIZE, height=MANA_SIZE,
                            filename=f"resources/svg/{text.mana_string}.svg",
                            background=Color("Transparent"))
                        image.composite(mana_image, left=CX, top=CY - MANA_SIZE)
                        if i < len(w) - 1 and isinstance(w[i + 1], ManaText):
                            CX += 2
                        CX += MANA_SIZE
                    else:
                        with Drawing() as draw:
                            draw.font = MPLANTIN
                            if type(text) != Text: # if italics
                                draw.font = MPLANTIN_ITAL
                            draw.font_size = FONT_SIZE
                            with Image(width=1, height=1) as img:
                                tw = int(draw.get_font_metrics(img, text.string).text_width)
                            draw.text(CX, CY, text.string)
                            draw(image)
                            CX += tw
            CY += LINE_GAP
        CY += PARAGRAPH_GAP
    image.trim()
    image.save(filename="test_images/rules.png")

# if __name__ == "__main__"
