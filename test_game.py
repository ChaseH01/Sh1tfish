import unittest
from gamestate import Card, PlayerState, GameState
from rules import can_play_card

class TestGameState(unittest.TestCase):
    def setUp(self):
        # Create some sample cards
        self.card3 = Card(3, "hearts")
        self.card5 = Card(5, "spades")
        self.card2 = Card(2, "clubs")
        self.card10 = Card(10, "diamonds")

    def test_initial_game_state(self):
        players = [PlayerState([], [], []) for _ in range(4)]
        pile = []
        burned_cards = []
        current_player = 0
        deck_size = 52

        game_state = GameState(players, pile, burned_cards, deck_size, current_player)

        self.assertEqual(len(game_state.players), 4)
        self.assertEqual(game_state.deck_size, 52)
        self.assertEqual(game_state.current_player, 0)
        self.assertEqual(len(game_state.pile), 0)

    def test_initial_player_hand(self):
        players = [PlayerState([self.card3, self.card5], [], []) for _ in range(4)]
        pile = []
        burned_cards = []
        current_player = 0
        deck_size = 52

        game_state = GameState(players, pile, burned_cards, deck_size, current_player)

        self.assertEqual(len(game_state.players[0].hand), 2)

    def test_play_card_legality(self):
        player = PlayerState([self.card3, self.card5], [], [])
        
        self.assertTrue(can_play_card(self.card2, self.card5, player))  # 2 can always be played
        self.assertTrue(can_play_card(self.card10, self.card5, player)) # 10 can always be played (assume burn)
        self.assertFalse(can_play_card(self.card3, self.card5, player)) # 3 can't beat 5

    def test_pick_up_pile(self):
        player = PlayerState([], [], [])
        pile = [self.card3, self.card5]

        player.pick_up_pile(pile)

        self.assertIn(self.card3, player.hand)
        self.assertIn(self.card5, player.hand)
        self.assertEqual(len(player.hand), 2)

if __name__ == '__main__':
    unittest.main()
