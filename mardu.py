from template import Template, ColorBackgroundLayer, ColorLayer, ManaCost, RulesText, ImageLayer
from template import ResizeImageLayer as ResizeIL
from template import FillImageLayer as FillIL
from template import GradientLayer as GradL
from template import FitImageLayer as FitIL
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA
from attribute import MaxAttribute as MA
from attribute import DivideAttribute as DivA
from attribute import MultiplyAttribute as MUA
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from bounds import Bounds

import json
from os.path import join, isfile
import os
from mtgsdk import Card
import math
import time
from datetime import datetime
from elapsed_time import ElapsedTimeThread
from termcolor import colored
from functools import reduce
import numpy as np

def apply_mask(image, mask, invert=False):
    mask.alpha_channel = 'copy'
    image.composite_channel('alpha', mask, 'copy_alpha')

def main():
    RESOURCE_DIR = join(os.getcwd(), "resources")
    SETS = join(RESOURCE_DIR, "card_data", "sets.json")
    TEST_DIR = "test_images"

    MPLANTIN = join(RESOURCE_DIR, "fonts", "MPlantin.ttf")
    BELEREN_SC = join(RESOURCE_DIR, "fonts", "Beleren_small_caps.ttf")
    BELEREN = join(RESOURCE_DIR, "fonts", "Jace_Beleren_bold.ttf")
    MPLANTIN_BOLD = join(RESOURCE_DIR, "fonts", "MPlantin_bold.ttf")
    MPLANTIN_ITAL = join(RESOURCE_DIR, "fonts", "MPlantin_italic.ttf")
    RELAY = join(RESOURCE_DIR, "fonts", "Relay_medium.ttf")
    FC = "White"

    if os.path.isfile(SETS):
        with open(SETS, "r") as f:
            sets = json.load(f)
    else:
        raise ValueError("sets.json not found.")

    myset = "mardu"
    JSON = join(RESOURCE_DIR, "card_data", f"{myset}.json")

    """make directory in art"""
    if not os.path.isdir(join(RESOURCE_DIR, "art", myset)): # dir does not exist
        os.mkdir(join(RESOURCE_DIR, "art", myset))
    """make directory in render dir"""
    if not os.path.isdir(join("test_images", "all_render", myset)): # dir does not exist
        os.mkdir(join("test_images", "all_render", myset))

    """load cards"""
    with open(JSON, "r") as f:
        cards = json.load(f)
    # cards = [c for c in cards if c["name"] == "Doom Whisperer"]

    BORDER = 45
    RULES_BORDER = 45
    HEIGHT = 1050
    WIDTH = 754
    SET_DOT_LANG_WIDTH = 5
    INFO_SIZE = 18
    # FONT_SIZE = 40
    NAME_SIZE = 38
    TYPE_SIZE = 33
    PT_LOYAL_SIZE = 40
    RULES_TEXT_SIZE = 25

    la = AA(MA(SA("language.right"), SA("number.right")), NA(3))
    lmiddle = AA(NA(WIDTH/2),
        DivA(AA(SA("artist_brush.width"), NA(3), SA("artist.width")), NA(2),
            negative=True))

    art_layers = {
        "bg": ColorBackgroundLayer("bg", content=Color("Black")),
        "art": FillIL("art", order=-5, XP50=NA(WIDTH / 2), top=NA(0),
            width=NA(WIDTH), height=NA(HEIGHT)),
        "shadow1": GradL("shadow1", start="#0000007F", end="Transparent",
            left=NA(0), width=NA(WIDTH), top=SA("name.bottom"), height=NA(200)),
        "shadow2": ColorLayer("shadow2", content="#0000007F", left=NA(0),
            width=NA(WIDTH), top=NA(0), bottom=SA("shadow1.top")),
        "shadow3": ColorLayer("shadow3", content="RGBA(0,0,0,0.7)", left=NA(0),
            width=NA(WIDTH), bottom=NA(HEIGHT + 1), top=SA("rules.YP30")),
        "shadow4": GradL("shadow4", start="Transparent", end="RGBA(0,0,0,0.7)",
            left=NA(0), width=NA(WIDTH), bottom=SA("shadow3.top"), height=NA(200))
    }
    no_content_reset = {
        "dot": PTL("dot", RELAY, 25, FC, content=".", left=AA(SA("set.right"),
            NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
        "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
            left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), base=NA(HEIGHT - BORDER)),
        "artist_brush": ResizeIL("artist_brush", content=join(RESOURCE_DIR, "artist_brush_white.png"),
            width=NA(20), left=lmiddle, height=SA("set.height"), bottom=NA(HEIGHT - BORDER)),
        "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC,
            right=NA(WIDTH-BORDER), bottom=SA("set.bottom")),
    }
    layers = {
        "name": PTL("name", BELEREN, NAME_SIZE, FC, left=NA(BORDER), base=NA(80)),
        "type": PTL("type", BELEREN, TYPE_SIZE, FC, left=NA(BORDER), base=AA(SA("rules.top"), NA(-10))),
        "PT": PTL("PT", BELEREN, PT_LOYAL_SIZE, FC, right=NA(WIDTH - BORDER), base=SA("set.base")),
        "loyalty": PTL("loyalty", BELEREN, PT_LOYAL_SIZE, FC, right=NA(WIDTH - BORDER), base=SA("set.base")),
        "set": PTL("set", RELAY, INFO_SIZE, FC, left=NA(BORDER), base=NA(HEIGHT - BORDER)),
        "number": PTL("number", RELAY, INFO_SIZE, FC, left=NA(BORDER), base=AA(SA("set.cap"), NA(-3))),
        "rarity": PTL("rarity", RELAY, INFO_SIZE, FC, left=SA("artist_brush.left"),
            base=SA("number.base")),
        "artist": PTL("artist", BELEREN_SC, INFO_SIZE, FC, left=AA(SA("artist_brush.right"),
            NA(3)), base=SA("set.base")),
        "mana_cost": ManaCost("mana_cost", right=NA(WIDTH-BORDER), bottom=AA(SA("name.base"), NA(4))),
        "rules": RulesText("rules", MPLANTIN, MPLANTIN_ITAL, RULES_TEXT_SIZE, FC,
            RULES_TEXT_SIZE - 4, left=NA(RULES_BORDER), right=NA(WIDTH-RULES_BORDER),
            bottom=AA(SA("PT.bottom"), NA(-PT_LOYAL_SIZE), NA(-5))),
    }

    text_template = Template("text_temp", *layers.values(), *no_content_reset.values(),
        left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
    art_template = Template("art_temp", *art_layers.values(), order=-5, left=NA(0), width=NA(WIDTH),
        top=NA(0), height=NA(HEIGHT))

    name = text_template.get_layer("name")

    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} Wizards of the Coast"
    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} WOTC"
    loga = math.ceil(math.log10(len(cards)))
    temp = Template("template", text_template, art_template,
        left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
    temp.mana_image_format = "svg"
    temp.resource_dir = RESOURCE_DIR
    max_card_length = max(len(c['name']) for c in cards)
    row = f"| {{:0{loga}}}/{{:0{loga}}} | {{}} | {{}} | {{:07.3f}} |"
    total = 0

    for i, card in enumerate(cards):
        start_time = time.time()
        # for layer in temp.layers:
        #     layer.unset_content_and_pre_render()

        reset_layers = list(layers) + ["art"]
        for name in reset_layers:
            layer = temp.get_layer(name)
            layer.unset_content_and_pre_render()
            # layer.content = None
            # layer.pre_render = None
            if layer.name in card:
                layer.content = card[layer.name]
        temp.get_layer("artist_brush").pre_shadow = None

        if "Creature" in card["types"]:
            layers["PT"].content = f"{card['power']}/{card['toughness']}"
        count = 999
        sset = [s for s in sets if s['code'] == card['set']]
        if len(sset) == 1:
            count = sset[0]["count"]
        number = card['number'].upper().zfill(math.ceil(math.log10(count)))
        layers["number"].content = f"{number}/{count}"
        rarity_colors = {
            "M": "#D15003",
            "R": "#DFBD6C",
            "U": "#C8C8C8",
            "C": FC,
            "L": FC,
        }
        rarity = card["rarity"][0].upper()
        layers["rarity"].color = rarity_colors[rarity]
        layers["rarity"].content = rarity

        rules = ""
        text_to_use = "original_text"
        if card[text_to_use] is not None:
            rules = card[text_to_use]
        if card["flavor"] is not None:
            rules += "".join([f"\n<i>{f}</i>" for f in card['flavor'].split('\n')])

        temp.get_layer("rules").content = rules
        art_path = join(RESOURCE_DIR, "art", "Mardu", f"{card['name']}_{card['id']}.jpg")
        temp.get_layer("art").content = art_path if os.path.isfile(art_path) else None

        temp.update_bounds()
        render_bg = temp.get_layer("art_temp").render()
        render_text_shadow = temp.get_layer("text_temp").shadow(-4, 4, sigma=2,
            radius=4, color="Black")
        render_text = temp.get_layer("text_temp").render()
        image = render_bg.clone()

        # xb = Bounds(start=BORDER - 10, end=WIDTH - BORDER + 10)
        # yb = Bounds(start=temp.get_layer("type")["top"] - 10,
        #     end=temp.get_layer("rules")['bottom'] + 10)
        # exp = render_bg.export_pixels(x=int(xb['start']), y=int(yb['start']),
        #     width=int(xb['full']), height=int(yb['full']))

        # with Image(width=int(xb['full']), height=int(yb['full']),
        #         background=Color("Transparent")) as blur_image:
        #     blur_image.import_pixels(width=int(xb['full']), height=int(yb['full']),
        #        channel_map="RGBA", storage="char", data=exp)
        #     with Image(width=blur_image.width, height=blur_image.height,
        #             background=Color("RGBA(0,0,0,0.2)")) as dark:
        #         blur_image.composite(dark, 0, 0)
        #     blur_image.blur(radius=10, sigma=5)
        #     with Image(width=blur_image.width, height=blur_image.height,
        #             background=Color("Black")) as mask:
        #         with Drawing() as ctx:
        #             ctx.fill_color = Color("White")
        #             ctx.rectangle(0, 0, width=mask.width,
        #                     height=mask.height, radius=15)
        #             ctx(mask)
        #         apply_mask(blur_image, mask)
        #     image.composite(blur_image, left=int(xb['start']), top=int(yb['start']))

        image.composite(render_text_shadow, left=0, top=0)
        image.composite(render_text, left=0, top=0)

        image.save(filename=join("test_images", "all_render", myset, f"{card['name']}_{card['id']}.bmp"))
        temp.unset_bounds_and_attributes()

        delta = time.time() - start_time
        total += delta
        if delta < .250:
            color = "green"
        elif delta < .500:
            color = "yellow"
        else:
            color = "red"
        print(f"\r{row}".format(i, len(cards) - 1, colored(f"{card['name']: <{max_card_length}}", color),
            colored(f"{delta:03.3f}", color), total))

