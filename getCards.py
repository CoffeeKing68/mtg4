from mtgsdk import Card
from pprint import pprint
from datetime import datetime
import pickle

class DeckDownloader:
    def __init__(self, name, deck_list=None, deck_text=None):
        if deck_list is not None:
            self.deck_list = deck_list
        elif deck_text is not None:
            self.deck_list = []
            with open(deck_text) as f:
                for l in f.read().splitlines():
                    quantity, card = l.split(None, 1)
                    self.deck_list.append(tuple([quantity, card]))
        else:
            raise ValueError("Must pass deck_list or deck_text")

        self.cards = []
        self.name = f"{name} {datetime.now()}"

    def download(self):
        for i, (quantity, card) in enumerate(self.deck_list):
            print(i, card)
            try:
                c = Card.where(name=card).all()
                print(len(c))
                self.cards.append(c)
            except:
                print("Failed")

        with open(f"downloads/{self.name}.pkl", "wb") as f:
            pickle.dump(self.cards, f)

    def images(self, index):
        pprint([c.image_url for c in self.cards[index]])

    def sets(self, index):
        pprint([c.set for c in self.cards[index]])

    @staticmethod
    def iid(c):
        print(f"{c.name}_{c.id}")

    @staticmethod
    def todict(cards):
        return [c.__dict__ for c in cards]

    def id(self, index, i=0):
        self.iid(self.cards[index][i])

    def autofill(self):
        finished = []
        unfinished = []
        for i, card in enumerate(self.cards):
            if len(card) == 1:
                finished.append(card[0])
                self.iid(card[0])
            else:
                c = [c for c in card if c.image_url is not None]
                if len(c) == 1:
                    finished.append(c[0])
                    self.iid(c[0])
                else:
                    unfinished.append(i)
            # elif len(list(filter(lambda i: i is not None, [c.image_url for c in card]))) == 1:
                # c = list(filter(lambda i: i is not None, [c.image_url for c in card]))[0]
                # finished.append(c)
                # self.iid(c)
            # else:
                # unfinished.append(i)
        print("Unfinished", unfinished)
        return finished, unfinished


