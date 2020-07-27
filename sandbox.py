from collections import namedtuple

Card = namedtuple("Card", ['value', 'suit'])

Deck = [Card(x, s) for x in range(2, 15) for s in ('s', 'c', 'h', 'd')]


