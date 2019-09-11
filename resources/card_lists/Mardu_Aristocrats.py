from counter import count

aristo = [
    (4, "Footlight Fiend"),
    (3, "Grim Initiate"),
    (4, "Knight of the Ebon Legion"),
    (4, "Corpse Knight"),
    (4, "Cruel Celebrant"),
    (4, "Fireblade Artist"),
    (3, "Hero of Precinct One"),
    (3, "Judith, the Scourge Diva"),
    (3, "Chandra, Acolyte of Flame"),

    (1, "Legion's End"),
    (2, "Bedevil"),
    (1, "Mortify"),

    (4, "Blood Crypt"),
    (4, "Clifftop Retreat"),
    (4, "Dragonskull Summit"),
    (4, "Godless Shrine"),
    (3, "Isolated Chapel"),
    (4, "Sacred Foundry"),
    (1, "Swamp"),
]

angels = [
    (2, "Plains"),
    (1, "Temple of Silence"),
    (1, "Temple of Triumph"),
    (4, "Sacred Foundry"),
    (4, "Godless Shrine"),
    (3, "Blood Crypt"),
    (2, "Dragonskull Summit"),
    (4, "Isolated Chapel"),
    (4, "Clifftop Retreat"),

    (4, "Bishop of Wings"),
    (2, "Tomik, Distinguished Advokist"),
    (3, "Kaalia, Zenith Seeker"),
    (4, "Resplendent Angel"),
    (2, "Aurelia, Exemplar of Justice"),
    (2, "Seraph of the Scales"),
    (2, "Shalai, Voice of Plenty"),
    (2, "Lyra Dawnbringer"),
    (2, "Skarrgan Hellkite"),
    (1, "Doom Whisperer"),
    (1, "Demonlord Belzenlok"),

    (2, "Cast Down"),
    (2, "Legion's End"),
    (2, "Prison Realm"),
    (2, "Flame Sweep"),
    (2, "Sorin, Vengeful Bloodlord"),

    # (3, "Duress"),
    # (3, "Fry"),
    # (3, "Alpine Moon"),
    # (2, "Noxious Grasp"),
    # (1, "Mortify"),
    # (1, "Disfigure"),
    # (1, "Sorcerous Spyglass"),
    # (1, "Chandra, Awakened Inferno"),
]

print(count(aristo))
print(count(angels))
