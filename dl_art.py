from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

import time
import threading
from terminaltables import AsciiTable
from elapsed_time import ElapsedTimeThread
from template import Template
from template import ColorBackgroundLayer as CBL
from template import ResizeImageLayer as ResizeIL
from text_layers import PointTextLayer as PTL
from attribute import StringAttribute as SA
from attribute import NumericAttribute as NA
from attribute import AddAttribute as AA

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve, Request, install_opener, build_opener
from os.path import join
import os
import json
import time

if __name__ == "__main__":
    myset = "GRN"
    dl = join(os.getcwd(), "resources", "art", myset)
    with open(join(os.getcwd(), "resources", "card_data", f"{myset}.json"), "r") as f:
        cards = json.load(f)

    art_existing = os.listdir(join(os.getcwd(), "resources", "art", myset))
    art_existing = [a[:-4] for a in art_existing]
    # cards = set([c['name'] for c in cards]) - set(art_existing)
    cards = [c for c in cards if f"{c['name']}_{c['id']}" not in art_existing]

    def d(r):
        return "downloaded" if r else "Not downloaded"

    max_card_length = max((len(c['name']) for c in cards))
    max_result = max((len(r) for r in ("Not downloaded", "downloaded")))

    s = f"| {{: <{max_card_length}}} | {{: <{max_result}}} |"
    for card in cards:
        # try:
        url_name = card['name'].replace("'", "").replace(" ", "-").lower()
        # url_name = "does-not-exist"
        save_dir = join(dl, f"{card['name']}_{card['id']}.jpg")
        URL = f"http://www.artofmtg.com/art/{url_name}/"

        try:
            req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

            response = urlopen(req)
            soup = BeautifulSoup(response, "html.parser")

            image = soup.find("img", {"class": "attachment-full wp-post-image"})
            opener = build_opener()
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            install_opener(opener)
            urlretrieve(image['src'], save_dir)
            print(s.format(card['name'], d(True)))
        except:
            print(s.format(card['name'], d(False)))
        time.sleep(2)
