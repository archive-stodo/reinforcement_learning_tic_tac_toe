import unittest
from tictactoe.environment import Environment

class TestEnvironment(unittest.TestCase):

    def test_rows_columns_number(self):
        # given
        env = Environment(4, 3)

        # when
        env.set_x(0, 0) # x denoted as 1 in numpy array
        env.set_o(0, 1) # o denoted as 2 in numpy array

        # then
        self.assertEqual(env.rows, 4)
        self.assertEqual(env.columns, 3)

        self.assertEqual(env.board[0, 0], 1)
        self.assertEqual(env.board[0, 1], 2)

    def test_get_state_number(self):
        env = Environment(3, 3)
        env.set_x(0, 0) # 1
        env.set_x(0, 1) # 3
        env.set_x(0, 2) # 9
        env.set_o(1, 1) # 3^4 * 2 = 162
        state_number = env.get_state_number()

        self.assertEqual(175, state_number)

    def test_3x3_max_number_for_get_state_number(self):
        env = Environment(3, 3)
        env.board.fill(2)

        state_number = env.get_state_number()

        self.assertEqual(3 ** 9 - 1, state_number)

    def test_4x4_max_number_for_get_state_number(self):
        env = Environment(4, 4)
        env.board.fill(2)

        state_number = env.get_state_number()

        self.assertEqual(3 ** 16 - 1, state_number)