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

with open("scraped_data/set_data/sets.json") as f:
    sets = json.load(f)

IMAGES_DIR = os.path.join("scraped_data", "images")
if not os.path.isdir(IMAGES_DIR):
    os.mkdir(IMAGES_DIR)

NEW_SETS = os.path.join("scraped_data", "set_data", "new_set_data.json")
if not os.path.isfile(NEW_SETS):
    MTG_SDK_SET_DATA = os.path.join("scraped_data", "set_data", "mtg_sdk_set_data.json")
    if not os.path.isfile(MTG_SDK_SET_DATA):
        print("Downloading sets.")
        mtg_sdk_sets = [s.__dict__ for s in Set.all()]
        with open(MTG_SDK_SET_DATA, "w") as f:
            json.dump(mtg_sdk_sets, f, indent=4, sort_keys=True)
    else:
        with open(MTG_SDK_SET_DATA) as f:
            mtg_sdk_sets = json.load(f)

    new_sets = []
    for i, sset in enumerate(sets):
        try:
            mtg_sdk_set = [s for s in mtg_sdk_sets if s['name'] == sset['name']][0]
            sset = {**mtg_sdk_set, **sset}
            cprint(f"{i}: {sset['name']} succeeded", "green")
        except:
            cprint(f"{i}: {sset['name']} failed.", "red")
        new_sets.append(sset)

    with open(NEW_SETS, "w") as f:
        json.dump(new_sets, f, indent=4, sort_keys=True)
else:
    with open(NEW_SETS) as f:
        new_sets = json.load(f)

new_sets = sorted(new_sets, key=lambda s: datetime.strptime(s["release_date"], "%B %d, %Y"))

new_sets = [new_sets[209], new_sets[201]]
# i = 0
# PER_PAGE = 5
# new_sets = new_sets[i * PER_PAGE:(i + 1) * PER_PAGE]

URL = "https://www.mtgpics.com/art?set={}&pointeur={}"
CARDS_PER_PAGE = 60

def download_image(sset, art):
    image_url = art["style"][re.search("background: url\(", art["style"]).end():-2].split("/")[-2:]
    id = image_url[-1].split(".")[0]
    image_url = f"https://www.mtgpics.com/pics/art/{'/'.join(image_url)}"
    name = art.div.select_one("div.Card12").a.contents[0]
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
        "artist": artist,
        "width": width,
        "height": height,
        "set_name": sset["name"]
    }

def download_page(sset, url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "html5lib")
    main = soup.select_one("div#mtgpics_content").div.div.div.div.div
    failures = []
    art_data = []
    for i, art in tqdm(enumerate(main.findChildren("div", recursive=False))):
        tries = 0
        while tries < 3:
            try:
                art_data.append(download_image(sset, art))
                break
            except Exception as e:
                tries += 1
        if tries == 3:
            failures.append(i)
    return art_data, failures

def download_set(sset, cards_per_page):
    download_dir = os.path.join("scraped_data", "images", sset['name'])
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    # number_of_artworks =
    art_data = []
    failures = []
    s = requests.get(URL.format(sset['id'], 0)).text
    soup = BeautifulSoup(s, "html5lib")
    MAX_IMAGES = int(soup.select_one("input[name=page][type=text]").find_parent("tr").td.contents[0].split()[0])
    if MAX_IMAGES != 0:
        for i in range(MAX_IMAGES // cards_per_page + 1):
            tries = 0
            while tries < 3:
                try:
                    a, fail = download_page(sset, URL.format(sset['id'], i * cards_per_page))
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
    for i, new_set in enumerate(new_sets):
        print(f"{i}: {new_set['name']}")
        art_data, MAX_IMAGES, failures = download_set(new_set, CARDS_PER_PAGE)

        if len(art_data) >= MAX_IMAGES:
            cprint(f"We got all the art for {new_set['name']} ({len(art_data)} >= {MAX_IMAGES})!", "green")
        else:
            cprint(f"We did not get all the art for {new_set['name']} ({len(art_data)} < {MAX_IMAGES})", "red")

        if len(failures) == 0:
            cprint("There were no failures.", "green")
        else:
            cprint(f"There were some failures, {len(failures)}.", "red")

        with open(os.path.join(IMAGES_DIR, new_set['name'], f"___{new_set['name']}.json"), "w") as f:
            json.dump(art_data, f, indent=4, sort_keys=True)

    # download_dir = os.path.join("scraped_data", "images", new_set['name'])
    # if not os.path.isdir(download_dir):
    #     os.mkdir(download_dir)
    # art_data = []
    # s = requests.get(URL.format(new_set['id'], 0)).text
    # soup = BeautifulSoup(s, "html5lib")
    # MAX_IMAGES = int(soup.select_one("input[name=page][type=text]").find_parent("tr").td.contents[0].split()[0])
#     if MAX_IMAGES != 0:
#         for i in range(MAX_IMAGES // CARDS_PER_PAGE + 1):
#             source = requests.get(URL.format(new_set['id'], i * CARDS_PER_PAGE)).text
#             soup = BeautifulSoup(source, "html5lib")

#             main = soup.select_one("div#mtgpics_content").div.div.div.div.div

#             for art in main.findChildren("div", recursive=False):
#                 try:
#                     image_url = art["style"][re.search("background: url\(", art["style"]).end():-2].split("/")[-2:]
#                     id = image_url[-1].split(".")[0]
#                     image_url = f"https://www.mtgpics.com/pics/art/{'/'.join(image_url)}"
#                     name = art.div.select_one("div.Card12").a.contents[0]
#                     artist = art.div.select_one("div.S10").a.contents[0]
#                     _, width, _, height = art.div.select_one("div.S10").contents[-1].split(" ")
#                     width = int(width)
#                     height = int(height)
#                     a = {
#                         "name": name,
#                         "id": id,
#                         "image_url": image_url,
#                         "artist": artist,
#                         "width": width,
#                         "height": height,
#                         "set_name": new_set["name"]
#                     }
#                     art_data.append(a)
#                     print(a)
#                     cprint(f"{name} SUCCESS", 'green')
#                 except Exception as e:
#                     cprint(f"{name} FAILURE \n {e}", 'red')

    # if len(art_data) >= MAX_IMAGES:
    #     cprint(f"We got all the art for {new_set['name']} ({len(art_data)} >= {MAX_IMAGES})!", "green")
    # else:
    #     cprint(f"We did not get all the art for {new_set['name']} ({len(art_data)} < {MAX_IMAGES})", "red")

    # with open(os.path.join(IMAGES_DIR, new_set['name'], f"___{new_set['name']}.json"), "w") as f:
    #     json.dump(art_data, f, indent=4, sort_keys=True)


# soup = BeautifulSoup(source, "html.parser")
# NUM_PAGES = int(soup.select("div.S14")[0].contents[-1].a.contents[0])

# for i in range(NUM_PAGES):
#     cprint(f"Page: {i + 1}", 'green')
#     print(URL.format(i + 1))
#     s = requests.get(URL.format(i + 1)).text
#     soup = BeautifulSoup(s, "html.parser")
#     for sset in soup.select_one("div.S14").find_next_siblings("div"):
#         a = sset.select_one("a")
#         set_id = a["href"].split("=")[-1]
#         set_name = a.parent.parent.select_one("td.Card18").contents[0]
#         release_date = a.parent.parent.select("td")[-1].select("div.G12")[0].contents[0]
#         sets.append({
#             "set_name": set_name,
#             "set_id": set_id,
#             "release_data": release_date
#         })

# with open("scraped_data/set_data/sets.json", "w") as f:
#     json.dump(sets, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
