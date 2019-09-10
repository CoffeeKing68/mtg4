from mtgsdk import Card
import pickle

JeffHoogland = [
    (4, "Commune with Dinosaurs"),
    (4, "Marauding Raptor"),
    (4, "Otepec Huntmaster"),
    (4, "Lava Coil"),
    (4, "Rampaging Ferocidon"),
    (2, "Savage Stomp"),
    (4, "Ripjaw Raptor"),
    (4, "Shifting Ceratops"),
    (3, "Regisaur Alpha"),
    (1, "Ghalta, Primal Hunger 1"),
    (2, "Ghalta, Primal Hunger 2"),
    (2, "Mountain 1"),
    (2, "Mountain 2"),
    (2, "Mountain 3"),
    (2, "Forest 1"),
    (2, "Forest 2"),
    (2, "Forest 3"),
    (4, "Rootbound Crag"),
    (4, "Stomping Ground"),

    (1, "Fry"),
    (3, "Veil of Summer"),
    (2, "Vivien Reid"),
    (3, "Cindervines"),
    # (3, "Sentinel Totem"),
]

mtgdecks = [
    # (4, "Otepec Huntmaster"),
    # (4, "Marauding Raptor"),
    (2,  "Drover of the Mighty"),
    (3,  "Ranging Raptors"),
    # (2, "Rampaging Ferocidon"),
    # (4, "Ripjaw Raptor"),
    # (2, "Shifting Ceratops"),
    # (3, "Regisaur Alpha"),
    (1,  "Etali, Primal Storm"),
    (1,  "Gishath, Sun's Avatar"),

    (2,  "Reckless Rage"),
    (1,  "Uncaged Fury"),
    (2,  "Lightning Strike"),

    # (4, "Commune with Dinosaurs"),
    (2,  "Bond of Flourishing"),
    (3,  "Domri's Ambush"),
    (3,  "Domri, Anarch of Bolas"),
    # (4, "Stomping Ground"),
    (3,  "Unclaimed Territory"),
    # (4, "Mountain"),
    # (5, "Forest"),
    (1,  "Temple of Triumph"),
    # (4, "Rootbound Crag"),

    (2,  "Carnage Tyrant"),
]

extra = [
    (3, "Dinosaur"),
    (4, "Priest of the Forgotten Gods"),
    (3, "God-Eternal Bontu"),
    # (4, "Fanatical Firebrand"),
    (4, "Mayhem Devil"),
    (3, "Shock"),
]



total = 0
unique = 0
with open("test_images/all_render/Printing/RG_Dinos/print_list.txt", "w") as f:
    for quantity, card in sorted(JeffHoogland + mtgdecks + extra, key=lambda x: x[1]):
        f.write(f"{quantity}x {card}\n")
        unique += 1
        total += quantity

print(total)
print(unique)


# dinosaurs = []
# for i, (q, card) in enumerate(mtgdecks):
#     print(i, card)
#     c = Card.where(name=card).all()
#     print(len(c))
#     dinosaurs.append(c)

# with open("dinos.pkl", "wb") as f:
#     pickle.dump(dinosaurs, f)

# with open("dinos.pkl", "rb") as f:
#     d = pickle.load(f)

# def images(array):
#     print([c.image_url for c in array])

# def id(index, array):
#     print(f"{array[index].name}_{array[index].id}")

