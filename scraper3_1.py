import urllib.request
import urllib.error
import os
from termcolor import cprint
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from mtgsdk import Set
import re
from tqdm import tqdm

IMAGES_DIR = os.path.join("scraped_data", "images")
if not os.path.isdir(IMAGES_DIR):
    os.mkdir(IMAGES_DIR)

URL = "https://www.mtgpics.com/art?pointeur={}"
CARDS_PER_PAGE = 60

def download_image(art):
    image_url = art["style"][re.search("background: url\(", art["style"]).end():-2].split("/")[-2:]
    id = image_url[-1].split(".")[0]
    image_url = f"https://www.mtgpics.com/pics/art/{'/'.join(image_url)}"
    name = art.div.select_one("div.Card12").a.contents[0].replace("/", "__")
    sset = art.div.select_one("div.Card12").find_all('a')[1].contents[0]
    try:
        artist = art.div.select_one("div.S10").a.contents[0]
    except:
        artist = None
    _, width, _, height = art.div.select_one("div.S10").contents[-1].split(" ")
    width = int(width)
    height = int(height)

    return {
        "name": name,
        "id": id,
        "image_url": image_url,
        "format": image_url.split(".")[-1],
        "artist": artist,
        "width": width,
        "height": height,
        "set_name": sset
    }

def download_page(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "html5lib")
    main = soup.select_one("div#mtgpics_content").div.div.div.div.div
    failures = []
    art_data = []
    for i, art in tqdm(enumerate(main.findChildren("div", recursive=False))):
        tries = 0
        while tries < 3:
            try:
                art_data.append(download_image(art))
                break
            except Exception as e:
                tries += 1
        if tries == 3:
            failures.append(i)
    return art_data, failures

def download_set(cards_per_page):
    download_dir = os.path.join("scraped_data", "images", "all")
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    # number_of_artworks =
    art_data = []
    failures = []
    s = requests.get(URL.format(0)).text
    soup = BeautifulSoup(s, "html5lib")
    MAX_IMAGES = int(soup.select_one("input[name=page][type=text]").find_parent("tr").td.contents[0].split()[0])
    if MAX_IMAGES != 0:
        for i in range(MAX_IMAGES // cards_per_page + 1):
            print(i)
            tries = 0
            while tries < 3:
                try:
                    a, fail = download_page(URL.format(i * cards_per_page))
                    art_data += a
                    failures += fail
                    break
                except Exception as e:
                    tries += 1
                    cprint(f"Exception while downloading set: {e}", "red")
            if tries == 3:
                failures.append(i)
    return art_data, MAX_IMAGES, failures

def main():
    art_data, MAX_IMAGES, failures = download_set(CARDS_PER_PAGE)

    if len(art_data) >= MAX_IMAGES:
        cprint(f"We got all the art ({len(art_data)} >= {MAX_IMAGES})!", "green")
    else:
        cprint(f"We did not get all the art ({len(art_data)} < {MAX_IMAGES})", "red")

    if len(failures) == 0:
        cprint("There were no failures.", "green")
    else:
        cprint(f"There were some failures, {len(failures)}.", "red")

    with open(os.path.join(IMAGES_DIR, "all", f"___all.json"), "w") as f:
        json.dump(art_data, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
