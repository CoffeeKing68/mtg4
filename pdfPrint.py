#! /Users/ashleyminshall/PythonProgramming/venvs/mtg/bin/python3
from normalLayout import NormalLayout
import math
import time
from termcolor import colored
from argparse import ArgumentParser
import json


def makeCards(cards, deckName):
    loga = math.ceil(math.log10(len(cards)))

    max_card_length = max(len(c['name']) for c in cards)
    row = f"| {{:0{loga}}}/{{:0{loga}}} | {{}} | {{}} | {{:07.3f}} |"
    total = 0

    for i, card in enumerate(cards):
        start_time = time.time()

        temp = NormalLayout(deckName)
        temp.make(card)

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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('filename', help='Name of json file.')
    args = parser.parse_args()
    
    with open(args.filename, "r") as f:
        deck = json.load(f)
        deck = sorted(deck, key=lambda c: c["name"])
        # deck = [c for c in deck if c['flavor_name'] == "Tywin, Warden of the West"]
        # deck = [deck[0]]
        # deck = [c for c in deck if c['name'] == "Dusk // Dawn"]
        makeCards(deck, args.filename.split('/')[-1].split('.')[0])
