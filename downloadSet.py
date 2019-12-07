from mtgsdk import Card, Set
import argparse
from termcolor import cprint
from pprint import pprint
from json import load, dump
from os.path import join, isfile

SET_DATA_DIR = join("resources", "set_data")

def jsonDumpTo(var, path):
    with open(path, "w") as f:
        dump(var, f, indent=4, sort_keys=True)

def jsonLoadFrom(path):
    with open(path, "r") as f:
        v = load(f)
    return v

def dlSet(sset):
    cprint(f"Looking for {sset}", "yellow")
    save_to = join(SET_DATA_DIR, f"{sset.upper()}.json")
    if not isfile(save_to):
        cprint(f"Downloading {sset}.")
        cards = Card.where(set=sset).all()
        if len(cards):
            cprint(f"Found {sset}", "green")
            js_cards = []
            for card in cards:
                card.name_id = f"{card.name}_{card.id}"
                js_cards.append(card.__dict__)
            jsonDumpTo(js_cards, save_to)
        else:
            cprint(f"Could not find {sset}", "red")
    else:
        cprint(f"Already have {sset}, skipping", "yellow")

def main():
    parser = argparse.ArgumentParser(description="Download mtg sets easily")
    parser.add_argument("sets", nargs="+",
            help="Name of set to download")

    args = parser.parse_args()

    for sset in args.sets:
        dlSet(sset)

if __name__ == "__main__":
    main()
