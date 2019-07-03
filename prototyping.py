from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

import time
import threading
from terminaltables import AsciiTable
from elapsed_time import ElapsedTimeThread

import os
cards = os.listdir(os.path.join(os.getcwd(), "resources", "targets", "cards"))

if __name__ == "__main__":
    loga = 3
    max_card_length = max([len(c) for c in cards])
    row = f"| {{:0{loga}}}/{{:0{loga}}} | {{: <{max_card_length}}} | {{:.3f}} |"
    for i, card in enumerate(cards):
        # print(f"Iteration: {i} ", end="", flush=True)
        start = time.time()
        thread = ElapsedTimeThread(i, len(cards) - 1, card, row)
        thread.start()
        # do something
        time.sleep(1)
        # something is finished so stop the thread
        thread.stop()
        thread.join()
        print() # empty print() to output a newline
# WIDTH = 100

# import json
# JSON = "resources/card_data/GRN.json"
# with open(JSON, "r") as f:
#     cards = json.load(f)

# print(len(cards))
# print(len(set(card['name'] for card in cards)))
# print(len(set(card['id'] for card in cards)))

# with open(JSON, "r") as f:
#     cards = json.load(f)

# gap = 50
# i = 0
# for i, card in enumerate(cards[i * gap:(i + 1) * gap]):
#     if card["text"] != card["original_text"]:
#         print(i, card["name"])
#         print(card["text"])
#         print(card["original_text"])


