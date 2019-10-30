import urllib.request
import urllib.error
import os
from termcolor import cprint

SSET = "ELD"
SCRAPED_DIR = "scraped_images"
DOWNLOAD_DIR = os.path.join(SCRAPED_DIR, SSET)

if not os.path.isdir(SCRAPED_DIR):
    os.mkdir(SCRAPED_DIR)

if not os.path.isdir(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

for i in range(350):
    download_to = os.path.join(DOWNLOAD_DIR, f"{i}.jpg")
    if not os.path.isfile(download_to):
        try:
            urllib.request.urlretrieve(f"https://www.mtgpics.com/pics/art/{SSET.lower()}/{i:03}.jpg",
                download_to)
            cprint(f"{i}: Successful", "green")
        except urllib.error.HTTPError as e:
            cprint(f"{i}: Failed: {e}", "red")
    else:
        cprint(f"{i}: Passing over image, already exists", 'yellow')
