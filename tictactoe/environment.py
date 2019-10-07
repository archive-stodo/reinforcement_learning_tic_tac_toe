import numpy as np

class Environment:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns), int)
        self.winner = None
        self.ended = False
        self.num_states = 3**(rows*columns)

    def reward(self, player_symbol):
        pass

    def initialV_x(env, state_winner_triples):
        pass

    def initialV_o(env, state_winner_triples):
        pass

    def is_game_over(self):
        pass

    def is_draw(self):
        pass

    def set_x(self, row, column):
        self.board[row, column] = -1

    def set_o(self, row, column):
        self.board[row, column] = 1

    def print_array(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                value = self.board[row][column]
                if value == 0:
                    print('.', end=" ")
                elif value == -1:
                    print('x', end=" ")
                elif value == 1:
                    print('o', end=" ")
            print()