from monte_carlo_engine import MonteCarloEngine
from poker import PokerPlayer, Deck, Card
import numpy as np


class PokerHandSimulator:
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


if __name__ == "__main__":
    n_other_players = 6
    me = PokerPlayer(Card(9, "c"), Card(9, "d"))
    board = [Card(11, "d"), Card(12, "s"), Card(4, "s")]
    # board = None
    hands_simulator = PokerHandSimulator(me, n_other_players, board=board)
    MCE = MonteCarloEngine()
    results = MCE.compute(hands_simulator, 50000, parallel=True)
    print(np.mean(results))
