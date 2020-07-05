from layers.template import Template
from layers.mask import Mask
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
from layers.attribute import MinAttribute as MinA
from layers.attribute import DivideAttribute as DivA
from layers.attribute import MultiplyAttribute as MUA
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from layers.bounds import Bounds
from MtgPy import ManaCost, RulesText
from TextReplacer import TextMapper

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

# from templates.adventure import adventure
from subprocess import call


class NormalLayout():
    def __init__(self, deckName):
        self.RESOURCE_DIR = join(os.getcwd(), "resources")

        # self.TEST_DIR = "test_images"

        # FONTS
        self.MPLANTIN = join(self.RESOURCE_DIR, "fonts", "MPlantin.ttf")
        self.BELEREN_SC = join(self.RESOURCE_DIR, "fonts",
                               "Beleren_small_caps.ttf")
        self.BELEREN = join(self.RESOURCE_DIR, "fonts",
                            "Jace_Beleren_bold.ttf")
        self.MPLANTIN_BOLD = join(
            self.RESOURCE_DIR, "fonts", "MPlantin_bold.ttf")
        self.MPLANTIN_ITAL = join(
            self.RESOURCE_DIR, "fonts", "MPlantin_italic.ttf")
        self.RELAY = join(self.RESOURCE_DIR, "fonts", "Relay_medium.ttf")
        self.FC = "White"
        self.FLAVOR_SPLIT_COLOR = "RGBA(255, 255, 255, 0.6)"
        self.SHADOW_COLOR = "#181510"
        self.FLAVOR_SPLIT_OFFSET = 40

        self.SET_DOT_LANG_WIDTH = 5
        self.INFO_SIZE = 18
        self.NAME_SIZE = 38
        self.FLAVOR_NAME_SIZE = 25
        self.TYPE_SIZE = 33
        self.PT_LOYAL_SIZE = 40
        self.RULES_TEXT_SIZE = 25

        self.INNER_BORDER = 40
        self.INNER_RULES_BORDER = 50
        self.INNER_HEIGHT = 1040
        self.INNER_WIDTH = 745

        self.HEIGHT = 1080
        self.WIDTH = 773

        self.SPLIT_CENTER = 460
        self.SPLIT_END = 870
        self.SPLIT_HEIGHT = self.SPLIT_END - self.SPLIT_CENTER
        self.SPLIT_SHADOW_SIZE = 50

        self.OUTER_X_BORDER = (self.WIDTH - self.INNER_WIDTH) / 2
        self.TOTAL_Y_BORDER = (self.HEIGHT - self.INNER_HEIGHT)
        self.OUTER_Y_BOTTOM_BORDER = 21
        self.TOP_OUTER_BORDER = 20
        self.STANDARD_BORDER = 40
        self.BORDER = self.STANDARD_BORDER + self.OUTER_X_BORDER
        self.TOP_BORDER = self.STANDARD_BORDER + self.TOP_OUTER_BORDER
        self.BOTTOM_BORDER = self.STANDARD_BORDER + self.OUTER_Y_BOTTOM_BORDER
        self.RULES_BORDER = 50 + self.OUTER_X_BORDER
        self.BORDER_PATH = join(self.RESOURCE_DIR, "Border5.png")

        self.B = 29
        self.MIN_ART_HEIGHT = 850 - self.B
        self.B_ART_WIDTH = self.WIDTH
        self.rarity_colors = {
            "M": "#D15003",
            "R": "#DFBD6C",
            "U": "#C8C8C8",
            "C": self.FC,
            "L": self.FC,
            "T": self.FC,
        }

        self.la = AA(MA(SA("language.right"), SA("number.right")), NA(3))
        self.lmiddle = AA(NA(self.WIDTH/2),
                          DivA(AA(SA("artist_brush.width"), NA(3), SA("artist.width")), NA(2),
                               negative=True))

        self.BOTTOM_BASE_INFO = NA(self.HEIGHT - 45)
        self.TOP_BASE_INFO = AA(SA("set.cap"), NA(-3))

        self.pdf = Image(filename=join(self.RESOURCE_DIR, "PrintPdf.png"))
        self.text_to_use = "text"
        self.PDF_SAVE_LOCATION = join("test_images", "pdfs", deckName)
        if not os.path.exists(self.PDF_SAVE_LOCATION):
            os.makedirs(self.PDF_SAVE_LOCATION)

    def layers(self, card):
        art_layers = {
            "bg": ColorBackgroundLayer("bg", content=Color(self.SHADOW_COLOR)),
            "art": FillIL("art", order=-5, XP50=NA(self.WIDTH / 2), top=NA(self.B + self.TOP_OUTER_BORDER),
                          width=NA(self.B_ART_WIDTH), height=NA(self.MIN_ART_HEIGHT)),
            "border": ImageLayer("border", content=self.BORDER_PATH, left=NA(0), top=NA(0))
        }
        layers = {
            "dot": PTL("dot", self.RELAY, 25, self.FC, content=".",
                       left=AA(SA("set.right"), NA(self.SET_DOT_LANG_WIDTH)), ycenter=SA("set.ycenter")),
            "language": PTL("language", self.RELAY, self.INFO_SIZE, self.FC, content="EN",
                            left=AA(SA("dot.right"), NA(self.SET_DOT_LANG_WIDTH)), base=self.BOTTOM_BASE_INFO),
            "artist_brush": ResizeIL("artist_brush", content=join(self.RESOURCE_DIR, "artist_brush_white.png"),
                                     width=NA(20), left=self.lmiddle, height=SA("set.height"), bottom=self.BOTTOM_BASE_INFO),
            "copyright": PTL("copyright", self.MPLANTIN, self.INFO_SIZE - 5, self.FC,
                             right=NA(self.WIDTH-self.BORDER), bottom=self.BOTTOM_BASE_INFO),
            "name": PTL("name", self.BELEREN, self.NAME_SIZE, self.FC, left=NA(self.BORDER), base=NA(70 + self.TOP_OUTER_BORDER)),
            "flavor_name": PTL("flavor_name", self.MPLANTIN_ITAL, self.FLAVOR_NAME_SIZE, self.FC, left=SA("name.left"), base=AA(SA("name.base"), NA(self.FLAVOR_NAME_SIZE + 4))),
            "PT": PTL("PT", self.BELEREN, self.PT_LOYAL_SIZE, self.FC, right=NA(self.WIDTH - self.BORDER), base=self.BOTTOM_BASE_INFO),
            "loyalty": PTL("loyalty", self.BELEREN, self.PT_LOYAL_SIZE, self.FC, right=NA(self.WIDTH - self.BORDER), base=self.BOTTOM_BASE_INFO),
            "set": PTL("set", self.RELAY, self.INFO_SIZE, self.FC, left=NA(self.BORDER), base=self.BOTTOM_BASE_INFO),

            "number": PTL("number", self.RELAY, self.INFO_SIZE, self.FC, left=NA(self.BORDER), base=self.TOP_BASE_INFO),
            "rarity": PTL("rarity", self.RELAY, self.INFO_SIZE, self.FC,
                          left=SA("artist_brush.left"), base=self.TOP_BASE_INFO),
            "artist": PTL("artist", self.BELEREN_SC, self.INFO_SIZE, self.FC, left=AA(SA("artist_brush.right"),
                                                                                      NA(3)), base=self.BOTTOM_BASE_INFO),

            "mana_cost": ManaCost("mana_cost", font=self.BELEREN, font_size=self.NAME_SIZE, font_color=self.FC,
                                  right=NA(self.WIDTH-self.BORDER), bottom=AA(SA("name.base"), NA(4))),
        }
        standard_rules = {
            "type": PTL("type", self.BELEREN, self.TYPE_SIZE, self.FC, left=NA(self.BORDER), base=AA(SA("rules.top"), NA(-10))),
            "rules": RulesText("rules", self.MPLANTIN, self.MPLANTIN_ITAL, self.RULES_TEXT_SIZE, self.FC,
                               self.RULES_TEXT_SIZE - 4, left=NA(self.RULES_BORDER), right=NA(self.WIDTH-self.RULES_BORDER),
                               base=AA(SA("rarity.cap"), NA(-6)))
        }
        split_text_layers = {
            "split_name": PTL("split_name", self.BELEREN, self.NAME_SIZE, self.FC, left=SA("name.left"),
                              base=NA(self.SPLIT_CENTER + self.NAME_SIZE)),
            "split_mana_cost": ManaCost("split_mana_cost", font=self.BELEREN, font_size=self.NAME_SIZE, font_color=self.FC,
                                        right=SA("mana_cost.right"), bottom=AA(SA("split_name.base"), NA(4))),
            "split_type": PTL("split_type", self.BELEREN, self.TYPE_SIZE, self.FC, left=SA("type.left"), base=AA(SA("split_rules.top"), NA(-10))),
            "split_rules": RulesText("split_rules", self.MPLANTIN, self.MPLANTIN_ITAL, self.RULES_TEXT_SIZE, self.FC,
                                     self.RULES_TEXT_SIZE - 4, left=SA("rules.left"), right=SA("rules.right"),
                                     base=AA(SA("split_name.cap"), NA(-6)))
        }

        split_kwargs = {"left": NA(0), "order": -5,
                        "width": NA(self.B_ART_WIDTH),
                        "height": NA(self.SPLIT_HEIGHT)}
        top_split_kwargs = {
            **split_kwargs, "YP50": NA((self.B + self.TOP_OUTER_BORDER + self.SPLIT_CENTER) / 2)}
        bottom_split_kwargs = {
            **split_kwargs, "YP50": NA((self.SPLIT_CENTER + self.SPLIT_END - 2) / 2)}

        split_art_layers = {
            "split_divider_top": GradL("split_divider_top", start="RGBA(0,0,0,0.0)", end=self.SHADOW_COLOR,
                                       left=NA(0), width=NA(self.WIDTH), bottom=NA(self.SPLIT_CENTER), height=NA(self.SPLIT_SHADOW_SIZE)),
            "split_divider_bottom": GradL("split_divider_bottom", start=self.SHADOW_COLOR, end="RGBA(0,0,0,0.0)",
                                          left=NA(0), width=NA(self.WIDTH), top=NA(self.SPLIT_CENTER - 1), height=NA(self.SPLIT_SHADOW_SIZE)),
            "split_art_top": Mask("split_art_top_mask", FillIL("split_art_top", **top_split_kwargs), **top_split_kwargs),
            "split_art_bottom": Mask("split_art_bottom_mask", FillIL("split_art_bottom", **bottom_split_kwargs), **bottom_split_kwargs)
        }
        adventure_rules = {
            "rules_box": Template("rules_box", *[
                RulesText("rules", self.MPLANTIN, self.MPLANTIN_ITAL, self.RULES_TEXT_SIZE, self.FC,
                          self.RULES_TEXT_SIZE - 4, left=AA(SA("parent.xcenter"), NA(5)),
                          right=AA(SA("parent.right"), NA(
                              self.RULES_BORDER, negative=True)),
                          ycenter=SA("template.ycenter")),
                Template("adventure_box", *[
                    RulesText("adventure_rules", self.MPLANTIN, self.MPLANTIN_ITAL, self.RULES_TEXT_SIZE, self.FC,
                              self.RULES_TEXT_SIZE - 4, left=NA(0),
                              right=AA(SA("parent.width"), NA(-5)), top=AA(SA("adventure_type.base"), NA(6))),
                    PTL("adventure_type", self.MPLANTIN, self.RULES_TEXT_SIZE + 3, self.FC,
                        left=SA("adventure_name.left"), cap=AA(SA("adventure_name.base"), NA(6))),
                    PTL("adventure_name", self.MPLANTIN, self.RULES_TEXT_SIZE + 5, self.FC,
                        left=NA(0), cap=NA(3)),
                    ManaCost("adventure_mana_cost", font=self.BELEREN, font_size=self.RULES_TEXT_SIZE,
                             font_color=self.FC, right=SA(
                                 "adventure_rules.right"),
                             top=NA(0), mana_size=self.RULES_TEXT_SIZE),
                ], left=NA(self.RULES_BORDER), right=AA(SA("rules.left"), NA(-10)),
                    ycenter=SA("template.ycenter"), height=SA("null.height")),
            ], left=NA(0), width=NA(self.WIDTH),
                base=AA(SA("self.height"), SA("rarity.cap"), NA(-6),
                        MA(SA("rules.bottom"), SA("adventure_box.bottom"), negative=True)),
                height=SA("template.height")
            ),
            "type": PTL("type", self.BELEREN, self.TYPE_SIZE, self.FC, left=NA(self.BORDER),
                        base=AA(SA("rules_box.top"), MinA(SA("adventure_box.top"), SA("rules.top")), NA(-10))),
        }
        if card['layout'] == 'adventure':
            layers = {**layers, **adventure_rules}
        elif card["layout"] == "split":
            layers = {**layers, **standard_rules, **split_text_layers}
            art_layers = {**art_layers, **split_art_layers}
        else:
            layers = {**layers, **standard_rules}

        return list(art_layers.values()), list(layers.values())

    def getRules(self, card):
        rules = ""
        if card[self.text_to_use] is not None:
            rules = card[self.text_to_use]

        if card["flavor"] is not None and card['flavor'] != "":
            replacer = TextMapper()
            flavor = replacer.map(card["flavor"], True).formattedText
            flavor = "\n".join(
                [f"<i>{f}</i>" for f in flavor.splitlines()])
            if rules == "":
                rules = flavor
            else:
                rules += "\n" + flavor
        return rules

    def setFlavorNameHelpText(self, card_name, rules):
        return f"<i>(This card's name is {card_name})</i>\n" + rules

    def make(self, card):
        art_layers, llayers = self.layers(card)
        text_template = Template("text_temp", *llayers,
                                 left=NA(0), width=NA(self.WIDTH), top=NA(0), height=NA(self.HEIGHT))
        art_template = Template("art_temp", *art_layers, order=-5, left=NA(0), width=NA(self.WIDTH),
                                top=NA(0), height=NA(self.HEIGHT))

        temp = Template("template", text_template, art_template,
                        left=NA(0), width=NA(self.WIDTH), top=NA(0), height=NA(self.HEIGHT))

        # generic templating
        temp.mana_image_format = "svg"
        temp.resource_dir = self.RESOURCE_DIR

        # START setting content
        rules = self.getRules(card)

        temp.get_layer("rules").content = rules

        for name in temp.get_layer("text_temp").layers:
            layer = temp.get_layer(name)
            if layer.name in card:
                layer.content = card[layer.name]

        if card['flavor_name'] is not None:
            temp.get_layer('name').content = card['flavor_name']
            temp.get_layer('flavor_name').content = card['name']
            # card['name'], card['flavor_name'] = card['flavor_name'], card['name']

        if card["layout"] == "adventure":
            for cc in card['card_faces']:
                if "power" in cc:
                    creature = cc
                else:
                    adventure_card = cc

            temp.get_layer('name').content = creature['name']
            temp.get_layer('mana_cost').content = creature['mana_cost']
            temp.get_layer('type').content = creature['type_line']

            temp.get_layer(
                "adventure_rules").content = adventure_card['oracle_text']
            temp.get_layer(
                "adventure_type").content = adventure_card["type_line"]
            temp.get_layer("adventure_name").content = adventure_card["name"]
            temp.get_layer(
                "adventure_mana_cost").content = adventure_card["mana_cost"]
        elif card["layout"] == "split":
            temp.get_layer("name").content = card["card_faces"][0]["name"]
            temp.get_layer("type").content = card["card_faces"][0]["type_line"]
            temp.get_layer(
                "mana_cost").content = card["card_faces"][0]["mana_cost"]
            temp.get_layer(
                "rules").content = card["card_faces"][1]["oracle_text"]
            temp.get_layer(
                "split_art_top").content = card["card_faces"][0]["image_location"]
            temp.get_layer(
                "split_art_bottom").content = card["card_faces"][1]["image_location"]
            temp.get_layer(
                "split_name").content = card["card_faces"][1]["name"]
            temp.get_layer(
                "split_mana_cost").content = card["card_faces"][1]["mana_cost"]
            temp.get_layer(
                "split_type").content = card["card_faces"][0]["type_line"]
            temp.get_layer(
                "split_rules").content = card["card_faces"][0]["oracle_text"]

        # generic
        if "Creature" in card["type"]:
            temp.get_layer(
                "PT").content = f"{card['power']}/{card['toughness']}"

        number = card['number'].upper().zfill(3)
        count = int(card['count'])
        temp.get_layer("number").content = f"{number}/{count:03}"

        rarity = card["rarity"][0].upper()
        temp.get_layer("rarity").color = self.rarity_colors[rarity]
        temp.get_layer("rarity").content = rarity

        # RULES CONTENT
        # if rules != "":
        # else:
        #     temp.get_layer('rules').content = card[self.text_to_use]
        art_path = join(self.RESOURCE_DIR, "art", card['set'], f"{card['name']}_{card['id']}.jpg") \
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
        # if temp.get_layer("art").content is not None:
        render_text_shadow = temp.get_layer("text_temp").shadow(-4, 4, sigma=2,
                                                                radius=4, color="Black")
        image.composite(render_text_shadow, left=0, top=0)
        render_text = temp.get_layer("text_temp").render()
        image.composite(render_text, left=0, top=0)
        # END setting content

        # SAVING content
        # image.save(filename=join(SAVE_LOCATION, f"{card['name']}_{card['id']}.jpg").replace("//", "__"))
        # image.save(filename=join(SAVE_LOCATION, f"{card['name']}.jpg").replace("//", "__"))

        p = self.pdf.clone()
        p.composite(image, left=73, top=67)
        p.save(filename=join(self.PDF_SAVE_LOCATION,
                             f"{card['name']}_{card['id']}.pdf").replace("//", "__"))

    # name = text_template.get_layer("name")
