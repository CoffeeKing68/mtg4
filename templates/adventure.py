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
from layers.attribute import MinAttribute as MinA
from layers.attribute import DivideAttribute as DivA
from layers.attribute import MultiplyAttribute as MUA
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from layers.bounds import Bounds

from os.path import join, expanduser
import sys
sys.path.append("..")
from mtgpy import ManaCost, RulesText
from copy import deepcopy

def env(key):
    env = {
        "SET_DOT_LANG_WIDTH": 5,
        "INFO_SIZE": 18,
        "NAME_SIZE": 38,
        "TYPE_SIZE": 33,
        "PT_LOYAL_SIZE": 40,
        "RULES_TEXT_SIZE": 25,

        "INNER_BORDER": 40,
        "INNER_RULES_BORDER": 50,
        "INNER_HEIGHT": 1040,
        "INNER_WIDTH": 745,

        "HEIGHT": 1080,
        "WIDTH": 773,

        "OUTER_Y_BOTTOM_BORDER": 21,
        "TOP_OUTER_BORDER": 20,
        "STANDARD_BORDER": 40,
        "B": 29,
        "RESOURCE_DIR": join(expanduser("~"), "PythonProgramming", "mtg4", "resources"),

        "DOT_HEIGHT": 25,
    }
    env["MPLANTIN"] = join(env["RESOURCE_DIR"], "fonts", "MPlantin.ttf")
    env["BELEREN_SC"] = join(env["RESOURCE_DIR"], "fonts", "Beleren_small_caps.ttf")
    env["BELEREN"] = join(env["RESOURCE_DIR"], "fonts", "Jace_Beleren_bold.ttf")
    env["MPLANTIN_BOLD"] = join(env["RESOURCE_DIR"], "fonts", "MPlantin_bold.ttf")
    env["MPLANTIN_ITAL"] = join(env["RESOURCE_DIR"], "fonts", "MPlantin_italic.ttf")
    env["RELAY"] = join(env["RESOURCE_DIR"], "fonts", "Relay_medium.ttf")
    env["FC"] = "White"
    env["FLAVOR_SPLIT_COLOR"] = "RGBA(255, 255, 255, 0.6)"
    env["FLAVOR_SPLIT_OFFSET"] = 40

    env["MIN_ART_HEIGHT"] = 850 - env["B"]
    env["B_ART_WIDTH"] = env["WIDTH"]
    env["OUTER_X_BORDER"] = (env["WIDTH"] - env["INNER_WIDTH"]) / 2
    env["TOTAL_Y_BORDER"] = (env["HEIGHT"] - env["INNER_HEIGHT"])
    env["BORDER"] = env["STANDARD_BORDER"] + env["OUTER_X_BORDER"]
    env["TOP_BORDER"] = env["STANDARD_BORDER"] + env["TOP_OUTER_BORDER"]
    env["BOTTOM_BORDER"] = env["STANDARD_BORDER"] + env["OUTER_Y_BOTTOM_BORDER"]
    env["RULES_BORDER"] = 50 + env["OUTER_X_BORDER"]
    env["BORDER_PATH"] = join(env["RESOURCE_DIR"], "Border5.png")

    return env[key]

la = AA(MA(SA("language.right"), SA("number.right")), NA(3))
lmiddle = AA(NA(env("WIDTH")/2),
    DivA(AA(SA("artist_brush.width"), NA(3), SA("artist.width")), NA(2),
        negative=True))

BOTTOM_BASE_INFO = NA(env("HEIGHT") - 45)
TOP_BASE_INFO = AA(SA("set.cap"), NA(-3))

art_layers = {
    "bg": ColorBackgroundLayer("bg", content=Color("#181510")),
    "art": FillIL("art", order=-5, XP50=NA(env("WIDTH") / 2), top=NA(env("B") + env("TOP_OUTER_BORDER")),
        width=NA(env("B_ART_WIDTH")), height=NA(env("MIN_ART_HEIGHT"))),
    "border": ImageLayer("border", content=env("BORDER_PATH"), left=NA(0), top=NA(0))
}
layers = {
    "dot": PTL("dot", env("RELAY"), env("DOT_HEIGHT"), env("FC"), content=".", left=AA(SA("set.right"),
        NA(env("SET_DOT_LANG_WIDTH"))), ycenter=SA("set.ycenter")),
    "language": PTL("language", env("RELAY"), env("INFO_SIZE"), env("FC"), content="EN",
        left=AA(SA("dot.right"), NA(env("SET_DOT_LANG_WIDTH"))), base=BOTTOM_BASE_INFO),
    "artist_brush": ResizeIL("artist_brush", content=join(env("RESOURCE_DIR"), "artist_brush_white.png"),
        width=NA(20), left=lmiddle, height=SA("set.height"), bottom=BOTTOM_BASE_INFO),
    "copyright": PTL("copyright", env("MPLANTIN"), env("INFO_SIZE") - 5, env("FC"),
        right=NA(env("WIDTH") - env("BORDER")), bottom=BOTTOM_BASE_INFO),
    "name": PTL("name", env("BELEREN"), env("NAME_SIZE"), env("FC"), left=NA(env("BORDER")), base=NA(70 + env("TOP_OUTER_BORDER"))),
    "type": PTL("type", env("BELEREN"), env("TYPE_SIZE"), env("FC"), left=NA(env("BORDER")),
        base=AA(SA("rules_box.top"), MinA(SA("adventure_box.top"), SA("rules.top")), NA(-10))),
    #     base=AA(MA(SA("rules.top"), SA("adventure_box.top")), NA(-20), SA("rules_box.top"))),
    "PT": PTL("PT", env("BELEREN"), env("PT_LOYAL_SIZE"), env("FC"), right=NA(env("WIDTH") - env("BORDER")), base=BOTTOM_BASE_INFO),
    "loyalty": PTL("loyalty", env("BELEREN"), env("PT_LOYAL_SIZE"), env("FC"), right=NA(env("WIDTH") - env("BORDER")), base=BOTTOM_BASE_INFO),
    "set": PTL("set", env("RELAY"), env("INFO_SIZE"), env("FC"), left=NA(env("BORDER")), base=BOTTOM_BASE_INFO),

    "number": PTL("number", env("RELAY"), env("INFO_SIZE"), env("FC"), left=NA(env("BORDER")), base=TOP_BASE_INFO),
    "rarity": PTL("rarity", env("RELAY"), env("INFO_SIZE"), env("FC"),
        left=SA("artist_brush.left"), base=TOP_BASE_INFO),
    "artist": PTL("artist", env("BELEREN_SC"), env("INFO_SIZE"), env("FC"), left=AA(SA("artist_brush.right"),
        NA(3)), base=BOTTOM_BASE_INFO),

    "mana_cost": ManaCost("mana_cost", font=env("BELEREN"), font_size=env("NAME_SIZE"),
        font_color=env("FC"), right=NA(env("WIDTH") - env("BORDER")),
        bottom=AA(SA("name.base"), NA(4))),

    "rules_box": Template("rules_box", *[
        RulesText("rules", env("MPLANTIN"), env("MPLANTIN_ITAL"), env("RULES_TEXT_SIZE"), env("FC"),
            env("RULES_TEXT_SIZE") - 4, left=AA(SA("parent.xcenter"), NA(5)),
            right=AA(SA("parent.right"), NA(env("RULES_BORDER"), negative=True)),
            ycenter=SA("template.ycenter")),
        Template("adventure_box", *[
            RulesText("adventure_rules", env("MPLANTIN"), env("MPLANTIN_ITAL"), env("RULES_TEXT_SIZE"), env("FC"),
                env("RULES_TEXT_SIZE") - 4, left=NA(0),
                right=AA(SA("parent.width"), NA(-5)), top=AA(SA("adventure_type.base"), NA(6))),
            PTL("adventure_type", env("MPLANTIN"), env("RULES_TEXT_SIZE") + 3, env("FC"),
                left=SA("adventure_name.left"), cap=AA(SA("adventure_name.base"), NA(6))),
            PTL("adventure_name", env("MPLANTIN"), env("RULES_TEXT_SIZE") + 5, env("FC"),
                left=NA(0), cap=NA(3)),
            ManaCost("adventure_mana_cost", font=env("BELEREN"), font_size=env("RULES_TEXT_SIZE"),
                font_color=env("FC"), right=SA("adventure_rules.right"),
                top=NA(0), mana_size=env("RULES_TEXT_SIZE")),
        ], left=NA(env("RULES_BORDER")), right=AA(SA("rules.left"), NA(-10)),
            ycenter=SA("template.ycenter"), height=SA("null.height")),
        # ColorLayer("test_shape", content="red", left=SA("adventure_box.left"), right=SA("adventure_box.right"),
        #     top=SA("adventure_box.top"), bottom=SA("adventure_box.bottom"), order=-1),
        # ColorLayer("test_shape_2", content="green", left=SA("rules.left"), right=SA("rules.right"),
        #     top=SA("rules.top"), bottom=SA("rules.bottom"), order=-1),
        # ColorLayer("test_shape_2", content="blue", left=SA("parent.left"), right=SA("parent.right"),
        #     top=SA("parent.top"), height=NA(10), order=-1),
        # ColorBackgroundLayer("adventure_bg", content="blue"),
        ], left=NA(0), width=NA(env("WIDTH")),
        # bottom=DivA(AA(SA("self.height"), MA(SA("rules.height"), SA("adventure_box.height"))), NA(2)),
        bottom=AA(SA("self.height"), SA("rarity.cap"), NA(-10),
            MA(SA("rules.bottom"), SA("adventure_box.bottom"), negative=True)),
        height=SA("template.height")
        # height=MA(SA("rules.height"), SA("adventure_box.height"))
    ),
}

def adventure():
    return deepcopy(list(art_layers.values())), deepcopy(list(layers.values()))




