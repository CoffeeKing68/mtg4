def count(cards):
    return len(cards), sum([c[0] for c in cards])
