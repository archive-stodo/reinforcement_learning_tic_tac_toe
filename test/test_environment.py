import unittest
from tictactoe.Environment import Environment

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

    def test__game_ended_row_check_when_game_not_ended(self):
        env = Environment(3, 3)
        env.set_o(0, 0)
        env.set_o(0, 1)
        env.set_x(0, 2)

        if_game_ended = env._game_ended_row_check()

        env.print_array(env.board)
        self.assertEqual(False, if_game_ended)

    def test__game_ended_row_check_when_game_not_ended_board_empty(self):
        env = Environment(3, 3)

        if_game_ended = env._game_ended_row_check()

        env.print_array(env.board)
        self.assertEqual(False, if_game_ended)

    def test__game_ended_row_check_when_game_ended(self):
        env = Environment(3, 3)

        env.set_x(1, 0)
        env.set_x(1, 1)
        env.set_x(1, 2)

        if_game_ended = env._game_ended_row_check()

        env.print_array(env.board)
        self.assertEqual(True, if_game_ended)

    def test__game_ended_row_check_when_game_ended_on4x4_board(self):
        env = Environment(4, 4)

        env.set_o(2, 1)
        env.set_o(2, 2)
        env.set_o(2, 3)

        if_game_ended = env._game_ended_row_check()

        env.print_array(env.board)
        self.assertEqual(True, if_game_ended)

    def test__game_ended_column_check_when_game_not_ended(self):
        env = Environment(3, 3)
        env.set_o(0, 0)
        env.set_o(1, 0)
        env.set_x(2, 0)

        if_game_ended = env._game_ended_column_check()

        env.print_array(env.board)
        self.assertEqual(False, if_game_ended)

    def test__game_ended_column_check_when_game_ended(self):
        env = Environment(3, 3)
        env.set_x(0, 0)
        env.set_x(1, 0)
        env.set_x(2, 0)

        if_game_ended = env._game_ended_column_check()

        self.assertEqual(True, if_game_ended)

    def test__game_ended_column_check_when_game_ended_4x3_board(self):
        env = Environment(4, 3)
        env.set_o(1, 1)
        env.set_o(2, 1)
        env.set_o(3, 1)

        env.print_array(env.board)
        if_game_ended = env._game_ended_column_check()

        self.assertEqual(True, if_game_ended)

    def test__game_ended_diagonal_check_when_not_ended(self):
        env = Environment(3, 3)
        env.set_o(0, 0)
        env.set_o(1, 1)
        env.set_o(2, 1)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(False, if_game_ended)

    def test__game_ended_diagonal_check_when_ended_left_to_right(self):
        env = Environment(3, 3)
        env.set_x(0, 0)
        env.set_x(1, 1)
        env.set_x(2, 2)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test__game_ended_diagonal_check_when_ended_left_to_right_on_4x4_board(self):
        env = Environment(4, 4)
        env.set_x(1, 1)
        env.set_x(2, 2)
        env.set_x(3, 3)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test__game_ended_diagonal_check_when_ended_right_to_left_on_4x4_board(self):
        env = Environment(4, 4)
        env.set_o(1, 3)
        env.set_o(2, 2)
        env.set_o(3, 1)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test2__game_ended_diagonal_check_when_ended_right_to_left_on_4x4_board(self):
        env = Environment(4, 4)
        env.set_o(1, 2)
        env.set_o(2, 1)
        env.set_o(3, 0)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test__game_ended_diagonal_check_when_not_ended_on_4x4_board(self):
        env = Environment(4, 4)
        env.board.fill(1)
        env.set_o(2, 1)
        env.set_o(2, 2)
        env.set_o(2, 3)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(False, if_game_ended)

    def test__game_ended_diagonal_check_on_12x12_board(self):
        env = Environment(12, 12)
        env.set_o(9, 2)
        env.set_o(10, 1)
        env.set_o(11, 0)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test2__game_ended_diagonal_check_on_12x12_board(self):
        env = Environment(12, 12)
        env.set_o(4, 4)
        env.set_o(5, 5)
        env.set_o(6, 6)
        env.print_array(env.board)

        if_game_ended = env._game_ended_diagonal_check()

        self.assertEqual(True, if_game_ended)

    def test_game_ended_when_not_ended(self):
        env = Environment(2, 2)
        env.print_array(env.board)

        game_ended = env.check_game_ended()

        self.assertEqual(False, game_ended)

    def test_game_ended_when_x_has_won_but_no_force_recalculate(self):
        env = Environment(3, 3)
        env.set_x(0, 0)
        env.set_x(1, 0)
        env.set_x(2, 0)
        env.print_array(env.board)

        game_ended = env.check_game_ended()

        self.assertEqual(False, game_ended)

    def test_game_ended_when_x_has_won_(self):
        env = Environment(3, 3)
        env.set_x(0, 0)
        env.set_x(1, 0)
        env.set_x(2, 0)
        env.print_array(env.board)

        game_ended = env.check_game_ended(force_recalculate=True)

        self.assertEqual(True, game_ended)

    def test__draw_check_when_no_draw(self):
        env = Environment(3, 3)
        env.set_x(0, 0)
        env.set_x(1, 0)
        env.set_o(2, 0)
        env.print_array(env.board)

        env._draw_check()

        self.assertEqual(False, env.draw)

    def test__draw_check_when_draw(self):
        env = Environment(3, 3)
        env.board.fill(1)
        env.set_o(1, 1)
        env.print_array(env.board)

        env._draw_check()

        self.assertEqual(True, env.draw)

    def test_get(self):
        env = Environment(2, 2)

        results = env.get_all_possible_states(env.board, 1, [])

        self.assertTrue(len(results) != 0)

    def test_get_board_from_state_number_23(self):
        # given
        env = Environment(2, 2)
        state_number = 23

        # when - conversion from state number to board and back to number
        board_from_state = env.get_board_from_state_number(state_number, True)
        state_number_from_board = env.get_state_number(board_from_state)

        # then
        self.assertEqual(state_number_from_board, state_number)

    def test_get_board_from_state_number_80(self):
        # given
        env = Environment(2, 2)
        state_number = 80

        # when - conversion from state number to board and back to number
        board_from_state = env.get_board_from_state_number(state_number, True)
        state_number_from_board = env.get_state_number(board_from_state)

        # then
        self.assertEqual(state_number_from_board, state_number)
