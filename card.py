from template import Template, ColorBackgroundLayer, ColorLayer, ManaCost, RulesText
from template import ResizeImageLayer as ResizeIL
from template import FillImageLayer as FillIL
# from template import FitImageLayer as FitIL
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA
from attribute import MaxAttribute as MA
from attribute import DivideAttribute as DA
from attribute import MultiplyAttribute as MUA
from wand.color import Color

import json
from os.path import join, isfile
import os
from mtgsdk import Card
import math
import time
from datetime import datetime

def main():
    RESOURCE_DIR = join(os.getcwd(), "resources")
    JSON = join(RESOURCE_DIR, "card_data", "BFZ.json")
    SETS = join(RESOURCE_DIR, "card_data", "sets.json")
    TEST_DIR = "test_images"

    MPLANTIN = join(RESOURCE_DIR, "fonts", "MPlantin.ttf")
    BELEREN_SC = join(RESOURCE_DIR, "fonts", "Beleren_small_caps.ttf")
    BELEREN = join(RESOURCE_DIR, "fonts", "Jace_Beleren_bold.ttf")
    MPLANTIN_BOLD = join(RESOURCE_DIR, "fonts", "MPlantin_bold.ttf")
    MPLANTIN_ITAL = join(RESOURCE_DIR, "fonts", "MPlantin_italic.ttf")
    # RELAY = BELEREN_SC = join(RESOURCE_DIR, "fonts", "Gotham_book.ttf")
    # RELAY = BELEREN_SC = join(RESOURCE_DIR, "fonts", "Gotham.ttf")
    RELAY = join(RESOURCE_DIR, "fonts", "Relay_medium.ttf")
    FC = "White"

    if os.path.isfile(JSON):
        with open(JSON, "r") as f:
            cards = json.load(f)
    else:
        raise ValueError("No json found.")
        # print("Downloading cards")
        # cards = [c.__dict__ for c in Card.where(name="Doom Whisperer").all()]
        # with open(JSON, "w") as f:
        #     json.dump(cards, f, sort_keys=True, indent=4)
    if os.path.isfile(SETS):
        with open(SETS, "r") as f:
            sets = json.load(f)
    else:
        raise ValueError("sets.json not found.")

    """Nice to haves"""
    # TODO adaptive_sharpen for ImageLayers
    # TODO left = l, bottom = b, top = t, right = r

    # TODO Shadows for template layers
    # TODO ImageLayers (move ColorLayers into new file with Image layers)
    # TODO Change Text to use caption in render_boundary()
    # TODO

    """Need to do"""
    # TODO test to see if pre_render function is worth the hassle

    # TODO remove pre_render probably because some layers' render depend variables other than content
    # TODO What I could do is wrap some variables eg. font, color, size (PTL) with decorator that will set layer to dirty
    # TODO If layer is dirty at render, re-render else return pre_render if it exists.
    # TODO Don't pre_render at content set, call render when updating_bounds
    # TODO render is a means to get width+/height and pre_render was implemented to make the process less expensive
    # TODO pre_render doesn't actually work with TextLayers due to the nature of asc/descender
    # TODO Ascender + Descender option for PointTextLayers
    # TODO layer.dirty_bounds would be necessary for render_shadow + color/gradient/image overlay
    # TODO layer.dirty_bounds and layer.dirty_content
    # TODO How will dirty work with templates + parents

    # TODO Implement predict / work_out width + height for layers as opposed to pre_render

    # TODO Infinite while loop when SA references layer that doesn't exist
    # TODO Template.update_bounds() infinite loop layer.x.is_bounded error

    # TODO Justify rules text
    # TODO Gradient, Image and Color overlay
    # TODO Lands confuse algo, no manacost
    # TODO

    # cards = [c for c in cards if c["name"] == "Deathless Behemoth"]
    cards = [c for c in cards if c["name"] == "Grovetender Druids"]
    BORDER = 45
    RULES_BORDER = 60
    HEIGHT = 1050
    WIDTH = 750
    SET_DOT_LANG_WIDTH = 5
    INFO_SIZE = 18
    FONT_SIZE = 40
    RULES_TEXT_SIZE = 25

    no_content_reset = {
        "bg": ColorBackgroundLayer("bg", content=Color("Black")),
        "dot": PTL("dot", RELAY, 25, FC, content=".", left=AA(SA("set.right"),
            NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
        "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
            left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), bottom=NA(HEIGHT - BORDER)),
        "artist_brush": ResizeIL("artist_brush", content=join(RESOURCE_DIR,
            "artist_brush_white.png"), width=NA(20), left=AA(MA(SA("language.right"),
            SA("number.right")), NA(3)), height=SA("set.height"), bottom=NA(HEIGHT - BORDER)),
        "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC,
            right=NA(WIDTH-BORDER), bottom=SA("set.bottom")),
    }
    layers = {
        "name": PTL("name", BELEREN, FONT_SIZE, FC, left=NA(BORDER), top=NA(BORDER)),
        "type": PTL("type", BELEREN, FONT_SIZE, FC, left=NA(BORDER), bottom=AA(SA("rules.top"), NA(-5))),
        "PT": PTL("PT", BELEREN, FONT_SIZE, FC, right=NA(WIDTH - BORDER), bottom=SA("rarity.bottom")),
        "set": PTL("set", RELAY, INFO_SIZE, FC, left=NA(BORDER), bottom=NA(HEIGHT - BORDER)),
        "number": PTL("number", RELAY, INFO_SIZE, FC, left=NA(BORDER), bottom=AA(SA("set.top"), NA(-3))),
        "rarity": PTL("rarity", RELAY, INFO_SIZE, FC, left=SA("artist_brush.left"),
            bottom=SA("number.bottom")),
        "artist": PTL("artist", BELEREN_SC, INFO_SIZE, FC, left=AA(SA("artist_brush.right"),
            NA(3)), bottom=SA("set.bottom")),
        "mana_cost": ManaCost("mana_cost", right=NA(WIDTH-BORDER), top=NA(BORDER)),
        "rules": RulesText("rules", MPLANTIN, MPLANTIN_ITAL, RULES_TEXT_SIZE, FC,
            RULES_TEXT_SIZE - 4, left=NA(RULES_BORDER), right=NA(WIDTH-RULES_BORDER),
            bottom=AA(SA("PT.bottom"), NA(-FONT_SIZE), NA(-5))),
        "art": FillIL("art", order=-1, XP50=NA(WIDTH / 2), top=NA(0),
            width=NA(WIDTH), height=NA(HEIGHT))
    }

    no_content_reset["copyright"].content = f"™ & © {datetime.now().year} Wizards of the Coast"
    loga = math.ceil(math.log10(len(cards)))
    temp = Template("template", *layers.values(), *no_content_reset.values(),
        left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
    temp.mana_image_format = "svg"
    temp.resource_dir = RESOURCE_DIR
    for i, card in enumerate(cards):
        print(f"{i:0{loga}}/{len(cards):0{loga}} - {card['name']}", end=" ")
        start_time = time.time()
        for layer in layers.values():
            layer.content = None
            if layer.name in card:
                layer.content = card[layer.name]

        if "Creature" in card["types"]:
            layers["PT"].content = f"{card['power']}/{card['toughness']}"
        count = 999
        sset = [s for s in sets if s['code'] == card['set']]
        if len(sset) == 1:
            count = sset[0]["count"]
        layers["number"].content = f"{card['number']}/{count}"
        rarity_colors = {
            "M": "#D15003",
            "R": "#DFBD6C",
            "U": "#C8C8C8",
            "C": FC
        }
        rarity = card["rarity"][0].upper()
        layers["rarity"].color = rarity_colors[rarity]
        layers["rarity"].content = rarity

        rules = ""
        if card["original_text"] is not None:
            rules = card["original_text"]
        if card["flavor"] is not None:
            rules += f"\n<i>{card['flavor']}</i>"

        layers["rules"].content = rules
        art_path = join(RESOURCE_DIR, "art", card["set"], f"{card['name']}.jpg")
        layers["art"].content = art_path if os.path.isfile(art_path) else None

        temp.update_bounds()
        image = temp.render()
        # image.composite(temp.render_boundary())
        image.save(filename=join("test_images", f"{card['name']}.bmp"))
        print(f"{time.time() - start_time:3.3f}")
