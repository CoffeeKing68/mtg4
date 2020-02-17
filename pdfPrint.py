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
from copy import deepcopy
from pprint import pprint

from templates.adventure import adventure
from subprocess import call


def apply_mask(image, mask, invert=False):
    mask.alpha_channel = 'copy'
    image.composite_channel('alpha', mask, 'copy_alpha')


def openInScryfall(card):
    call(["open", "-a", "Google Chrome",
          f"https://scryfall.com/search?q=artist:'{card['artist']}'+set:'{card['set']}'+'{card['name']}'&unique=cards&as=grid&order=name"])


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

    myset = "Modern_Merfolk"
    JSON = "/Users/ashleyminshall/Desktop/test.json"
    # JSON = join(RESOURCE_DIR, "card_data", f"{myset}.json")
    # JSON = join(RESOURCE_DIR, "card_data", f"mardu_aristocrats_M20.json")
    # TOKENS = join(RESOURCE_DIR, "card_data", f"tokens.json")
    # ANGELS = join(RESOURCE_DIR, "card_data", f"mardu_angels_M20.json")
    # JSON = join("print_lists", f"{myset}.json")
    # JSON = join(RESOURCE_DIR, "set_data", f"{myset}.json")

    # SAVE_LOCATION = join("test_images", "print_pdfs", myset)
    SAVE_LOCATION = join("test_images", "print_lists", myset)
    PDF_SAVE_LOCATION = join("test_images", "pdfs", myset)

    # JSON = SULTAI_FLASH
    # JSON = TOKENS

    """make directory in art"""
    # if not os.path.isdir(join(RESOURCE_DIR, "art", myset)): # dir does not exist
    #     os.mkdir(join(RESOURCE_DIR, "art", myset))
    """make directory in render dir"""
    if not os.path.isdir(SAVE_LOCATION):  # dir does not exist
        os.makedirs(SAVE_LOCATION)
    if not os.path.isdir(PDF_SAVE_LOCATION):  # dir does not exist
        os.makedirs(PDF_SAVE_LOCATION)

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
    layers = {
        "dot": PTL("dot", RELAY, 25, FC, content=".", left=AA(SA("set.right"),
                                                              NA(SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
        "language": PTL("language", RELAY, INFO_SIZE, FC, content="EN",
                        left=AA(SA("dot.right"), NA(SET_DOT_LANG_WIDTH)), base=BOTTOM_BASE_INFO),
        "artist_brush": ResizeIL("artist_brush", content=join(RESOURCE_DIR, "artist_brush_white.png"),
                                 width=NA(20), left=lmiddle, height=SA("set.height"), bottom=BOTTOM_BASE_INFO),
        "copyright": PTL("copyright", MPLANTIN, INFO_SIZE - 5, FC,
                         right=NA(WIDTH-BORDER), bottom=BOTTOM_BASE_INFO),
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
                           bottom=AA(SA("rarity.cap"), NA(-10))),
    }
    # name = text_template.get_layer("name")

    # chosing what cards we want to render
    # cards = sorted([c for c in cards if os.path.isdir(join(RESOURCE_DIR, "art", c["set"])) and \
    #         f"{c['name']}_{c['id']}.jpg" in list(os.listdir(join(RESOURCE_DIR, "art", c["set"])))],
    #         key=lambda x: x['name'])
    # cards = [c for c in cards if c['name'] == "Island"]
    if len(cards) == 0:
        exit("No cards")

    # set some content values
    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} Wizards of the Coast"
    # no_content_reset["copyright"].content = f"™ & © {datetime.now().year} WOTC"
    loga = math.ceil(math.log10(len(cards)))

    rarity_colors = {
        "M": "#D15003",
        "R": "#DFBD6C",
        "U": "#C8C8C8",
        "C": FC,
        "L": FC,
        "T": FC,
    }

    text_to_use = "text"

    def getRules(card, ttu):
        rules = ""
        if card[ttu] is not None:
            rules = card[ttu]
        if card["flavor"] is not None:
            flavor = "\n".join(
                [f"<i>{f}</i>" for f in card['flavor'].split('\n')])
            if rules == "":
                rules = flavor
            else:
                rules += "\n" + flavor
        return rules

    def noneToEmptyList(maybeList):
        if maybeList is None:
            return []
        else:
            return maybeList

    # display purposes
    max_card_length = max(len(c['name']) for c in cards)
    row = f"| {{:0{loga}}}/{{:0{loga}}} | {{}} | {{}} | {{:07.3f}} |"
    total = 0

    pdf = Image(filename=join(RESOURCE_DIR, "PrintPdf.png"))

    for i, card in enumerate(cards):
        start_time = time.time()

        # count = 999
        # sset = [s for s in sets if s['code'] == card['set']]
        # if len(sset) == 1:
        #     count = sset[0]["count"]

        # standard layout
        layout = card["layout"]
        if layout == "adventure":
            allayers, llayers = adventure()
        else:
            llayers = deepcopy(list(layers.values()))
            allayers = deepcopy(list(art_layers.values()))

        text_template = Template("text_temp", *llayers,
                                 left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))
        art_template = Template("art_temp", *allayers, order=-5, left=NA(0), width=NA(WIDTH),
                                top=NA(0), height=NA(HEIGHT))

        temp = Template("template", text_template, art_template,
                        left=NA(0), width=NA(WIDTH), top=NA(0), height=NA(HEIGHT))

        # generic templating
        temp.mana_image_format = "svg"
        temp.resource_dir = RESOURCE_DIR

        # START setting content
        for name in temp.get_layer("text_temp").layers:
            layer = temp.get_layer(name)
            if layer.name in card:
                layer.content = card[layer.name]

        if layout == "adventure":
            for cc in card['card_faces']:
                if "power" in cc:
                    creature = cc
                else:
                    adventure_card = cc

            temp.get_layer('name').content = creature['name']
            temp.get_layer('mana_cost').content = creature['mana_cost']
            temp.get_layer('type').content = creature['type_line']
            # RULES CONTENT
            temp.get_layer('rules').content = creature['oracle_text']
            # print(temp.get_layer('rules'))

            # real_card = [c for c in card['card_faces'] if "power" in c]
            # temp.get_layer('name').content = card['ca']
            # with open(join(RESOURCE_DIR, "set_data", f"{card['set'].upper()}.json")) as f:
            #     ccc = json.load(f)
            # adventure_card = [c2 for c2 in ccc if (card['name'] in noneToEmptyList(c2["names"])
            #                                        and (card['name'] != c2['name']))][0]

            temp.get_layer(
                "adventure_rules").content = adventure_card['oracle_text']
            temp.get_layer(
                "adventure_type").content = adventure_card["type_line"]
            temp.get_layer("adventure_name").content = adventure_card["name"]
            temp.get_layer(
                "adventure_mana_cost").content = adventure_card["mana_cost"]

        # generic
        if "Creature" in card["type"]:
            temp.get_layer(
                "PT").content = f"{card['power']}/{card['toughness']}"

        number = card['number'].upper().zfill(3)
        count = int(card['count'])
        temp.get_layer("number").content = f"{number}/{count:03}"

        rarity = card["rarity"][0].upper()
        temp.get_layer("rarity").color = rarity_colors[rarity]
        temp.get_layer("rarity").content = rarity

        rules = getRules(card, text_to_use)

        if rules != "":
            # RULES CONTENT
            temp.get_layer("rules").content = rules
        art_path = join(RESOURCE_DIR, "art", card['set'], f"{card['name']}_{card['id']}.jpg") \
            .replace("//", "__")
        # print(art_path)
        if card['image_location']:
            temp.get_layer("art").content = card['image_location']
        else:
            temp.get_layer("art").content = art_path if os.path.isfile(
                art_path) else None

        # generic
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
        # image.save(filename=join(SAVE_LOCATION, f"{card['name']}_{card['id']}.jpg").replace("//", "__"))
        # image.save(filename=join(SAVE_LOCATION, f"{card['name']}.jpg").replace("//", "__"))

        p = pdf.clone()
        p.composite(image, left=73, top=67)
        p.save(filename=join(PDF_SAVE_LOCATION,
                             f"{card['name']}_{card['id']}.pdf").replace("//", "__"))
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
