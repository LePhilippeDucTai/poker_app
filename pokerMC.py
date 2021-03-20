from poker import PokerPlayer, Deck, Card

class from poker import PokerPlayer, Deck, Card:
    def __init__(self, me, n_players, board=None) -> None:
        self.n_players = n_players
        self.me = me
        # tuples : ex : board = [Card(5, "s"), Card(11, "h"), Card(13, "s")]
        self.board = board

    def simulate(self, id):
        deck = Deck()
        deck.shuffle()
        deck.draw_cards(self.me.hand)

        if self.board:
            deck.draw_cards(self.board)
            new_board = self.board + [deck.draw() for _ in range(5 - len(self.board))]
        else:
            new_board = [deck.draw() for _ in range(5)]

        other_players = [
            PokerPlayer(deck.draw(), deck.draw()) for _ in range(self.n_players)
        ]
        my_rank = self.me.my_rank(new_board)
        maximum_other_ranks = max(
            [player.my_rank(new_board) for player in other_players]
        )
        return (my_rank >= maximum_other_ranks) * 1
