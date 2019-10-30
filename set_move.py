import os
from mtgsdk import Card
from wand.image import Image
import pickle
from shutil import move
import json
from termcolor import cprint
from wand.compat import nested

# SSET = "ELD"
LANDS = ["Plains", "Island", "Mountain", "Swamp", "Forest"]
ART_DIR = os.path.join("/", "Users", "ashleyminshall", "Downloads", "Downloaded Sets")
RESOURCE_DIR = os.path.join("resources")

def safe_move(src, dest):
    if os.path.isfile(dest):
        cprint(f"{dest} already exists, not moving.", 'white', 'on_red')
        with nested(Image(filename=src), Image(filename=dest)) as (original, new):
            H = "New" if new.height > original.height else "Original"
            W = "New" if new.width > original.width else "Original"
            print(f"{H} image has > height.")
            print(f"{W} image has > width.")
    else:
        move(src, dest)

sets = [s for s in os.listdir(ART_DIR) if os.path.isdir(os.path.join(ART_DIR, s))]
for SSET in sets:
    cprint(SSET, 'green')
    set_data = os.path.join(RESOURCE_DIR, "set_data", f"{SSET}.json")
    if os.path.isfile(set_data):
        with open(set_data, "r") as f:
            cards = json.load(f)
    else:
        print(f"Downloading cards for {SSET}")
        cards = Card.where(artist=ARTIST).all()
        cards = [c.__dict__ for c in cards]
        for i, c in enumerate(cards):
            cards[i]["name_id"] = f"{c['name']}_{c['id']}"
        with open(set_data, "w") as f:
            json.dump(cards, f, indent=4, sort_key=True)

    for art in os.listdir(os.path.join(ART_DIR, SSET)):
        if art[0] != "." and not art.endswith(".pkl"):
            name, fmt = art.split(".")
            if name not in LANDS:
                cprint(art, 'yellow')
                try:
                    if fmt != "jpg": # change format
                        Image(filename=os.path.join(ART_DIR, SSET, art)).save(filename=os.path.join(ART_DIR, SSET, f"{name}.jpg"))
                        try:
                            os.remove(os.path.join(ART_DIR, SSET, art))
                        except:
                            cprint(f"Failed to delete {art}.", 'red')

                    if name.endswith("token"): # is a token
                        print("Trying to move token.")
                        safe_move(os.path.join(ART_DIR, art),
                            os.path.join(RESOURCE_DIR, "art", "TOKENS", f"{name}_{ARTIST}.jpg"))
                    else:
                        matching_art = [c for c in cards if c["name"] == name]
                        match = matching_art[0]
                        SET_ART_DIR = os.path.join(RESOURCE_DIR, "art", match['set'])
                        if not os.path.isdir(SET_ART_DIR):
                            os.mkdir(SET_ART_DIR)
                        # print(os.path.join(ART_DIR, SSET, f"{name}.jpg"))
                        # print(os.path.join(SET_ART_DIR, f"{match['name']}_{match['id']}.jpg"))
                        safe_move(os.path.join(ART_DIR, SSET, f"{name}.jpg"),
                            os.path.join(SET_ART_DIR, f"{match['name']}_{match['id']}.jpg"))
                except Exception as e:
                    cprint(f"Failed {e}", 'red')
            else:
                cprint(f"Can't move{art} because it's a land.", 'yellow')

