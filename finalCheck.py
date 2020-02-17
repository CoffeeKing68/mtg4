from csv import DictReader
from termcolor import cprint
from os.path import isfile
from shutil import copy2
from os import listdir
from PyPDF2 import PdfFileMerger, PdfFileReader

total = 0
# with open("singles.csv") as f:
#     d = DictReader(f)
#     for row in d:
#         src = f"test_images/final_print/{row['name_long']}"
#         for i in range(int(row["quantity"])):
#             name, format = row['name_long'].split('.')
#             name += f"_{i}"
#             dest = f"test_images/final_print_duplicates/{name}.{format}"
#             copy2(src, dest)

merger = PdfFileMerger()
artDir = "test_images/final_print_duplicates"
for i, artPdf in enumerate([a for a in listdir(artDir) if a.endswith(".pdf")]):
    print(i, artPdf)
    merger.append(PdfFileReader(open(f"{artDir}/{artPdf}", "rb")))
    merger.append(PdfFileReader(open("resources/examples/back.pdf", "rb")))

merger.write("test_images/final_print_duplicates/__merge_with_back.pdf")
merger.close()
        # if isfile():
        #     cprint(row["name_long"], "green")
        # else:
        #     cprint(row["name_long"], "red")
        # total += int(row["quantity"])
print(total)