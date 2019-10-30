from getCards import DeckDownloader

deck_list = [
    (3, "Dire Fleet Poisoner"),
    # (4, "Spectral Sailor"),
    # (4, "Nightpack Ambusher"),
    # (4, "Frilled Mystic"),
    # (4, "Brineborn Cutthroat"),
    (1, "Disfigure"),
    (2, "Tyrant's Scorn"),
    (2, "Cast Down"),
    (4, "Lookout's Dispersal"),
    (1, "Temple of Malady"),
    (2, "Drowned Catacomb"),
    (2, "Golgari Guildgate"),
]

deck_text = "test_images/all_render/Printing/Sultai_Flash/print_list.txt"

dl = DeckDownloader("Sultai_Flash", deck_text=deck_text)
dl.download()
