from moveCards import jsonLoadFrom, jsonDumpTo
import os
from os.path import join
from datetime import datetime
from shutil import copy2
from re import compile, sub
from pprint import pprint

ERROR_JSON_PATH = join("print_lists", "errors.json")

def makeErrorJson(path):
    error_cards = []
    with open(path) as f:
        for line in f.read().splitlines():
            p = line.split(os.sep)
            sset = p[-2]
            name, id = p[-1].split("_")
            print(name)
            id = id.split(".")[0]
            print(sset, name, id)
            sset_cards = jsonLoadFrom(join("resources", "set_data", f"{sset}.json"))
            error_card = [c for c in sset_cards if c["id"] == id][0]
            error_cards.append(error_card)
    jsonDumpTo(error_cards, ERROR_JSON_PATH)

def makeCopyofError(now=None):
    if now is None:
        now = datetime.now()
    dest = join("print_lists", f"errors_{now}.json")
    copy2(ERROR_JSON_PATH, dest)
    return dest

text_fields = ["text", "original_text"]
# class Transform():
    def __init__(self, path):
        self.path = path

    def map(self):
        cards = jsonLoadFrom(self.path)
        new_cards = []
        for card in cards:self
            for rep in self.transformations().values():
                for field in rep.fields:
                    if card[field] is not None:
                        card = rep.substitute(card, field)
            new_cards.append(card)
        return new_cards

    def transformations(self):
        LANDS = ["Plains", "Mountain", "Swamp", "Forest", "Island"]
        return {
            "prowess": Rep(r"(Prowess.*)(?<!<i>)(\(Whenever you cast a noncreature spell, this creature gets \+1/\+1 until end of turn.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "suspend": Rep(r"(Suspend.*)(?<!<i>)(\(Rather than cast this card from your hand, you may pay .+ and exile it with a time counter on it. At the beginning of your upkeep, remove a time counter. When the last is removed, cast it without paying its mana cost.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "land_taps": Rep(r"(?<!<i>)(\({T}: Add {.*}\.\))(?<!</i>)", r"<i>\1</i>", text_fields),
            "landfall": Rep(r"(?<!<i>)(Landfall [-|\u2014] )(?<!</i>)(?=If you had a land enter the battlefield under your control this)", "<i>Landfall \u2014 </i>", text_fields),
            "spectacle": Rep(r"(Spectacle.*)(?<!<i>)(\(You may cast this spell for its spectacle cost rather than its mana cost if an opponent lost life this turn.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "escalate": Rep(r"(Escalate\u2014.*)(?<!<i>)(\(Pay this cost for each mode chosen beyond the first.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "revolt": Rep(r"(?<!<i>)(Revolt)(?<!</i>)(.*permanent you controlled left the battlefield this turn\..*)", r"<i>\1</i>\2", text_fields),
            "levels": Rep(r"(Level up.*)(?<!<i>)(\(\{.*\}: Put a level counter on this. Level up only as a sorcery\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "flavor_dash": Rep(r"(?<!\n)(\u2014.+)$", r"\n\1", ["flavor"]),
            "trample_help": Rep(r"([T|t]rample.*)(?<!<i>)(\(It can deal excess combat damage to the player or planeswalker it's attacking\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "delve": Rep(r"([D|d]elve.*)(?<!<i>)(\(Each card you exile from your graveyard while casting this spell pays for \{1\}\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "clue_help": Rep(r"([I|i]nvestigate.*)(?<!<i>)(\(.*colorless Clue artifact token .*with \"\{2\}, Sacrifice this artifact: Draw a card.\"\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "undergrowth": Rep(r"(?<!<i>)(Undergrowth [-|\u2014] )(?<!</i>)(?=.*creature cards+ in your graveyard.*)", "<i>Undergrowth \u2014 </i>", text_fields),
            "scry_help": Rep(r"([S|s]cry \d+.*)(?<!<i>)(\(Look at .* You may .* of your library.*\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "flashback": Rep(r"([F|f]lashback.*)(?<!<i>)(\(You may cast that card from your graveyard for its flashback cost\. Then exile it\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "cycle": Rep(r"([C|c]ycl[e|ing].*)(?<!<i>)(\(.*[D|d]iscard this card: Draw a card\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "ferocius": Rep(r"(?<!<i>)(Ferocious [-|\u2014] )(?<!</i>)(?=.*If you control a creature with power 4 or greater.*)", "<i>Ferocious \u2014 </i>", text_fields),
            "cascade": Rep(r"([C|c]ascade.*)(?<!<i>)(\(When you cast this spell, exile cards from the top .* in a random order\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "monstrous": Rep(r"(Monstrosity .*)(?<!<i>)(\(If this creature isn't monstrous.*and it becomes monstrous\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "planeswalker": PlaneswalkerRep(),
            "phyrexian_mana": Rep(r"(?<!<i>)(\(\{.+\} can be paid with either.+life\.\))(?<!</i>)", r"<i>\1</i>", text_fields),
            "retrace": Rep(r"([R|r]etrace.*)(?<!<i>)(\(You may cast instant and sorcery cards from your graveyard by discarding a land card in addition to paying their other costs\.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "devoid": Rep(r"([D|d]evoid.*)(?<!<i>)(\(This card has no color.\))(?<!</i>)", r"\1<i>\2</i>", text_fields),
            "colorless_mana": Rep(r"(?<!<i>)(\(\{C\} represents colorless mana.\))(?<!</i>)", r"<i>\1</i>", text_fields),
            "landwalk": Rep(r"(walk.*)(?<!<i>)(\(\D+ be blocked as long as defending player controls a\D+\.\))(?<!</i>)", 
                r"\1<i>\2</i>", text_fields),
            "colorless_cards": Rep(r"(?<!<i>)(\((Cards with no colored mana in their mana costs are colorless\D*\.)\))(?<!</i>)",
                r"<i>\1</i>", text_fields),
            "exalted": Rep(r"([E|e]xalted.*)(?<!<i>)(\(Whenever a creature you control attacks alone, that creature gets \+1/\+1 until end of turn\.\))(?<!</i>)",
                r"\1<i>\2</i>", text_fields),
        }

class Rep():
    def __init__(self, search, replace, fields):
        self.search = search
        self.replace = replace
        self.fields = fields

    def substitute(self, card, field):
        card[field] = sub(self.search, self.replace, card[field])
        return card

class PlaneswalkerRep():
    def __init__(self, fields=text_fields):
        self.fields = text_fields

    # "text": "[+1]: Each player discards a card.\n[\u22122]: Target player sacrifices a creature.\n[\u22126]: Separate all permanents target player controls into two piles. That player sacrifices all permanents in the pile of their choice.",
    def substitute(self, card, field):
        if "Planeswalker" in card["types"]:
            card[field] = sub("\u2212", "-", card[field])
            card[field] = sub(r"\[(.*\d+)\]:", r"\1:", card[field])
            return card
        else:
            return card


def main():
        # makeErrorJson(join("print_lists", "errors.txt"))
    new = makeCopyofError("errors_new.json")
    # print(new)
    trans = Transform(new)
    new_cards = trans.map()

    pprint(new_cards[15]["text"])
    jsonDumpTo(new_cards, new)

if __name__ == "__main__":
    main()
