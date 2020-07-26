import random
import collections
import poker

class PokerHandsSimulator:
    # hand : tuple of Cards  (Card(x,s1), Card(y,s2))
    # board : tuple of Cards or ()
    def __init__(self, hand, board):
        self.hand = hand
        self.initial_board = board
    
    def simulation(self, n_other_players):
        deck = poker.Deck()
        # Remove hand and board from the deck
        deck.draw_cards(self.hand)
        deck.draw_cards(self.initial_board)

        # Shuffle the deck
        deck.shuffle()

        # Distribute cards to the players
        players_hand = [poker.PokerPlayer(deck.draw(), deck.draw()) for _ in range(n_other_players)]
        my_hand = poker.PokerPlayer(*self.hand)

        # Draw final board
        final_board = self.draw_board_from(deck)
 
        print(my_hand)
        print(players_hand)
        print(final_board)
        print(deck)


    def draw_board_from(self, deck):
        board = self.initial_board.copy()
        while len(board) < 5 :
            if len(board) == 0 or len(board) == 3 or len(board) == 4 :
                deck.draw() #burn the card
            board.append(deck.draw())
        return board
            

if __name__ == "__main__":
    hand = (poker.Card(13, 's'), poker.Card(12, 's'))
    board = [poker.Card(13,'d'), poker.Card(6,'h'), poker.Card(5,'d')]
    app = PokerHandsSimulator(hand, board)
    app.simulation(5)
    app.simulation(5)
    
    