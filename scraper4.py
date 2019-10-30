import os
import json
from shutil import move
from collections import defaultdict
from termcolor import cprint
import urllib.request
import colorama
from datetime import datetime

colorama.init()

SET_DATA_DIR = os.path.join("scraped_data", "images")

def make_duplicates_dir(set_name):
    duplicates_dir = os.path.join(SET_DATA_DIR, set_name, "duplicates")
    if not os.path.isdir(duplicates_dir):
        os.mkdir(duplicates_dir)

def move_duplicate(card):
    make_duplicates_dir(card["set_name"])
    move(os.path.join(SET_DATA_DIR, card["set_name"], f"{card['name']}.{card['format']}"),
        os.path.join(SET_DATA_DIR, card["set_name"], "duplicates", f"{card['name']}_1.{card['format']}"))

def download_image(card, duplicates):
    set_dir = os.path.join(SET_DATA_DIR, card["set_name"])
    if not os.path.isdir(set_dir):
        os.mkdir(set_dir)

    duplicates[card['set_name']][card['name']] += 1
    if duplicates[card['set_name']][card['name']] == 2: # If we have a copy already
        move_duplicate(card)

    if duplicates[card['set_name']][card['name']] > 1: # If we have a copy already
        download_to = os.path.join(SET_DATA_DIR, card['set_name'], "duplicates",
            f"{card['name']}_{duplicates[card['set_name']][card['name']]}.{card['format']}")
    else:
        download_to = os.path.join(SET_DATA_DIR, card['set_name'], f"{card['name']}.{card['format']}")
    tries = 0
    failures = []
    while tries < 3:
        try:
            urllib.request.urlretrieve(card['image_url'], download_to)
            break
        except Exception as e:
            print(e)
            tries +=1
    if tries == 3:
        failures = [card]
    return failures, duplicates

def main():
    try:
        SSETS = [s for s in os.listdir(SET_DATA_DIR) if os.path.isdir(os.path.join(SET_DATA_DIR, s))]
        images = []
        sset_dir = "all"
        with open(os.path.join(SET_DATA_DIR, sset_dir, f"___{sset_dir}.json")) as f:
            sset = json.load(f)

        OFFSET = 24515

        failures = []
        duplicates = defaultdict(lambda: defaultdict(lambda: 0))
        for i, card in enumerate(sset[OFFSET:]):
            if i % 100 == 0:
                pct = 0 if i == 0 else (i - len(failures)) / i * 100
                print(f"{i - len(failures)} sucesses, {len(failures)} failures, {pct:4.2f}%")
            fail, duplicates = download_image(card, duplicates)
            color = "red" if len(fail) == 1 else "green"
            cprint(f"{i:05}: {card['set_name']}@{card['name']}", color)
    except Exception as e:
        cprint(f"There was an exception: {e}")
    finally:
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        INFO_DIR = os.path.join(SET_DATA_DIR, sset_dir, f"info_{time}")
        print(INFO_DIR)
        os.mkdir(INFO_DIR)
        with open(os.path.join(INFO_DIR, "last_image_attempted.txt"), "w") as f:
            f.write(f"i: {i}, OFFSET: {OFFSET}, true: {i + OFFSET}, card: {card}")
        with open(os.path.join(INFO_DIR, "failures.json"), "w") as f:
            json.dump(failures, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
