from template import Template, ColorBackgroundLayer
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
# from attribute import AddAttribute as AA
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
RELAY = BELEREN_SC

FC = Color("White")

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

# TODO colors on PTLs aren't working
# TODO Add/Function Attributes
# TODO Get Relay Medium font
# TODO

card = [c for c in cards if c["name"] == "Dust Stalker"][0]

layers = {
    "bg": ColorBackgroundLayer("bg", content=Color("White")),
    "name": PTL("name", BELEREN, 40, FC, left=NA(45), top=NA(45)),
    "type": PTL("type", BELEREN, 40, FC, left=SA("name.left"), top=NA(500)),
    "PT": PTL("PT", BELEREN, 40, FC, right=NA(705), top=NA(700)),
    "set": PTL("set", RELAY, 20, FC, left=SA("name.left"), bottom=NA(1005)),
    # "language": PTL("language", RELAY, 20, FC, left=SA("name.left"), bottom=NA(1005)),
    # "number": PTL("number", RELAY, 25, FC, left=SA("name.left"), bottom=NA(1005)),
    # "number": PTL("number", RELAY, 25, FC, left=SA("name.left"), bottom=NA(1005))
}

for layer in layers.values():
    if layer.name in card:
        layer.content = card[layer.name]

layers["PT"].content = f"{card['power']}/{card['toughness']}"
count = 999
sset = [s for s in sets if s['code'] == card['set']]
if len(sset) == 1:
    count = sset[0]["count"]
# layers["number"].content = f"{card['number']}/{count}"

temp = Template("template", *layers.values(), left=NA(0), width=NA(750), top=NA(0), height=NA(1050))

temp.update_bounds()
image = temp.render()
image.save(filename=join("test_images", "test_image.bmp"))
