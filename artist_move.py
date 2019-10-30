import os
from mtgsdk import Card
from wand.image import Image
import pickle
from shutil import move
import json
from termcolor import cprint
from wand.compat import nested

ARTIST = "Igor Kieryluk"
RESOURCE_DIR = os.path.join("resources")
ROOT_ART_DIR = os.path.join("/", "Users", "ashleyminshall", "Downloads", "Downloaded Artists")
LANDS = ["Plains", "Island", "Mountain", "Swamp", "Forest"]

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

artists = [d for d in os.listdir(ROOT_ART_DIR) if os.path.isdir(os.path.join(ROOT_ART_DIR, d))]
for ARTIST in artists:
    cprint(ARTIST, 'green')
    ART_DIR = os.path.join(ROOT_ART_DIR, ARTIST)

    cards_pkl = os.path.join(ART_DIR, f"{ARTIST}_cards.pkl")
    if os.path.isfile(cards_pkl):
        with open(cards_pkl, "rb") as f:
            cards = pickle.load(f)
    else:
        print(f"Downloading cards for {ARTIST}")
        cards = Card.where(artist=ARTIST).all()
        with open(cards_pkl, "wb") as f:
            pickle.dump(cards, f)

    for art in os.listdir(ART_DIR):
        if art[0] != "." and not art.endswith(".pkl"):
            name, fmt = art.split(".")
            if name not in LANDS:
                cprint(art, 'yellow')
                try:
                    if fmt != "jpg": # change format
                        Image(filename=os.path.join(ART_DIR, art)).save(filename=os.path.join(ART_DIR, f"{name}.jpg"))
                        try:
                            os.remove(os.path.join(ART_DIR, art))
                        except:
                            cprint(f"Failed to delete {art}.", 'red')

                    if name.endswith("token"): # is a token
                        print("Trying to move token.")
                        safe_move(os.path.join(ART_DIR, art), os.path.join(RESOURCE_DIR, "art", "TOKENS", f"{name}_{ARTIST}.jpg"))
                    elif name.endswith("extra"): # extra
                        print("Tying to move extra")
                        safe_move(os.path.join(ART_DIR, art), os.path.join(RESOURCE_DIR, "art", "extra", f"{name}_{ARTIST}.jpg"))
                    else:
                        matching_art = [c for c in cards if c.name == name]
                        match = matching_art[0]
                        # print(len(matching_art))
                        # Download set if not exists
                        SET_DIR = os.path.join(RESOURCE_DIR, "set_data", f"{match.set}.json")
                        if not os.path.isfile(SET_DIR):
                            print(f"Downloading {match.set}")
                            sset = Card.where(set=match.set).all()
                            sset = [c.__dict__ for c in sset]
                            for i, c in enumerate(sset):
                                sset[i]["name_id"] = f"{c['name']}_{c['id']}"
                            # print(len(sset))
                            with open(SET_DIR, "w") as f:
                                json.dump(sset, f, indent=4, sort_keys=True)

                        # Make art directory
                        SET_ART_DIR = os.path.join(RESOURCE_DIR, "art", match.set)
                        if not os.path.isdir(SET_ART_DIR):
                            os.mkdir(SET_ART_DIR)
                        # print(os.path.join(ART_DIR, f"{name}.jpg"))
                        # print(os.path.join(SET_ART_DIR, f"{match.name}_{match.id}.jpg"))
                        safe_move(os.path.join(ART_DIR, f"{name}.jpg"), os.path.join(SET_ART_DIR, f"{match.name}_{match.id}.jpg"))
                except Exception as e:
                    cprint(f"Failed {e}", 'red')
            else:
                cprint(f"Can't move {art} because it's a land.", 'yellow')

