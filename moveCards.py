from shutil import copy2
from os.path import join, isdir, expanduser
from os import makedirs, listdir
from termcolor import cprint
from json import load, dump, JSONDecodeError
from pprint import pprint

TEST_DIR = "test_images"
PRINTS_DIR = "prints"
LIST = "URB_Alliance"
SAVE_LOCATION = join(TEST_DIR, PRINTS_DIR, LIST)
LANDS = ["Plains", "Mountain", "Forest", "Island", "Swamp",]

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
            # (1, "Fiery Islet"),
            (4, "Inspiring Vantage"),
            (3, "Mountain"),
            (2, "Sacred Foundry"),
            (4, "Sunbaked Canyon"),
            # (3, "Wooded Foothills"),
            (4, "Arid Mesa"),
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
        "url": "https://www.jeffhoogland.com/decklists/urx-alliance/",
        "modern": False,
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
        "url": "https://www.jeffhoogland.com/decklists/ranklecrats/",
        "modern": False,
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
        "url": "https://www.jeffhoogland.com/decklists/aggro-knights/",
        "modern": False
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
            # (2, "Hissing Quagmire"),
            (3, "Inquisition of Kozilek"),
            (3, "Liliana of the Veil"),
            (1, "Maelstrom Pulse"),
            (2, "Nurturing Peatland"),
            # (2, "Overgrown Tomb"),
            (4, "Overgrown Tomb"),
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
            # (2, "Sleight of Hand"),
            (2, "Serum Visions"),
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
    },
    "death_taxes": {
        "main": [
            (4, "Aether Vial"),
            (4, "Blade Splicer"),
            (2, "Caves of Koilos"),
            (4, "Concealed Courtyard"),
            (4, "Dark Confidant"),
            (4, "Flickerwisp"),
            (4, "Ghost Quarter"),
            (4, "Godless Shrine"),
            (4, "Leonin Arbiter"),
            (4, "Path to Exile"),
            (2, "Plains"),
            (2, "Ravenous Chupacabra"),
            (2, "Shambling Vent"),
            (2, "Smuggler's Copter"),
            (2, "Swamp"),
            (2, "Tectonic Edge"),
            (4, "Thalia, Guardian of Thraben"),
            (2, "Thraben Inspector"),
            (4, "Tidehollow Sculler"),
        ],
        "side": [
            (2, "Disenchant"),
            (2, "Fatal Push"),
            (2, "Gonti, Lord of Luxury"),
            (2, "Kambal, Consul of Allocation"),
            (3, "Rest in Peace"),
            (2, "Sin Collector"),
            (2, "Thoughtseize"),
        ],
        "url": "https://www.mtggoldfish.com/deck/912194#paper",
        "modern": True,
    },
    "UR_tempo": {
        "main": [
            (4, "Brazen Borrower"),
            (4, "Burst Lightning"),
            (4, "Delver of Secrets"),
            (1, "Faerie Conclave"),
            (3, "Fiery Islet"),
            (1, "Flooded Strand"),
            (3, "Island"),
            (4, "Lightning Bolt"),
            (1, "Mana Leak"),
            (2, "Mountain"),
            (2, "Mutavault"),
            (2, "Nimble Obstructionist"),
            (2, "Opt"),
            (3, "Remand"),
            (4, "Scalding Tarn"),
            (4, "Snapcaster Mage"),
            (2, "Spell Pierce"),
            (1, "Spell Snare"),
            (4, "Spirebluff Canal"),
            (3, "Steam Vents"),
            (2, "Vendilion Clique"),
            (4, "Wizard's Lightning"),
        ],
        "side": [
            (2, "Abrade"),
            (2, "Alpine Moon"),
            (2, "Disdainful Stroke"),
            (2, "Dragon's Claw"),
            (1, "Izzet Staticaster"),
            (2, "Magma Spray"),
            (2, "Magmatic Sinkhole"),
            (2, "Negate"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/ur-delver-fae/",
        "modern": True
    },
    "Jeskai_Nahiri": {
        "main": [
            (3, "Anger of the Gods"),
            (3, "Celestial Colonnade"),
            (2, "Cryptic Command"),
            (1, "Emrakul, the Aeons Torn"),
            (1, "Field of Ruin"),
            (4, "Flooded Strand"),
            (2, "Gideon of the Trials"),
            (1, "Glacial Fortress"),
            (2, "Hallowed Fountain"),
            (3, "Island"),
            (4, "Lightning Bolt"),
            (3, "Lightning Helix"),
            (3, "Mana Leak"),
            (1, "Mountain"),
            (4, "Nahiri, the Harbinger"),
            (4, "Path to Exile"),
            (1, "Plains"),
            (1, "Sacred Foundry"),
            (4, "Scalding Tarn"),
            (2, "Search for Azcanta"),
            (4, "Serum Visions"),
            (4, "Snapcaster Mage"),
            (2, "Steam Vents"),
            (1, "Sulfur Falls"),
        ],
        "side": [
            (3, "Damping Sphere"),
            (1, "Disdainful Stroke"),
            (1, "Dispel"),
            (1, "Engineered Explosives"),
            (1, "Izzet Staticaster"),
            (2, "Negate"),
            (2, "Rest in Peace"),
            (1, "Supreme Verdict"),
            (2, "Wear/Tear"),
            (1, "Wrath of God"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/jeskai-nahiri/",
        "modern": True
    },
    "Mardu_pyromancer": {
        "main": [
            (4, "Blackcleave Cliffs"),
            (3, "Blood Crypt"),
            (3, "Blood Moon"),
            (4, "Bloodstained Mire"),
            (3, "Collective Brutality"),
            (2, "Dreadbore"),
            (2, "Fatal Push"),
            (4, "Inquisition of Kozilek"),
            (3, "Kolaghan's Command"),
            (4, "Lightning Bolt"),
            (4, "Lingering Souls"),
            (4, "Marsh Flats"),
            (3, "Mountain"),
            (1, "Plains"),
            (1, "Sacred Foundry"),
            (2, "Swamp"),
            (3, "Thoughtseize"),
            (4, "Young Pyromancer"),
            (4, "Seasoned Pyromancer"),
            (2, "Bedlam Reveler"),
        ],
        "side": [
            (1, "Collective Brutality"),
            (3, "Ensnaring Bridge"),
            (2, "Kambal, Consul of Allocation"),
            (4, "Leyline of the Void"),
            (3, "Molten Rain"),
            (2, "Wear/Tear"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/mardu-pyromancer/",
        "modern": True
    },
    "UB_Fae": {
        "main": [
            (4, "Bitterblossom"),
            (1, "Bloodstained Mire"),
            (2, "Brazen Borrower"),
            (3, "Creeping Tar Pit"),
            (1, "Darkslick Shores"),
            (4, "Drown in the Loch"),
            (3, "Fatal Push"),
            (1, "Flooded Strand"),
            (4, "Inquisition of Kozilek"),
            (4, "Island"),
            (3, "Mistbind Clique"),
            (2, "Murderous Rider"),
            (2, "Mutavault"),
            (4, "Polluted Delta"),
            (4, "Secluded Glen"),
            (2, "Snapcaster Mage"),
            (4, "Spellstutter Sprite"),
            (2, "Swamp"),
            (3, "Thought Scour"),
            (2, "Thoughtseize"),
            (3, "Vendilion Clique"),
            (2, "Watery Grave"),
        ],
        "side": [
            (2, "Ceremonious Rejection"),
            (3, "Collective Brutality"),
            (2, "Damping Sphere"),
            (2, "Disdainful Stroke"),
            (1, "Dismember"),
            (1, "Force of Negation"),
            (2, "Kalitas, Traitor of Ghet"),
            (1, "Murderous Rider"),
            (1, "Negate"),
        ],
        "url": "https://www.jeffhoogland.com/decklists/ub-fae/",
        "modern": True
    },
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

    # def getAllCards(self):
    #     in_sets = findSets(self.name)
    #     cards = []
    #     for sset in in_sets:
    #         json_cards = jsonLoadFrom(join("resources", "set_data", f"{sset}.json"))
    #         cards += [c for c in json_cards if c['name'] == self.name]
    #     return cards

class Deck():
    def __init__(self, main, side=[], url="", modern=True):
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
    def make(cls, main, side=[], url="", modern=True):
        return cls([Card(n, q) for (q, n) in main],
                   [Card(n, q) for (q, n) in side],
                   url, modern)

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

    def layouts(self):
        layouts = []
        for card in self.main + self.side:
            for sset in [s for s in listdir(sset_dir) if s.endswith(".json")]:
                try:
                    cards = [s for s in jsonLoadFrom(join(sset_dir, sset)) if s["name"] == card.name]
                    if len(cards):
                        layouts.append(cards[0]["layout"])
                        break
                except JSONDecodeError:
                    pass
            # cards = jsonLoadFrom(join("resources", "set_data", f"{sset}.json"))
            # c = [cc for cc in cards if cc["name"] == card.name][0]
            # layouts.append(c["layout"])
        return list(set(layouts))

    def saveDeckToJson(self, name):
        in_sets = []
        save_to = join("print_lists")
        card_names = []
        cards = []
        if not isdir(save_to):
            makedirs(save_to)

        for card in [c for c in self.main if c.name not in LANDS]:
            print(card.name)
            in_sets += findSets(card.name)
            card_names.append(card.name)

        for sset in list(set(in_sets)):
            json_cards = jsonLoadFrom(join("resources", "set_data", f"{sset}.json"))
            cards += [c for c in json_cards if c['name'] in card_names]

        jsonDumpTo(cards, join(save_to, f"{name}.json"))
        return cards

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

def viewMissingArt(deckName, verbose=True):
    ddd = Deck.make(decks[deckName]["main"], decks[deckName]["side"],
            decks[deckName]["url"], decks[deckName].get("modern", True))
    deck = ddd.main
    lacking_art = ddd.doesMyDeckHaveArt(deck)
    cards_missing_art = []
    for c, r in zip(deck, lacking_art):
        if verbose:
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
        else:
            if not r:
                cards_missing_art.append(c)

    if not verbose:
        # print(sum([c.quantity for c in cards_missing_art]))
        # pprint([f"{c.name}: {c.quantity}" for c in cards_missing_art])
        return cards_missing_art

def printMissingArt(deckName, verbosity=False):
    missing = viewMissingArt(deckName, verbosity)
    if not verbosity:
        s = f"{deckName}, {sum([c.quantity for c in missing])}"
        if len(missing) == 0:
            cprint(s, "green")
        elif len(missing) < 5:
            cprint(s, "yellow")
        else:
            cprint(s, "red")

def main():
    single = False
    if single:
        i = 8
        deckName = list(decks.keys())[i]
        deckName = "burn"
        print(deckName)
        printMissingArt(deckName, True)
    else:
        from regexSets import Transform
        for deckName in [d for d in decks if decks[d].get("modern", True)]:
            sset_dir = join("print_lists", f"{deckName}.json")
            t = Transform(sset_dir)
            new_cards = t.map()
            jsonDumpTo(new_cards, sset_dir)
            # printMissingArt(deckName, False)
            # print(deckName)
            # ddd = Deck.make(decks[deckName]["main"], decks[deckName]["side"],
            #         decks[deckName]["url"], decks[deckName].get("modern", True))

            # ddd.saveDeckToJson(deckName)


if __name__ == "__main__":
    main()

