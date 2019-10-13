import unittest
from tictactoe.main import *


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env = Environment(3, 3)
        cls.triples = get_state_number_winner_ended_triple(cls.env, verbose_lvl=2)

    def test_get_state_number_winner_ended_triple(self):
        # given - board where x has won
        won_environment = Environment(3, 3)
        won_environment.set_x(0, 0)
        won_environment.set_x(1, 1)
        won_environment.set_x(2, 2)
        won_environment.set_o(0, 1)
        won_environment.set_o(1, 2)
        won_environment.print_array(won_environment.board)

        won_environment_state_number = won_environment.get_state_number(won_environment.board)

        # to check that conversion board <-> number works
        board_from_number = self.env.get_board_from_state_number(won_environment_state_number)

        state_number, winner, ended = self.triples[won_environment_state_number]

        self.assertEqual(won_environment.board, board_from_number)
        self.assertEqual(won_environment_state_number, state_number)
        self.assertEqual(winner, 1)
        self.assertEqual(ended, True)
