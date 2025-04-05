from typing import List, Set
from collections import deque

# Define Card class to represent individual cards in the deck
class Card:
    def __init__(self, rank: int, suit: str):
        self.rank = rank  # 2-10, J=11, Q=12, K=13, A=14
        self.suit = suit  # "hearts", "diamonds", "clubs", "spades"
    
    def __repr__(self):
        return f"{self.rank}{self.suit[0].upper()}"

# Define PlayerState class to represent individual player states
class PlayerState:
    def __init__(self, hand: List[Card], upcards: List[Card], downcards: List[Card]):
        self.hand = hand      # Cards in hand, fully known
        self.upcards = upcards     # Face-up cards
        self.downcards = downcards  # Face-down cards (unknown until played)

    def is_empty(self) -> bool:
        return not self.hand and not self.upcards and not self.downcards

    def pick_up_pile(self, pile: List[Card]):
        """Player picks up the pile; adds all cards to their hand"""
        self.hand.update(pile)

# Define the GameState class to represent the full game state
class GameState:
    def __init__(self, players, pile, discarded_cards, deck_size, current_player, draw_pile):
        self.players = players
        self.pile = pile
        self.discarded_cards = discarded_cards
        self.deck_size = deck_size
        self.current_player = current_player
        self.draw_pile = draw_pile  # The draw pile is now part of the game state


    def current_player_state(self) -> PlayerState:
        """Return the state of the current player"""
        return self.players[self.current_player]
