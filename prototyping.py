from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

WIDTH = 100

import json
JSON = "resources/card_data/GRN.json"
with open(JSON, "r") as f:
    cards = json.load(f)

print(len(cards))
print(len(set(card['name'] for card in cards)))
print(len(set(card['id'] for card in cards)))



# with open(JSON, "r") as f:
#     cards = json.load(f)

# gap = 50
# i = 0
# for i, card in enumerate(cards[i * gap:(i + 1) * gap]):
#     if card["text"] != card["original_text"]:
#         print(i, card["name"])
#         print(card["text"])
#         print(card["original_text"])


