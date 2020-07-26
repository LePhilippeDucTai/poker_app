import random
import collections 

class Deck:
    def __init__(self):
        self.cards = [Card(k, s) for k in range(2,15) for s in ('c','d','h','s')]

    def draw_cards(self, hand):
        for card in hand :
            self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
       
    def __repr__(self):
        return " ".join([str(card) for card in self.cards])

    @property
    def length(self):
        return len(self.cards)


class Card:
    dict_corr = {11 : 'J', 12 : 'Q', 13 : 'K', 1 :'A', 14 : 'A'}
    def __init__(self, value : int, symbol : str):
        self.value = value
        self.symbol = symbol
    # Consider that J = 11, Q = 12, K = 13, A = {1 ou 14}

    def __repr__(self):
        return f'{self.dict_corr.get(self.value, self.value)}{self.symbol}'
 
    def __eq__(self, other):
        return self.value == other.value and self.symbol == other.symbol

# A hand is constituted with 7 cards but only the best 5 are taken into account
# Implements all the logic in poker combinations
class PokerHandCalculator:
    def __init__(self):
        pass

    @staticmethod
    def is_flush(seven_cards):
        counts_suits = sorted(list(collections.Counter([card.symbol for card in seven_cards]).values()), reverse = True)
        return counts_suits[0] >= 5 #if more or 5 cards of the same symbol then it is a flush

    @staticmethod
    def is_straight(seven_cards):
        cards_values = list(set(card.value for card in seven_cards))
        if len(cards_values) < 5 :
            return False
        else :
            if 14 in cards_values :
                cards_values.append(1)
            cards_values.sort() 
            print(cards_values)
            counter = 0
            last = cards_values[0]
            for v in cards_values[1:] :
                if v == last + 1 :
                    counter += 1
                    print(counter)
                    if counter == 5 :
                        return True

                elif v == last :
                    counter = counter
                else :
                    counter = 0
                    
        return False

    def is_royal_flush(self, seven_cards):
        pass

# A poker Player has two cards only
# A hand is a tuple of Cards
class PokerPlayer:
    def __init__(self, *hand):
        self.hand = hand
        self.bank = 1000

    def __repr__(self):
        return str(self.hand)

    def combination(self, board):
        return self.hand + tuple(board)



class PokerGame:
    def __init__(self, n_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = [PokerPlayer(self.deck.draw(), self.deck.draw()) for _ in range(n_players)]
        self.board = [self.deck.draw() for _ in range(5)]

    def __repr__(self):
        return "\n".join([str(self.players), str(self.board), str(self.deck)])

    def reinit(self, n_players):
        self.__init__(n_players)

    def hands_combinations(self):
        return [player.combination(self.board) for player in self.players]
            


if __name__ == "__main__":
    n_players = 10
    pokergame = PokerGame(n_players)
    print(pokergame.deck)
    hands = pokergame.hands_combinations()
    print(hands)
    counts_values = [sorted(list(collections.Counter([card.value for card in hand]).values()), reverse = True) for hand in hands] 
    counts_suits = [sorted(list(collections.Counter([card.symbol for card in hand]).values()), reverse = True) for hand in hands] 
    
    # print(counts_values)
    # print(counts_suits)
    # print(counts)

    peval = PokerHandCalculator()
    x = list(map(peval.is_straight, hands))
    print(x)