from shutil import copy2
from os.path import join, isdir, expanduser
from os import makedirs, listdir
from termcolor import cprint
from json import load, dump, JSONDecodeError

TEST_DIR = "test_images"
PRINTS_DIR = "prints"
LIST = "URB_Alliance"
SAVE_LOCATION = join(TEST_DIR, PRINTS_DIR, LIST)

cards = [
]

decks = {
    "burn": {
        "main": [
            (4, "Eidolon of the Great Revel"),
            (4, "Goblin Guide"),
            (4, "Monastery Swiftspear"),
            (4, "Boros Charm"),
            (4, "Lightning Bolt"),
            (3, "Lightning Helix"),
            (3, "Searing Blaze"),
            (2, "Skullcrack"),
            (4, "Lava Spike"),
            (4, "Rift Bolt"),
            (4, "Skewer the Critics"),
            (3, "Bloodstained Mire"),
            (1, "Fiery Islet"),
            (4, "Inspiring Vantage"),
            (3, "Mountain"),
            (2, "Sacred Foundry"),
            (4, "Sunbaked Canyon"),
            (3, "Wooded Foothills"),
        ],
        "side": [
            (1, "Searing Blaze"),
            (2, "Skullcrack"),
            (1, "Deflecting Palm"),
            (3, "Kor Firewalker"),
            (3, "Path to Exile"),
            (2, "Rest in Peace"),
            (3, "Smash to Smithereens"),
        ],
        "url": "https://mtgdecks.net/Modern/burn-decklist-by-norrathdecay-911437"
    },
    "jund": {
        "main": [
            (4, "Bloodbraid Elf"),
            (2, "Dark Confidant"),
            (2, "Scavenging Ooze"),
            (4, "Tarmogoyf"),
            (1, "Tireless Tracker"),
            (2, "Assassin's Trophy"),
            (2, "Fatal Push"),
            (2, "Kolaghan's Command"),
            (4, "Lightning Bolt"),
            (4, "Inquisition of Kozilek"),
            (2, "Thoughtseize"),
            (4, "Liliana of the Veil"),
            (3, "Wrenn and Six"),
            (1, "Barren Moor"),
            (4, "Blackcleave Cliffs"),
            (1, "Blood Crypt"),
            (2, "Bloodstained Mire"),
            (1, "Forest"),
            (1, "Mountain"),
            (2, "Nurturing Peatland"),
            (2, "Overgrown Tomb"),
            (1, "Raging Ravine"),
            (1, "Stomping Ground"),
            (2, "Swamp"),
            (4, "Verdant Catacombs"),
            (2, "Wooded Foothills"),
        ],
        "side": [
            (1, "Ancient Grudge"),
            (2, "Collective Brutality"),
            (1, "Collector Ouphe"),
            (1, "Damping Sphere"),
            (3, "Fulminator Mage"),
            (1, "Huntmaster of the Fells"),
            (1, "Kitchen Finks"),
            (2, "Leyline of the Void"),
            (1, "Liliana, the Last Hope"),
            (2, "Plague Engineer"),
        ],
        "url": "https://mtgdecks.net/Modern/jund-decklist-by-theaznyoshi-911457"
    },
    "whirza": {
        "main": [
            (4, "Gilded Goose"),
            (4, "Urza, Lord High Artificer"),
            (4, "Arcum's Astrolabe"),
            (1, "Damping Sphere"),
            (1, "Ensnaring Bridge"),
            (1, "Grafdigger's Cage"),
            (4, "Mishra's Bauble"),
            (4, "Mox Opal"),
            (1, "Nihil Spellbomb"),
            (1, "Pithing Needle"),
            (2, "Sword of the Meek"),
            (4, "Thopter Foundry"),
            (2, "Witching Well"),
            (1, "Aether Spellbomb"),
            (3, "Whir of Invention"),
            (4, "Oko, Thief of Crowns"),
            (1, "Breeding Pool"),
            (1, "Flooded Strand"),
            (1, "Inventors' Fair"),
            (4, "Misty Rainforest"),
            (4, "Polluted Delta"),
            (1, "Scalding Tarn"),
            (1, "Snow-Covered Forest"),
            (4, "Snow-Covered Island"),
            (1, "Snow-Covered Swamp"),
            (1, "Watery Grave"),
        ],
        "side": [
            (2, "Assassin's Trophy"),
            (2, "Collective Brutality"),
            (3, "Fatal Push"),
            (1, "Sorcerous Spyglass"),
            (3, "Thoughtseize"),
            (1, "Tormod's Crypt"),
            (1, "Unmoored Ego"),
            (1, "Veil of Summer"),
            (1, "Welding Jar"),
        ],
        "url": "https://mtgdecks.net/Modern/whirza-decklist-by-chris-wulf1991-910578"
    },
    "selesnya_eldrazi": {
        "main": [
            (4, "Eldrazi Displacer"),
            (4, "Noble Hierarch"),
            (4, "Reality Smasher"),
            (4, "Stoneforge Mystic"),
            (4, "Thought-Knot Seer"),
            (4, "Karn, the Great Creator"),
            (2, "Forest"),
            (2, "Plains"),
            (1, "Wastes"),
            (4, "Brushland"),
            (4, "Cavern of Souls"),
            (4, "Eldrazi Temple"),
            (1, "Horizon Canopy"),
            (4, "Prismatic Vista"),
            (1, "Batterskull"),
            (1, "Sword of Feast and Famine"),
            (1, "Sword of Fire and Ice"),
            (3, "Talisman of Unity"),
            (4, "Path to Exile"),
            (4, "Ancient Stirrings"),
        ],
        "side": [
            (1, "Batterskull"),
            (3, "Damping Sphere"),
            (1, "Ensnaring Bridge"),
            (2, "Grafdigger's Cage"),
            (1, "Liquimetal Coating"),
            (1, "Mycosynth Lattice"),
            (1, "Sorcerous Spyglass"),
            (1, "Tormod's Crypt"),
            (1, "Witchbane Orb"),
            (1, "Walking Ballista"),
            (2, "Dismember"),
        ],
        "url": "https://www.youtube.com/watch?v=uVlpOliIe3g"
    },
    "wrenn_and_six": {
        "main": [
            (4, "Arbor Elf"),
            (2, "Hexdrinker"),
            (2, "Scavenging Ooze"),
            (4, "Seasoned Pyromancer"),
            (3, "Tireless Tracker"),
            (3, "Bloodbraid Elf"),
            (2, "Stormbreath Dragon"),
            (4, "Wrenn and Six"),
            (1, "Banefire"),
            (4, "Lightning Bolt"),
            (4, "Utopia Sprawl"),
            (4, "Blood Moon"),
            (3, "Forest"),
            (3, "Forgotten Cave"),
            (1, "Kessig Wolf Run"),
            (2, "Mountain"),
            (4, "Prismatic Vista"),
            (4, "Stomping Ground"),
            (4, "Verdant Catacombs"),
            (2, "Wooded Foothills"),
        ],
        "side": [
            (2, "Ancient Grudge"),
            (3, "Collector Ouphe"),
            (3, "Eidolon of the Great Revel"),
            (2, "Anger of the Gods"),
            (1, "Magus of the Moon"),
            (4, "Leyline of the Void"),
        ],
        "url": "https://www.mtggoldfish.com/articles/instant-deck-tech-wrenn-and-six-gruul-modern"
    },
    "URB_Alliance": {
        "main": [
            (4, "The Royal Scions"),
            (3, "Nicol Bolas, Dragon"),

            (4, "Bonecrusher Giant"),
            (3, "Foulmire Knight"),
            (4, "Irencrag Pyromancer"),
            (2, "Murderous Rider"),
            (2, "Rankle, Master of Pranks"),

            (3, "Bedevil"),
            (4, "Opt"),

            (2, "Golden Egg"),
            (2, "Witching Well"),

            (3, "Improbable Alliance"),

            (4, "Blood Crypt"),
            (1, "Bloodfell Caves"),
            (1, "Castle Vantress"),
            (1, "Dismal Backwater"),
            (4, "Fabled Passage"),

            (1, "Island"),
            (1, "Mountain"),
            (4, "Steam Vents"),
            (3, "Swamp"),
            (4, "Watery Grave"),
        ],
        "side": [
            (2, "Aether Gust"),
            (2, "Cry of the Carnarium"),
            (4, "Disdainful Stroke"),
            (2, "Lava Coil"),
            (2, "Noxious Grasp"),
            (1, "Rankle, Master of Pranks"),
            (2, "Sorcerous Spyglass"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/urx-alliance/"
    },
    "rankle_crats": {
        "main": [
            (4, "Chandra, Acolyte of Flame"),
            (2, "Tibalt, Rakish Instigator"),
            (3, "Bonecrusher Giant"),
            (4, "Cauldron Familiar"),
            (4, "Mayhem Devil"),
            (4, "Priest of Forgotten Gods"),
            (4, "Rankle, Master of Pranks"),
            (4, "Stormfist Crusader"),

            (4, "Claim the Firstborn"),
            (4, "Witch's Oven"),

            (4, "Blood Crypt"),
            (2, "Castle Locthwain"),
            (4, "Fabled Passage"),
            (8, "Mountain"),
            (5, "Swamp"),
        ],
        "side": [
            (2, "Bedevil"),
            (3, "Duress"),
            (2, "Lava Coil"),
            (2, "Noxious Grasp"),
            (2, "Redcap Melee"),
            (3, "Theater of Horrors"),
            (1, "Tibalt, Rakish Instigator"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/ranklecrats/"
    },
    "aggro_knights": {
        "main": [
            (4, "Acclaimed Contender"),
            (4, "Blacklance Paragon"),
            (4, "Fervent Champion"),
            (4, "Inspiring Veteran"),

            (4, "Knight of the Ebon Legion"),
            (4, "Stormfist Crusader"),
            (4, "Venerable Knight"),
            (4, "Weaselback Redcap"),

            (1, "Chance for Glory"),

            (3, "Embercleave"),

            (4, "Blood Crypt"),
            (3, "Fabled Passage"),
            (4, "Godless Shrine"),
            (2, "Mountain"),
            (1, "Plains"),
            (4, "Sacred Foundry"),
            (2, "Swamp"),
            (4, "Tournament Grounds"),
        ],
        "side": [
            (3, "Duress"),
            (3, "Kaya, Orzhov Usurper"),
            (2, "Legion's End"),
            (3, "Mortify"),
            (4, "Worthy Knight"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/aggro-knights/"
    },
    "GB_rock": {
        "main": [
            (4, "Assassin's Trophy"),
            (4, "Blooming Marsh"),
            (3, "Collective Brutality"),
            (4, "Fatal Push"),
            (3, "Field of Ruin"),
            (2, "Forest"),
            (3, "Hexdrinker"),
            (2, "Hissing Quagmire"),
            (3, "Inquisition of Kozilek"),
            (3, "Liliana of the Veil"),
            (1, "Maelstrom Pulse"),
            (2, "Nurturing Peatland"),
            (2, "Overgrown Tomb"),
            (3, "Scavenging Ooze"),
            (4, "Swamp"),
            (4, "Tarmogoyf"),
            (3, "Thoughtseize"),
            (4, "Tireless Tracker"),
            (2, "Treetop Village"),
            (4, "Verdant Catacombs"),
        ],
        "side": [
            (1, "Abrupt Decay"),
            (2, "Damping Sphere"),
            (2, "Duress"),
            (2, "Languish"),
            (4, "Leyline of the Void"),
            (1, "Liliana, the Last Hope"),
            (1, "Nissa, Vital Force"),
            (2, "Surgical Extraction"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/bg-rock/"
    },
    "GDS": {
        "main": [
            (1, "Blood Crypt"),
            (4, "Bloodstained Mire"),
            (4, "Death's Shadow"),
            (2, "Dismember"),
            (4, "Fatal Push"),
            (4, "Gurmag Angler"),
            (2, "Inquisition of Kozilek"),
            (1, "Island"),
            (1, "Kolaghan's Command"),
            (1, "Liliana, the Last Hope"),
            (1, "Mausoleum Secrets"),
            (4, "Polluted Delta"),
            (3, "Scalding Tarn"),
            (2, "Sleight of Hand"),
            (2, "Snapcaster Mage"),
            (2, "Steam Vents"),
            (4, "Street Wraith"),
            (4, "Stubborn Denial"),
            (1, "Swamp"),
            (4, "Thought Scour"),
            (4, "Thoughtseize"),
            (3, "Watery Grave"),
            (2, "The Royal Scions"),
        ],
        "side": [
            (2, "Abrade"),
            (2, "Ceremonious Rejection"),
            (2, "Collective Brutality"),
            (1, "Disdainful Stroke"),
            (1, "Engineered Explosives"),
            (1, "Fulminator Mage"),
            (1, "Grim Lavamancer"),
            (1, "Hurkyl's Recall"),
            (1, "Liliana of the Veil"),
            (2, "Surgical Extraction"),
            (1, "Thief of Sanity"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/grixis-shadow/"
    }
}

art_dir = join("resources", "art")
sset_dir = join("resources", "set_data")
scraped_dir = join(expanduser("~"), "PythonProgramming", "decker", "scraped_data", "images", "all")

def jsonDumpTo(var, path):
    with open(path, "w") as f:
        dump(var, f, indent=4, sort_keys=True)

def jsonLoadFrom(path):
    with open(path, "r") as f:
        v = load(f)
    return v

def doIHave(card_name):
    in_sets = []
    for sset in [s for s in listdir(art_dir) if isdir(join(art_dir, s))]:
        for art in listdir(join(art_dir, sset)):
            if art.startswith(card_name):
                in_sets.append(sset)

    return in_sets

def findScrapedArt(card_name):
    in_sets = []
    for sset in [s for s in listdir(scraped_dir) if isdir(join(scraped_dir, s))]:
        for art in listdir(join(scraped_dir, sset)):
            if art.startswith(card_name):
                in_sets.append(sset)
    return in_sets

def findSets(card_name):
    in_sets = []
    for sset in [s for s in listdir(sset_dir) if s.endswith(".json")]:
        try:
            sss = jsonLoadFrom(join(sset_dir, sset))
    # c["name"] == card_name.name
            if card_name in [s["name"] for s in sss]:
                in_sets.append(sset.rstrip(".json"))
        except JSONDecodeError:
            pass
    return in_sets

class Card():
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __eq__(self, other):
        return type(other.name) == Card and self.name == other.name

    def doIExist(self):
        return doIHave(self.name)

class Deck():
    def __init__(self, main, side=[], url=""):
        self.main = main
        self.side = side
        self.url = url

    def doesMyDeckHaveArt(self, d):
        in_sets = []
        for card in d:
            in_sets.append(card.doIExist())
        return in_sets

    def printDoesMyDeckHaveArt(self, d):
        res = self.doesMyDeckHave(d)
        for card, r in zip(d, res):
            if r:
                cprint(card.name, "green")
            else:
                cprint(card.name, "red")

    @classmethod
    def make(cls, deckName):
        return cls([Card(n, q) for (q, n) in decks[deckName]["main"]],
                [Card(n, q) for (q, n) in decks[deckName]["side"]],
                decks[deckName]["url"])

    @staticmethod
    def quantity(deck):
        return sum([c.quantity for c in deck])

    @property
    def mainQuantity(self):
        return self.quantity(self.main)

    @property
    def sideQuantity(self):
        return self.quantity(self.side)

    def __repr__(self):
        return f"main: {self.mainQuantity}, side: {self.sideQuantity}"

LAND_AMOUNT = 1000
no_print = [
    (3, "Improbable Alliance"),
    (2, "Witching Well"),
    (LAND_AMOUNT, "Island"), (LAND_AMOUNT, "Swamp"),
    (LAND_AMOUNT, "Mountain"), (LAND_AMOUNT, "Plains"),
    (LAND_AMOUNT, "Forest"),
    (4, "Opt"),
    (4, "Disdainful Stroke"),
]
def main():
    # dd = ["burn", "jund", "whirza", "selesnya_eldrazi", "wrenn_and_six",
          # "URB_Alliance", "rankle_crats", "aggro_knights"]
    dd = list(decks.keys())
    ddd = Deck.make(dd[9])
    print(ddd)
    deck = ddd.side
    lacking_art = ddd.doesMyDeckHaveArt(deck)
    for c, r in zip(deck, lacking_art):
        if not r:
            cprint(f"Art not found for {c.name}", "yellow")
            in_sets = findSets(c.name)
            if in_sets:
                cprint(f"{c.name} can be found in {in_sets}", "green")
                scraped_sets = findScrapedArt(c.name)
                if scraped_sets:
                    cprint(f"Found the scraped art work in {scraped_sets}", "green")
                else:
                    cprint(f"Could not find scraped art for {c.name}", "red")
            else:
                cprint(f"Can't find {c.name}", "red")

        else:
            cprint(f"We have the art for {c.name}")
    # ddd.printDoesMyDeckHaveArt(ddd.main)

    # Burn = Deck.make("burn")
    # Jund = Deck.make("jund")
    # print(Jund)
    # print(Burn)

if __name__ == "__main__":
    main()

# for sset, card in cards:
#     s = f"{sset}: {card}"

#     ss = doIHave(card)
#     if (ss):
#         cprint(f"{s}, {ss}", "green")
#     else:
#         cprint(s, "red")

#     src_dir = join(TEST_DIR, "pdfs", sset)
#     if isdir(src_dir):
#         b = False
#         for c in listdir(src_dir):
#             if c.startswith(card): # Found a match
#                 cprint(s, "green")
#                 b = True
#                 break
#         if not b:
#             cprint(s, "red")
#     else:
#         cprint(f"Not a set: {sset}", "red")
