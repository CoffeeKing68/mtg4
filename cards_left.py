import os
import json
from pprint import pprint

SSET = "ELD"
CARDS_PER_PAGE = 5
P = 0
with_art = os.listdir(f"resources/art/{SSET}")

with open(f"resources/set_data/{SSET}.json") as f:
    original_cards = json.load(f)
    original_cards = [c for c in original_cards if 'Adventure' not in c['subtypes']]

cards = [c for c in original_cards if f"{c['name']}_{c['id']}.jpg" not in with_art]
print(len(cards))

def print_cards(p, cards_per_page):
    for i, c in enumerate(cards[p * cards_per_page: cards_per_page * (p + 1)]):
        print(f"{i + (P * cards_per_page):03}: {c['name']}")
        print(f"https://www.google.com/search?q={c['name'].replace(' ', '+')}+mtg+art+{c['artist'].replace(' ', '+')}+{SSET}&sxsrf=ACYBGNSKRWokxPgDALATOgroAdCfL0nwFQ:1569690141922&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiOgsS6__PkAhWMOcAKHV_gCzkQ_AUIEigB&biw=1280&bih=598")


print_cards(P, CARDS_PER_PAGE)

quit = False
while not quit:
    response = input(">> ")
    if response == "quit":
        quit = True
    elif response == "re" or response == "reset":
        with_art = os.listdir(f"resources/art/{SSET}")
        cards = [c for c in original_cards if f"{c['name']}.jpg" not in with_art]
        print_cards(P, CARDS_PER_PAGE)
    elif response == "n" or response == "next":
        P += 1
        print_cards(P, CARDS_PER_PAGE)
    elif response == "p" or response == "prev":
        P -= 1
        print_cards(P, CARDS_PER_PAGE)
    elif response.isnumeric():
        P = int(response)
        print_cards(P, CARDS_PER_PAGE)
    else:
        print(f"'{response}' is not valid.")

