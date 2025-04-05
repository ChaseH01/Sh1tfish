import random
from gamestate import Card, PlayerState, GameState
from typing import List

# Color codes
RESET = "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def create_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = list(range(2, 15))  # 2-10, 11=J, 12=Q, 13=K, 14=A
    return [Card(rank, suit) for suit in suits for rank in ranks]

def deal_cards(num_players: int):
    deck = create_deck()
    random.shuffle(deck)

    players = []
    for _ in range(num_players):
        downcards = [deck.pop() for _ in range(3)]
        upcards = [deck.pop() for _ in range(3)]
        hand = [deck.pop() for _ in range(3)]
        players.append(PlayerState(hand, upcards, downcards))

    discarded_cards = []  # Initialize an empty discarded pile
    # Remaining cards after dealing are the draw pile
    draw_pile = deck  # All remaining cards form the draw pile

    deck_size = len(draw_pile)  # Remaining cards after dealing

    return GameState(
        players=players,
        pile=[],  # Empty at the start
        discarded_cards=discarded_cards,
        deck_size=deck_size,
        current_player=0,
        draw_pile=draw_pile  # Pass the draw pile into the game state
    )

def print_game_state(game_state: GameState):
    print(f"{BLUE}\n=== Current Game State ===")
    print(f"Current Player: Player {game_state.current_player}")
    print(f"Pile: {game_state.pile}")
    for i, player in enumerate(game_state.players):
        hand_list = list(player.hand)
        print(f"Player {i} Hand: {[f'{idx}: {card}' for idx, card in enumerate(hand_list)]}")
        print(f"Player {i} Upcards: {[f'{idx}: {card}' for idx, card in enumerate(player.upcards)]}")
        print(f"Player {i} Downcards: {[f'{idx}: {card}' for idx, card in enumerate(player.downcards)]}")
    print("\n")
    print(f"Discarded Pile: {game_state.discarded_cards}")
    print("\n")
    print(f"Draw Pile: {game_state.draw_pile}")
    print(f"==========================\n{RESET}")

def draw_cards(player: PlayerState, draw_pile: List[Card]):
    while len(player.hand) < 3 and draw_pile:
        player.hand.append(draw_pile.pop())  # Draw from the draw pile


def should_burn_pile(pile):
    if not pile:
        return False
    if pile[-1].rank == 10:
        return True
    return False

def main():
    # Set up a simple test game with 2 players
    game_state = deal_cards(2)

    while True:
        print_game_state(game_state)
        player = game_state.players[game_state.current_player]

        if not player.hand:
            print(f"{GREEN}Player {game_state.current_player} has no cards left! Skipping turn.{RESET}")
            game_state.current_player = (game_state.current_player + 1) % len(game_state.players)
            continue

        print(f"{GREEN}Player {game_state.current_player}'s turn.{RESET}")
        print(f"{YELLOW}Options:")
        print("1. Play a card")
        print("2. Pick up pile")
        choice = input(f"{YELLOW}Choose action (1 or 2): {RESET}")

        if choice == "1":
            hand_list = list(player.hand)
            print(f"{YELLOW}Your hand:")
            for idx, card in enumerate(hand_list):
                print(f"{YELLOW}{idx}: {card}{RESET}")

            idx = int(input(f"{YELLOW}Enter the index of the card you want to play: {RESET}"))

            if idx < 0 or idx >= len(hand_list):
                print(f"Invalid index. Try again.{RESET}")
                continue

            card = hand_list[idx]
            if len(game_state.pile) == 0:
                top = Card(0, 'hearts')
            else:
                top = game_state.pile[-1]

            # Check if the card is valid to play (example rule: rank must match top card)
            if card.rank < top.rank:
                print(f"Invalid move! The rank of the card does not match the top card of the pile.{RESET}")
                continue

            # Simulate playing the card and checking rules
            if should_burn_pile(game_state.pile):
                print(f"{GREEN}Burning the play pile with {card}. Player {game_state.current_player} gets another turn.")
                game_state.discarded_cards.extend(game_state.pile)  # Add play pile to discarded pile
                game_state.pile.clear()  # Clear the play pile

            if card.rank == 10:
                print(f"{GREEN}Playing {card}. You get to discard and draw two cards.{RESET}")
                game_state.pile.append(card)  # Add card to the play pile
                player.hand.remove(card)
                # Draw two cards from the draw pile
                draw_cards(player, game_state.draw_pile)
                draw_cards(player, game_state.draw_pile)

            else:
                # Otherwise just add the card to the play pile
                game_state.pile.append(card)
                player.hand.remove(card)
                draw_cards(player, game_state.draw_pile)

        elif choice == "2":
            print(f"{GREEN}Picking up the pile...{RESET}")
            player.hand.extend(game_state.pile)  # Add all cards from play pile to the player's hand
            game_state.pile.clear()  # Clear the play pile
            draw_cards(player, game_state.draw_pile)  # Draw new cards from the draw pile

        else:
            print(f"Invalid choice. Try again.{RESET}")
            continue

        # Move to next player
        game_state.current_player = (game_state.current_player + 1) % len(game_state.players)

if __name__ == "__main__":
    main()
