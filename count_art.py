import os
from pprint import pprint

ART_DIR = os.path.join("resources", "art")
set_count = {}

for sset in os.listdir(ART_DIR):
    SET_DIR = os.path.join(ART_DIR, sset)
    if os.path.isdir(SET_DIR):
        set_count[sset] = 0
        for image in os.listdir(SET_DIR):
            if not image.endswith("full.jpg"):
                set_count[sset] += 1

pprint(sorted(set_count.items(), key=lambda kv: kv[1], reverse=True))
print(sum(set_count.values()))


