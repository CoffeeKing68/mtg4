from template import Template, ColorBackgroundLayer, ColorLayer, ManaCost, RulesText
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA
from attribute import MaxAttribute as MA
from wand.color import Color

import json
from os.path import join, isfile
import os
from mtgsdk import Card

RESOURCE_DIR = join(os.getcwd(), "resources")
JSON = join(RESOURCE_DIR, "card_data", "BFZ.json")
SETS = join(RESOURCE_DIR, "card_data", "sets.json")
TEST_DIR = "test_images"

MPLANTIN = join(RESOURCE_DIR, "fonts", "MPlantin.ttf")
BELEREN_SC = join(RESOURCE_DIR, "fonts", "Beleren_small_caps.ttf")
BELEREN = join(RESOURCE_DIR, "fonts", "Jace_Beleren_bold.ttf")
MPLANTIN_BOLD = join(RESOURCE_DIR, "fonts", "MPlantin_bold.ttf")
MPLANTIN_ITAL = join(RESOURCE_DIR, "fonts", "MPlantin_italic.ttf")
RELAY = BELEREN_SC # TODO change this to Relay Medium

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

# TODO Get Relay Medium font
# TODO left = l, bottom = b, top = t, right = r
# TODO write render_boundary method for template
# TODO Ascender, Descender for text height, etc.
# TODO Get current year
# TODO Shadows for template layers
# TODO ImageLayers (move ColorLayers into new file with Image layers)
# TODO ({0!r}) format()
# TODO composite images over transparent (see boundary template test)
# TODO fit > adjust till image fits within boundary
# TODO fill > adjust so that image leaves no gaps
# TODO strech fill > adjust so that no gaps (ratio not respected)
# TODO test to see if pre_render function is worth the hassle
# TODO remove pre_render probably because some layers' render depend variables other than content
# TODO What I could do is wrap some variables eg. font, color, size (PTL) with decorator that will set layer to dirty
# TODO If layer is dirty at render, re-render else return pre_render if it exists.
# TODO Regex: how to split {3}{B}{B} -> "{3}", "{B}", "{B}"
# TODO Test if svgs are better than png/jpg/bmp
# TODO rebuild Magick with svg delegates
# TODO Implement template variables
# TODO Implement predict / work_out width + height for layers as opposed to pre_render
# TODO If content is None, set pre_render = Image(width=0, height=0)
# TODO OR set bounds to {0, 0}
# TODO

card = [c for c in cards if c["name"] == "Dust Stalker"][0]
BORDER = 45
RULES_BORDER = 50
HEIGHT = 1050
WIDTH = 750
SET_DOT_LANG_WIDTH = 5
INFO_SIZE = 18

layers = {
    "bg": ColorBackgroundLayer("bg", content=Color("Black")),
    "name": PTL("name", BELEREN, 40, FC, left=NA(BORDER), top=NA(BORDER)),
    "type": PTL("type", BELEREN, 40, FC, left=NA(BORDER), bottom=AA(SA("rules.top"), NA(-5))),
    "PT": PTL("PT", BELEREN, 40, FC, right=NA(WIDTH - BORDER), bottom=SA("rarity.bottom")),
    "set": PTL("set", RELAY, INFO_SIZE, FC, left=NA(BORDER), bottom=NA(HEIGHT - BORDER)),
    "dot": PTL("dot", RELAY, 25, FC, content=u"\u2022", left=AA(SA("set.right"),
        NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
    "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
        left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), bottom=NA(HEIGHT - BORDER)),
    "number": PTL("number", RELAY, INFO_SIZE, FC, left=NA(BORDER), bottom=AA(SA("set.top"), NA(-3))),
    "artist_brush": ColorLayer("artist_brush", content="Red", width=NA(20),
        left=AA(MA(SA("language.right"), SA("number.right")), NA(3)), height=SA("set.height"),
        bottom=NA(HEIGHT - BORDER)),
    "rarity": PTL("rarity", RELAY, INFO_SIZE, FC, left=SA("artist_brush.left"),
        bottom=SA("number.bottom")),
    "artist": PTL("artist", RELAY, INFO_SIZE, FC, left=AA(SA("artist_brush.right"), NA(3)),
        bottom=SA("set.bottom")),
    "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC, right=NA(WIDTH-BORDER),
        bottom=SA("set.bottom")),
    "mana_cost": ManaCost("mana_cost", right=NA(WIDTH-BORDER), top=NA(BORDER)),
    "rules": RulesText("rules", MPLANTIN, MPLANTIN_ITAL, 20, FC, 20, left=NA(RULES_BORDER), right=NA(WIDTH-RULES_BORDER),
        bottom=NA(500)),
}

for layer in layers.values():
    if layer.name in card:
        layer.content = card[layer.name]

layers["PT"].content = f"{card['power']}/{card['toughness']}"
count = 999
sset = [s for s in sets if s['code'] == card['set']]
if len(sset) == 1:
    count = sset[0]["count"]
layers["number"].content = f"{card['number']}/{count}"
rarity_colors = {
    "M": "Brick",
    "R": "Yellow",
    "U": "Grey",
    "C": FC
}
rarity = card["rarity"][0].upper()
layers["rarity"].color = rarity_colors[rarity]
layers["rarity"].content = rarity
current_year = 2019
layers["copyright"].content = f"™ & © {current_year} Wizards of the Coast"
layers["rules"].content = card["original_text"]

temp = Template("template", *layers.values(), left=NA(0), width=NA(WIDTH),
    top=NA(0), height=NA(HEIGHT))

temp.update_bounds()
image = temp.render()
image.save(filename=join("test_images", "test_image.bmp"))
