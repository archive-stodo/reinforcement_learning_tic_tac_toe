import numpy as np

class Environment:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns), int)
        self.winner = None
        self.game_ended = False
        self.draw = False
        self.num_states = 3**(rows*columns)

    def reward(self, player_symbol):
        if not self.is_game_over():
            return 0

        return 1 if self.winner == player_symbol else 0

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def get_state_number(self, board):
        power = 0
        state_number = 0
        for row in range(len(board)):
            for column in range(len(board[0])):
                current_field_value = board[row][column] # 0 1 2
                state_number += 3**power * current_field_value
                power += 1

        return state_number

    def get_state_number_winner_ended_triple(env, i=0, j=0):
        pass

    def get_all_possible_states(self, board, player_turn, visited_state_numbers):
        results = []
        results.append((self.get_state_number(board), self.game_ended, self.winner))

        possible_moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i, j] not in (1, 2):
                    board_copy = board.copy()
                    board_copy[i, j] = player_turn
                    next_move_state_number = self.get_state_number(board_copy)

                    if next_move_state_number not in visited_state_numbers:
                        visited_state_numbers.append(next_move_state_number)
                        possible_moves.append((i, j))

        for move in possible_moves:
            previous_state = self.board[move]
            self.board[move] = player_turn
            self.check_game_ended(force_recalculate=True)

            results.append((self.get_state_number(self.board), self.game_ended, self.winner))

            self.board[move] = previous_state

            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1

            board_copy = board.copy()
            board_copy[move] = player_turn
            results += self.get_all_possible_states(board_copy, player_turn, visited_state_numbers)

        return results

    def initialV_x(env, state_winner_triples):
        pass

    def initialV_o(env, state_winner_triples):
        pass

    def check_game_ended(self, force_recalculate=False):
        if not force_recalculate:
            return self.game_ended

        # assume that:
        self.game_ended = False
        self.draw = False
        self.winner = None

        # set fields / check if assumptions were right
        self._game_ended_row_check()
        self._game_ended_column_check()
        self._game_ended_diagonal_check()
        self._draw_check()

        return self.game_ended

    def _draw_check(self):
        if np.all(self.board != 0):
            self.draw = True
            self.game_ended = True
            self.winner = None

    def _game_ended_diagonal_check(self):
        for player_number in (1, 2):
            #left to right
            for row in range(self.rows - 2):
                in_a_diagonal_count = 0
                for column in range(self.columns - 2):

                    if self.board[row, column] == player_number:
                        in_a_diagonal_count += 1
                    if self.board[row + 1, column + 1] == player_number:
                        in_a_diagonal_count += 1
                    if self.board[row + 2, column + 2] == player_number:
                        in_a_diagonal_count += 1

                    if in_a_diagonal_count == 3:
                        self.winner = player_number
                        self.game_ended = True

                    in_a_diagonal_count = 0

            # right to left
            for row in range(self.rows - 2):
                in_a_diagonal_count = 0
                for column in range(2, self.columns):

                    if self.board[row, column] == player_number:
                        in_a_diagonal_count += 1
                    if self.board[row + 1, column - 1] == player_number:
                        in_a_diagonal_count += 1
                    if self.board[row + 2, column - 2] == player_number:
                        in_a_diagonal_count += 1

                    if in_a_diagonal_count == 3:
                        self.winner = player_number
                        self.game_ended = True

                    in_a_diagonal_count = 0

        return self.game_ended

    def _game_ended_row_check(self):
        for player_number in (1, 2):
            for row in range(self.rows):
                in_a_row_count = 0
                for column in range(self.columns):
                    if self.board[row, column] == player_number:
                        in_a_row_count += 1

                    if in_a_row_count == 3:
                        self.winner = player_number
                        self.game_ended = True

        return self.game_ended

    def _game_ended_column_check(self):
        for player_number in (1, 2):
            for column in range(self.columns):
                in_a_column_count = 0
                for row in range(self.rows):
                    if self.board[row, column] == player_number:
                        in_a_column_count += 1

                    if in_a_column_count == 3:
                        self.winner = player_number
                        self.game_ended = True

        return self.game_ended

    def is_draw(self):
        return np.all(self.board != 0)

    def set_x(self, row, column):
        self.board[row, column] = 1

    def set_o(self, row, column):
        self.board[row, column] = 2

    def print_array(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                value = self.board[row][column]
                if value == 0:
                    print('.', end=" ")
                elif value == 1:
                    print('x', end=" ")
                elif value == 2:
                    print('o', end=" ")
            print()