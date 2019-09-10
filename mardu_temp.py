from mtgsdk import Card
import json
from shutil import copy2 as copy
from shutil import move
import os
from os.path import join
from pickle import dump
from pprint import pprint

# shared = [
#     (4, "Clifftop Retreat"),
#     (4, "Dragonskull Summit"),
#     (4, "Godless Shrine"),
#     (4, "Isolated Chapel"),
#     (4, "Sacred Foundry"),
#     (1, "Swamp"),
#     (4, "Blood Crypt"),
#     (2, "Plains"),
#     (2, "Legion's End"),
#     (1, "Mortify"),
# ]
# extras = [
#     (4, "Gutterbones"),
#     (4, "Dreadhorde Butcher"),
#     (1, "Queen Marchesa"),
#     (4, "Soldier token"),
#     (4, "Spirit token"),
#     (4, "Human token"),
#     (2, "Drill bit")
# ]

# cards = [
#     (4, "Footlight Fiend"),
#     (3, "Grim Initiate"),
#     (3, "Heroic Reinforcements"),
#     (4, "Knight of the Ebon Legion"),
#     (4, "Corpse Knight"),
#     (4, "Cruel Celebrant"),
#     (4, "Fireblade Artist"),
#     (3, "Hero of Precinct One"),
#     (4, "Judith, the Scourge Diva"),
#     (4, "Chandra, Acolyte of Flame"),
#     (2, "Bedevil"),
# ]

# angels = [
#     (1, "Temple of Silence"),
#     (1, "Temple of Triumph"),
#     (4, "Bishop of Wings"),
#     (2, "Tomik, Distinguished Advokist"),
#     (4, "Kaalia, Zenith Seeker"),
#     (1, "Resplendent Angel 1"),
#     (1, "Resplendent Angel 2"),
#     (1, "Resplendent Angel 3"),
#     (1, "Resplendent Angel 4"),
#     (3, "Aurelia, Exemplar of Justice"),
#     (2, "Seraph of the Scales"),
#     (2, "Shalai, Voice of Plenty"),
#     (2, "Lyra Dawnbringer"),
#     (2, "Skarrgan Hellkite"),
#     (1, "Doom Whisperer 1"),
#     (1, "Doom Whisperer 2"),
#     (1, "Demonlord Belzenlok"),
#     (2, "Cast Down"),
#     (2, "Prison Realm"),
#     (2, "Flame Sweep"),
#     (2, "Sorin, Vengeful Bloodlord"),
#     (1, "Duress 1"),
#     (2, "Duress 2"),
#     (3, "Fry"),
#     (2, "Alpine Moon"),
#     (2, "Noxious Grasp"),
#     (1, "Disfigure"),
#     (1, "Sorcerous Spyglass"),
#     (2, "Chandra, Awakened Inferno"),
# ]

# total = 0
# num = 0
# with open("test_images/all_render/Mardu_Printing_angels/print_list.txt", "w") as f:
#     for quant, card in sorted(shared + extras + angels + cards, key=lambda x: x[1]):
#         f.write(f"{quant}x {card}\n")
#         num += 1
#         total += quant
# with open("test_images/all_render/Mardu_Printing_angels/print_list.txt", "r") as f:
#     for l in f.readlines()[:-1]:
#         num += 1
#         total += int(l[0])

# print(total)
# print(num)

ART = join(os.getcwd(), "resources", "art")
with open("resources/card_data/mardu_aristocrats_M20.json") as f:
    cards = json.load(f)
    for i, card in enumerate(cards):
        print(card['name'])
        try:
            move(join(ART, "Mardu", f"{card['name']}_{card['id']}.jpg"),
                 join(ART, card['set'], f"{card['name']}_{card['id']}.jpg"))
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"failed {e.message}")
