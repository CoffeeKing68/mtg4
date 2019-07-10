from template import Template, ColorBackgroundLayer, ColorLayer, ManaCost, RulesText, ImageLayer
from template import ResizeImageLayer as ResizeIL
from template import FillImageLayer as FillIL
from template import GradientLayer as GradL
# from template import FitImageLayer as FitIL
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

    myset = "GRN"
    JSON = join(RESOURCE_DIR, "card_data", f"{myset}.json")

    """make directory in art"""
    if not os.path.isdir(join(RESOURCE_DIR, "art", myset)): # dir does not exist
        os.mkdir(join(RESOURCE_DIR, "art", myset))
    """make directory in render dir"""
    if not os.path.isdir(join("test_images", "all_render", myset)): # dir does not exist
        os.mkdir(join("test_images", "all_render", myset))
    """download set data"""
    if os.path.isfile(JSON): # load cards if card data exists
        with open(JSON, "r") as f:
            cards = json.load(f)
    else:
        # raise ValueError("No json found.")
        print(f"Downloading cards for {myset}")
        cards = [c.__dict__ for c in Card.where(set=myset).all()]
        with open(JSON, "w") as f:
            json.dump(cards, f, sort_keys=True, indent=4)
    """Add set count to sets.json if it does not exist"""
    if myset not in [s["code"] for s in sets]:
        sets.append({
            "code": myset,
            "count": len(set(card['id'] for card in cards))
        })
        with open(SETS, "w") as f:
            json.dump(sets, f, indent=4)

    """Nice to haves"""
    # TODO adaptive_sharpen for ImageLayers
    # TODO left = l, bottom = b, top = t, right = r
    # TODO Justify rules text (MTG stretches text so that it fits better)
    # TODO Image overlay

    # TODO ImageLayers (move ColorLayers into new file with Image layers)
    # TODO \u0106 does not have a character in BELEREN_SMALL_CAPS
    # TODO
    """The evaluate method on FunctionAttribute does not know when to return
    evaluated_value and when not. A function to clear them (bounds not
    neccessary but can be treated the same for extra efficiency)"""
    # TODO

    """Need to do"""
    # TODO test to see if pre_render function is worth the hassle
    # pre_render is necessary, especially for update_bounds()

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

    # TODO Each Layer.render() method is responsible for deciding whether or
    # not to return pre_render.
    """
    Managing pre_render was challenging with just render(), but now with
    - render_boundary
    - shadow
    - color_overlay
    - and image_overlay and gradient_overlay to come
    it's too difficult. For now, render is called only in render(),
    render-like-methods (overlays etc) and update_bounds().
    """
    """Can't replicate"""
    # TODO Infinite while loop when SA references layer that doesn't exist
    # TODO Template.update_bounds() infinite loop layer.x.is_bounded error
    """ AddAttribute
    Weird behaviour here, with other FunctionAttributes setting ev should
    take place outside of try.except, but not AddAttribute.Pytest passes
    either way, so should write some more tests.
    """
    # TODO possibly better land images
    # https://www.passionmagic.com/illustrations-exclusives-officielles-fournies-par-wizard/
    # TODO Match lands to EXP
    # TODO

    # gap = 20 + 75
    # i = 0
    # cards = cards[:10]
    # cards = [c for c in cards if c["name"] == "Evolving Wilds"]
    # cards = [c for c in cards if c["name"] == "Dust Stalker"]
    # cards = [c for c in cards if c["name"] == "Blighted Gorge"]
    cards = [c for c in cards if c["name"] == "Doom Whisperer"]
    BORDER = 45
    RULES_BORDER = 60
    HEIGHT = 1050
    WIDTH = 750
    SET_DOT_LANG_WIDTH = 5
    INFO_SIZE = 18
    FONT_SIZE = 40
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
        # "shadow3": ColorLayer("shadow3", content="Black", left=NA(0),
        #     width=NA(WIDTH), bottom=NA(HEIGHT), top=SA("art.YP100")),
        # "shadow4": GradL("shadow4", start="Transparent", end="Black", left=NA(0),
        #     width=NA(WIDTH), bottom=SA("art.YP100"), height=NA(200))
    }
    no_content_reset = {
        "dot": PTL("dot", RELAY, 25, FC, content=".", left=AA(SA("set.right"),
            NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
        "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
            left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), bottom=NA(HEIGHT - BORDER)),
        "artist_brush": ResizeIL("artist_brush", content=join(RESOURCE_DIR, "artist_brush_white.png"),
            width=NA(20), left=lmiddle, height=SA("set.height"), bottom=NA(HEIGHT - BORDER)),
        "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC,
            right=NA(WIDTH-BORDER), bottom=SA("set.bottom")),
    }
    layers = {
        "name": PTL("name", BELEREN, FONT_SIZE, FC, left=NA(BORDER), base=NA(BORDER)),
        "type": PTL("type", BELEREN, FONT_SIZE, FC, left=NA(BORDER), bottom=AA(SA("rules.top"), NA(-5))),
        "PT": PTL("PT", BELEREN, FONT_SIZE, FC, right=NA(WIDTH - BORDER), bottom=SA("set.bottom")),
        "loyalty": PTL("loyalty", BELEREN, FONT_SIZE, FC, right=NA(WIDTH - BORDER), bottom=SA("set.bottom")),
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
        # thread = ElapsedTimeThread(i, len(cards) - 1, card['name'], row)
        # thread.start()
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
        number = card['number'].upper().zfill(loga)
        layers["number"].content = f"{number}/{count:0{loga}}"
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
        text_to_use = "text"
        if card[text_to_use] is not None:
            rules = card[text_to_use]
        if card["flavor"] is not None:
            rules += "".join([f"\n<i>{f}</i>" for f in card['flavor'].split('\n')])

        temp.get_layer("rules").content = rules
        art_path = join(RESOURCE_DIR, "art", card["set"], f"{card['name']}_{card['id']}.jpg")
        temp.get_layer("art").content = art_path if os.path.isfile(art_path) else None

        temp.update_bounds()
        # for
        render_bg = temp.get_layer("art_temp").render()
        # render_text_shadow = temp.get_layer("text_temp").shadow(-4, 4, sigma=2,
        #     radius=0, color="Black")
        render_text = temp.get_layer("text_temp").render()
        image = render_bg.clone()

        xb = Bounds(start=BORDER - 10, end=WIDTH - BORDER + 10)
        yb = Bounds(start=temp.get_layer("type")["top"] - 10,
            end=temp.get_layer("rules")['bottom'] + 10)
        exp = render_bg.export_pixels(x=int(xb['start']), y=int(yb['start']),
            width=int(xb['full']), height=int(yb['full']))

        with Image(width=int(xb['full']), height=int(yb['full']),
                background=Color("Transparent")) as blur_image:
            blur_image.import_pixels(width=int(xb['full']), height=int(yb['full']),
               channel_map="RGBA", storage="char", data=exp)
            with Image(width=blur_image.width, height=blur_image.height,
                    background=Color("RGBA(0,0,0,0.2)")) as dark:
                blur_image.composite(dark, 0, 0)
            blur_image.blur(radius=10, sigma=5)
            with Image(width=blur_image.width, height=blur_image.height,
                    background=Color("Black")) as mask:
                with Drawing() as ctx:
                    ctx.fill_color = Color("White")
                    ctx.rectangle(0, 0, width=mask.width,
                            height=mask.height, radius=15)
                    ctx(mask)
                apply_mask(blur_image, mask)
            image.composite(blur_image, left=int(xb['start']), top=int(yb['start']))
        # image.composite(render_text_shadow, left=0, top=0)
        image.composite(render_text, left=0, top=0)
        # image = reduce(lambda x, y: x.composite(y, left=0, top=0),
        #     (render_bg, render_text_shadow, render_text))
        # image = temp.render(fresh=False)
        image.save(filename=join("test_images", "all_render", card['set'], f"{card['name']}_{card['id']}.bmp"))
        temp.unset_bounds_and_attributes()
        # thread.stop()
        # thread.join()

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

