from pokerMC import PokerHandSimulator
from monte_carlo_engine import MonteCarloEngine
from poker import PokerPlayer, Card
import numpy as np

def game_simulation(n_other_players, board = None):
    me = PokerPlayer(Card(14, "c"), Card(13, "d"))
    # board = [Card(14, "d"), Card(14, "s")]
    hands_simulator = PokerHandSimulator(me, n_other_players, board=board)
    MCE = MonteCarloEngine()
    results = MCE.compute(hands_simulator, 1000, parallel=True)
    return str(np.mean(results))

