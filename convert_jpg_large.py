import os
from shutil import move

print("Enter directory to clean")
DIR = input(">> ")
# DIR = os.getcwd()

for f in os.listdir(DIR):
    if f.endswith(".jpg_large"):
        move(os.path.join(DIR, f), os.path.join(f"{f[:-10]}.jpg"))

