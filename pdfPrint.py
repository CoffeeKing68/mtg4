from layers.template import Template
from layers.color import ColorBackgroundLayer, ColorLayer
from layers.color import GradientLayer as GradL
from layers.image import ImageLayer
from layers.image import ResizeImageLayer as ResizeIL
from layers.image import FillImageLayer as FillIL
from layers.image import FitImageLayer as FitIL
from layers.text import PointTextLayer as PTL
from layers.attribute import StringAttribute as SA
from layers.attribute import NumericAttribute as NA
from layers.attribute import AddAttribute as AA
from layers.attribute import MaxAttribute as MA
from layers.attribute import DivideAttribute as DivA
from layers.attribute import MultiplyAttribute as MUA
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from layers.bounds import Bounds
from mtgpy import ManaCost, RulesText

import json
from os.path import join, isfile
import os
from mtgsdk import Card
import math
import time
from datetime import datetime
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
    FLAVOR_SPLIT_COLOR = "RGBA(255, 255, 255, 0.6)"
    FLAVOR_SPLIT_OFFSET = 40

    if os.path.isfile(SETS):
        with open(SETS, "r") as f:
            sets = json.load(f)
    else:
        raise ValueError("sets.json not found.")

    myset = "WAR"
    # JSON = join(RESOURCE_DIR, "card_data", f"{myset}.json")
    # JSON = join(RESOURCE_DIR, "card_data", f"mardu_aristocrats_M20.json")
    # TOKENS = join(RESOURCE_DIR, "card_data", f"tokens.json")
    # ANGELS = join(RESOURCE_DIR, "card_data", f"mardu_angels_M20.json")
    JSON = join(RESOURCE_DIR, "set_data", f"{myset}.json")
    # SULTAI_FLASH = join(RESOURCE_DIR, "card_data", f"sultai_flash.json")

    SAVE_LOCATION = join("test_images", "print_pdfs", myset)
    PDF_SAVE_LOCATION = join("test_images", "pdfs", myset)
    # SAVE_LOCATION = "sultai_flash"

    # JSON = SULTAI_FLASH
    # JSON = TOKENS

    """make directory in art"""
    # if not os.path.isdir(join(RESOURCE_DIR, "art", myset)): # dir does not exist
    #     os.mkdir(join(RESOURCE_DIR, "art", myset))
    """make directory in render dir"""
    if not os.path.isdir(SAVE_LOCATION): # dir does not exist
        os.mkdir(SAVE_LOCATION)
    if not os.path.isdir(PDF_SAVE_LOCATION): # dir does not exist
        os.mkdir(PDF_SAVE_LOCATION)

    """load cards"""
    with open(JSON, "r") as f:
        cards = json.load(f)
    """load tokens"""
    # with open(TOKENS, "r") as f:
    #     tokens = json.load(f)

    SET_DOT_LANG_WIDTH = 5
    INFO_SIZE = 18
    NAME_SIZE = 38
    TYPE_SIZE = 33
    PT_LOYAL_SIZE = 40
    RULES_TEXT_SIZE = 25

    INNER_BORDER = 40
    INNER_RULES_BORDER = 50
    INNER_HEIGHT = 1040
    INNER_WIDTH = 745

    HEIGHT = 1080
    WIDTH = 773

    OUTER_X_BORDER = (WIDTH - INNER_WIDTH) / 2
    TOTAL_Y_BORDER = (HEIGHT - INNER_HEIGHT)
    OUTER_Y_BOTTOM_BORDER = 21
    TOP_OUTER_BORDER = 20
    STANDARD_BORDER = 40
    BORDER = STANDARD_BORDER + OUTER_X_BORDER
    TOP_BORDER = STANDARD_BORDER + TOP_OUTER_BORDER
    BOTTOM_BORDER = STANDARD_BORDER + OUTER_Y_BOTTOM_BORDER
    RULES_BORDER = 50 + OUTER_X_BORDER
    BORDER_PATH = join(RESOURCE_DIR, "Border5.png")

    # 773 x 1080

    B = 29
    MIN_ART_HEIGHT = 850 - B
    # B_ART_WIDTH = WIDTH - 2 * B
    B_ART_WIDTH = WIDTH

    la = AA(MA(SA("language.right"), SA("number.right")), NA(3))
    lmiddle = AA(NA(WIDTH/2),
        DivA(AA(SA("artist_brush.width"), NA(3), SA("artist.width")), NA(2),
            negative=True))

    BOTTOM_BASE_INFO = NA(HEIGHT - 45)
    TOP_BASE_INFO = AA(SA("set.cap"), NA(-3))

    art_layers = {
        "bg": ColorBackgroundLayer("bg", content=Color("#181510")),
        "art": FillIL("art", order=-5, XP50=NA(WIDTH / 2), top=NA(B + TOP_OUTER_BORDER),
            width=NA(B_ART_WIDTH), height=NA(MIN_ART_HEIGHT)),
        "border": ImageLayer("border", content=BORDER_PATH, left=NA(0), top=NA(0))
    }
    no_content_reset = {
        "dot": PTL("dot", RELAY, 25, FC, content=".", left=AA(SA("set.right"),
            NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
        "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
            left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), base=BOTTOM_BASE_INFO),
        "artist_brush": ResizeIL("artist_brush", content=join(RESOURCE_DIR, "artist_brush_white.png"),
            width=NA(20), left=lmiddle, height=SA("set.height"), bottom=BOTTOM_BASE_INFO),
        "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC,
            right=NA(WIDTH-BORDER), bottom=BOTTOM_BASE_INFO),
    }
    layers = {
        "name": PTL("name", BELEREN, NAME_SIZE, FC, left=NA(BORDER), base=NA(70 + TOP_OUTER_BORDER)),
        "type": PTL("type", BELEREN, TYPE_SIZE, FC, left=NA(BORDER), base=AA(SA("rules.top"), NA(-10))),
        "PT": PTL("PT", BELEREN, PT_LOYAL_SIZE, FC, right=NA(WIDTH - BORDER), base=BOTTOM_BASE_INFO),
        "loyalty": PTL("loyalty", BELEREN, PT_LOYAL_SIZE, FC, right=NA(WIDTH - BORDER), base=BOTTOM_BASE_INFO),
        "set": PTL("set", RELAY, INFO_SIZE, FC, left=NA(BORDER), base=BOTTOM_BASE_INFO),

        "number": PTL("number", RELAY, INFO_SIZE, FC, left=NA(BORDER), base=TOP_BASE_INFO),
        "rarity": PTL("rarity", RELAY, INFO_SIZE, FC,
            left=SA("artist_brush.left"), base=TOP_BASE_INFO),
        "artist": PTL("artist", BELEREN_SC, INFO_SIZE, FC, left=AA(SA("artist_brush.right"),
            NA(3)), base=BOTTOM_BASE_INFO),

        "mana_cost": ManaCost("mana_cost", font=BELEREN, font_size=NAME_SIZE, font_color=FC,
            right=NA(WIDTH-BORDER), bottom=AA(SA("name.base"), NA(4))),
        "rules": RulesText("rules", MPLANTIN, MPLANTIN_ITAL, RULES_TEXT_SIZE, FC,
            RULES_TEXT_SIZE - 4, left=NA(RULES_BORDER), right=NA(WIDTH-RULES_BORDER),
            bottom=NA(950 + OUTER_Y_BOTTOM_BORDER)),
    }

    text_template = Template("text_temp", *layers.values(), *no_content_reset.values(),
        left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
    art_template = Template("art_temp", *art_layers.values(), order=-5, left=NA(0), width=NA(WIDTH),
        top=NA(0), height=NA(HEIGHT))

    # name = text_template.get_layer("name")

    # chosing what cards we want to render
    with_art = list(os.listdir(join(RESOURCE_DIR, "art", myset)))
    cards = [c for c in cards if f"{c['name']}_{c['id']}.jpg" in with_art]
    cards = [c for c in cards if c['name'] == "Ahn-Crop Invader"]
    if len(cards) == 0:
        exit("No cards")

    # set some content values
    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} Wizards of the Coast"
    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} WOTC"
    loga = math.ceil(math.log10(len(cards)))
    count = 999

    rarity_colors = {
        "M": "#D15003",
        "R": "#DFBD6C",
        "U": "#C8C8C8",
        "C": FC,
        "L": FC,
        "T": FC,
    }

    if len(cards):
        sset = [s for s in sets if s['code'] == cards[0]['set']]
        if len(sset) == 1:
            count = sset[0]["count"]



    # display purposes
    max_card_length = max(len(c['name']) for c in cards)
    row = f"| {{:0{loga}}}/{{:0{loga}}} | {{}} | {{}} | {{:07.3f}} |"
    total = 0

    pdf = Image(filename=join(RESOURCE_DIR, "PrintPdf.png"))

    for i, card in enumerate(sorted(cards, key=lambda x: x['name'])):
        start_time = time.time()

        temp = Template("template", text_template, art_template,
            left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
        temp.mana_image_format = "svg"
        temp.resource_dir = RESOURCE_DIR

        # remove
        reset_layers = list(layers) + ["art"]
        for name in reset_layers:
            layer = temp.get_layer(name)
            layer.unset_content_and_pre_render()
            if layer.name in card:
                layer.content = card[layer.name]
        temp.get_layer("artist_brush").pre_shadow = None

        # START setting content
        if "Creature" in card["types"]:
            layers["PT"].content = f"{card['power']}/{card['toughness']}"

        number = card['number'].upper().zfill(3)
        layers["number"].content = f"{number}/{count:03}"

        rarity = card["rarity"][0].upper()
        layers["rarity"].color = rarity_colors[rarity]
        layers["rarity"].content = rarity

        rules = ""
        text_to_use = "text"
        if card[text_to_use] is not None:
            rules = card[text_to_use]
        if card["flavor"] is not None:
            flavor = "\n".join([f"<i>{f}</i>" for f in card['flavor'].split('\n')])
            if rules == "":
                rules = flavor
            else:
                rules += "\n" + flavor

        if rules != "":
            temp.get_layer("rules").content = rules
        art_path = join(RESOURCE_DIR, "art", card['set'], f"{card['name']}_{card['id']}.jpg") \
                .replace("//", "__")
        temp.get_layer("art").content = art_path if os.path.isfile(art_path) else None

        temp.update_bounds()
        render_bg = temp.get_layer("art_temp").render()
        image = render_bg.clone()
        if temp.get_layer("art").content is not None:
            render_text_shadow = temp.get_layer("text_temp").shadow(-4, 4, sigma=2,
                radius=4, color="Black")
            image.composite(render_text_shadow, left=0, top=0)
        render_text = temp.get_layer("text_temp").render()
        image.composite(render_text, left=0, top=0)
        # END setting content

        # SAVING content
        image.save(filename=join(SAVE_LOCATION, f"{card['name']}_{card['id']}.jpg").replace("//", "__"))

        p = pdf.clone()
        p.composite(image, left=73, top=67)
        p.save(filename=join(PDF_SAVE_LOCATION, f"{card['name']}_{card['id']}.pdf").replace("//", "__"))
        # END

        # remove
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

