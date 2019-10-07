import unittest
from tictactoe.environment import Environment

class TestEnvironment(unittest.TestCase):

    def test_rows_columns_number(self):
        # given
        env = Environment(4, 3)

        # when
        env.set_x(0, 0) # x denoted as -1 in numpy array
        env.set_o(0, 1) # o denoted as 1 in numpy array

        # then
        self.assertEqual(env.rows, 4)
        self.assertEqual(env.columns, 3)

        self.assertEqual(env.board[0, 0], -1)
        self.assertEqual(env.board[0, 1], 1)