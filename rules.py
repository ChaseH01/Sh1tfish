from gamestate import Card, PlayerState, GameState
from typing import List

def can_play_card(card: Card, top_of_pile: Card, current_player: PlayerState) -> bool:
    """Check if a card can be legally played on top of the current pile"""

    if top_of_pile is None:
        return True
    
    
    if card.rank == 2:  # 2 can be played on any card
        return True
    
    if card.rank == 10:  # 10 clears the pile
        return True
    
    if card.rank == top_of_pile.rank:  # Can play cards of the same rank
        return True
    
    if card.rank > top_of_pile.rank:  # Must play higher cards
        return True

    return False

def get_legal_moves(state: GameState) -> List[Card]:
    """Get all the legal moves for the current player"""
    current_player = state.current_player_state()
    top_of_pile = state.pile[-1] if state.pile else None
    legal_moves = []

    # Add all cards from the player's hand that are legal to play
    for card in current_player.hand:
        if can_play_card(card, top_of_pile, current_player):
            legal_moves.append(card)

    # Add face-up cards that can be legally played (once the hand is exhausted)
    if not current_player.hand:  # If hand is empty, use face-up cards
        for card in current_player.upcards:
            if can_play_card(card, top_of_pile, current_player):
                legal_moves.append(card)

    return legal_moves

def pick_up_pile(state: GameState):
    """If the current player cannot play any legal card, they pick up the pile"""
    current_player = state.current_player_state()
    if not get_legal_moves(state):  # No legal moves
        current_player.pick_up_pile(state.pile)
        state.pile.clear()  # Clear the pile after it's picked up


def play_card(state: GameState, card: Card):
    """Simulate playing a card"""
    current_player = state.current_player_state()
    
    if card in current_player.hand:
        current_player.hand.remove(card)
    elif card in current_player.upcards:
        current_player.upcards.remove(card)
    
    # Add the played card to the pile
    state.pile.append(card)

    # Move to the next player
    state.current_player = (state.current_player + 1) % len(state.players)
