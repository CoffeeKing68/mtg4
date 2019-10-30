import urllib.request
import urllib.error
import os
from termcolor import cprint
from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.mtgpics.com/sets_chrono?page_nb={}"

# if not os.path.isfile("mtgpics_sets.html"):
source = requests.get(URL.format(1)).text
with open("mtgpics_sets.html", "w") as f:
    f.write(source)
# else:
#     with open("mtgpics_sets.html") as f:
#         source = f.read()

if not os.path.isdir("scraped_data"):
    os.mkdir("scraped_data")

if not os.path.isdir("scraped_data/set_data"):
    os.mkdir("scraped_data/set_data")

soup = BeautifulSoup(source, "html.parser")
NUM_PAGES = int(soup.select("div.S14")[0].contents[-1].a.contents[0])

sets = []

for i in range(NUM_PAGES):
    cprint(f"Page: {i + 1}", 'green')
    print(URL.format(i + 1))
    s = requests.get(URL.format(i + 1)).text
    soup = BeautifulSoup(s, "html.parser")
    for sset in soup.select_one("div.S14").find_next_siblings("div"):
        a = sset.select_one("a")
        set_id = a["href"].split("=")[-1]
        set_name = a.parent.parent.select_one("td.Card18").contents[0]
        release_date = a.parent.parent.select("td")[-1].select("div.G12")[0].contents[0]
        sets.append({
            "name": set_name,
            "id": set_id,
            "release_date": release_date
        })

with open("scraped_data/set_data/sets.json", "w") as f:
    json.dump(sets, f, indent=4, sort_keys=True)

