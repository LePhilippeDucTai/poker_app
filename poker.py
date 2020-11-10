import random
import collections
import itertools as it


class Deck:
    def __init__(self):
        self.cards = [Card(k, s) for k in range(2, 15) for s in ("c", "d", "h", "s")]

    def draw_cards(self, hand):
        for card in hand:
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
    dict_corr = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, *tuple):
        self.value = tuple[0]
        self.symbol = tuple[1]

    def __repr__(self):
        return f"{self.dict_corr.get(self.value, self.value)}{self.symbol}"

    def __eq__(self, other):
        return self.value == other.value and self.symbol == other.symbol


# A hand is constituted with 7 cards but only the best 5 are taken into account
# Implements all the logic in poker combinations
class PokerHandCalculator:
    straight_flush_royale_combs = [
        set(((14, c), (13, c), (12, c), (11, c), (10, c))) for c in "schd"
    ]
    straight_flush_combs = [
        set((x, c) for x in range(i, i + 5)) for i in range(2, 11) for c in "schd"
    ] + [set((x, c) for x in (14, 2, 3, 4, 5)) for c in "schd"]
    straight_combs = [{14, 2, 3, 4, 5}] + [
        set(x for x in range(i, i + 5)) for i in range(2, 11)
    ]

    def __init__(self, seven_cards):
        self.seven_cards = seven_cards
        self.count_values = None
        self.count_suits = None
        self.most_frequent_suit = None

    def count_tuples(self, suit_for_flush=None):
        if suit_for_flush:
            self.seven_cards = [
                card for card in self.seven_cards if card[1] == suit_for_flush
            ]
        tuples_counter = collections.Counter(
            [value for value, _ in self.seven_cards]
        ).items()
        tuples_sorted_keys = sorted(
            tuples_counter, key=lambda item: item[0], reverse=True
        )
        tuple_cards = sorted(tuples_sorted_keys, key=lambda item: item[1], reverse=True)
        return tuple_cards

    def is_straight_flush_royale(self):
        for comb in self.straight_flush_royale_combs:
            if comb.issubset(self.seven_cards):
                return True
        return False

    def is_straight_flush(self):
        for comb in self.straight_flush_combs:
            if comb.issubset(self.seven_cards):
                return True
        return False

    def is_square(self):
        self.count_values = sorted(
            list(
                collections.Counter([value for value, _ in self.seven_cards]).values()
            ),
            reverse=True,
        )
        return max(self.count_values) == 4

    def is_full_house(self):
        return (
            self.count_values == [3, 3, 1]
            or self.count_values == [3, 2, 1, 1]
            or self.count_values == [3, 2, 2]
        )

    # Must treat this
    def is_flush(self):
        counter_suits = collections.Counter([suit for _, suit in self.seven_cards])
        counts_values = list(counter_suits.values())

        # if more or 5 cards of the same symbol then it is a flush
        if max(counts_values) >= 5:
            self.most_frequent_suit = counter_suits.most_common(1)[0][0]
            return True
        else:
            return False

    def is_straight(self):
        set_values = set(x for x, _ in self.seven_cards)
        for comb in self.straight_combs:
            if comb.issubset(set_values):
                return True
        return False

    def is_three_of_kind(self):
        return self.count_values == [3, 1, 1, 1, 1]

    def is_two_pairs(self):
        return self.count_values in [[2, 2, 1, 1, 1], [2, 2, 2, 1]]

    def is_pair(self):
        return self.count_values == [2, 1, 1, 1, 1, 1]

    def compute_score(self, tuple_value_count):
        accumulated_counts = it.accumulate(
            tuple_value_count, lambda acc, k: (k[0], k[1] + acc[1])
        )
        shorten_tuple = list(it.takewhile(lambda x: x[1] <= 5, accumulated_counts))
        n = len(shorten_tuple)
        products = sum(
            [k[0] * k[1] * 14 ** (n - i) for i, k in enumerate(shorten_tuple)]
        )
        denominator = sum(
            [k[1] * 14 ** (n - i + 1) for i, k in enumerate(shorten_tuple)]
        )
        return 100 * products / denominator

    def evaluate_hand(self):
        if self.is_straight_flush_royale():
            comb, rank = ("Straight Flush Royale", 900)
        elif self.is_straight_flush():
            comb, rank = ("Straight Flush", 800)
        elif self.is_square():
            comb, rank = ("Square", 700)
        elif self.is_full_house():
            comb, rank = ("Full House", 600)
        elif self.is_flush():
            comb, rank = ("Flush", 500)
        elif self.is_straight():
            comb, rank = ("Straight", 400)
        elif self.is_three_of_kind():
            comb, rank = ("Three of Kind", 300)
        elif self.is_two_pairs():
            comb, rank = ("Two Pairs", 200)
        elif self.is_pair():
            comb, rank = ("Pair", 100)
        else:
            comb, rank = ("High Card", 0)

        tuple_cards = self.count_tuples(suit_for_flush=self.most_frequent_suit)
        return (comb, rank + self.compute_score(tuple_cards))


# A poker Player has two cards only
# A hand is a tuple of Cards
class PokerPlayer:
    def __init__(self, *hand):
        self.hand = hand
        self.str_game = None

    def __repr__(self):
        return str(self.str_game)

    def combination(self, board):
        strboard = "\033[32m" + str(board)
        self.str_game = str(self.hand) + strboard + "\033[m"
        return [(card.value, card.symbol) for card in it.chain(self.hand, board)]


class PokerGame:
    def __init__(self, n_other_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.me = PokerPlayer(self.deck.draw(), self.deck.draw())
        self.players = [self.me] + [
            PokerPlayer(self.deck.draw(), self.deck.draw())
            for _ in range(n_other_players)
        ]
        self.board = [self.deck.draw() for _ in range(5)]

    def __repr__(self):
        return "\n".join([str(self.players), str(self.board), str(self.deck)])

    def reinit(self, n_players):
        self.__init__(n_players)

    def hands_combinations(self):
        return [player.combination(self.board) for player in self.players]

    def hands_print(self):
        print([str(player) for player in self.players])


if __name__ == "__main__":
    n_players = 10
    pokergame = PokerGame(n_players)
    hands = pokergame.hands_combinations()
    eval = [PokerHandCalculator(hand).evaluate_hand() for hand in hands]
    hands_str = "\n".join(
        map(str, sorted(zip(eval, pokergame.players), key=lambda t: t[0][1]))
    )
    print(hands_str)
