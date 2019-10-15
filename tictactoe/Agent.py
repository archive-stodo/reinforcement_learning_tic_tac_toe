import numpy as np

class Agent:

    def __init__(self, player_number, eps=0.1, alpha=0.2):
        self.eps = eps
        self.alpha = alpha # learning rate
        self.verbose = False
        self.state_history = []
        self.state_values = []
        self.player_number = player_number

        self.points = [(0, 0)] # 1 for win, 0.5 for draw

    def reset_history(self):
        self.state_history = []

    def set_state_values(self, state_values_indexed_with_state_number):
        self.state_values = state_values_indexed_with_state_number

    def set_player_number(self, player_number):
        if player_number not in (1, 2):
            raise ValueError()
        else:
            self.player_number = player_number

    def take_action(self, env):
        r = np.random.rand()
        move = None

        if r < self.eps:
            # random action
            if self.verbose:
                print("Taking a random action")

            possible_moves = self.get_possible_moves(env)

            move_id = np.random.choice(len(possible_moves))
            move = possible_moves[move_id]

        else:
            if self.verbose:
                print("Taking a greedy action")

            #choose best action
            possible_moves = self.get_possible_moves(env)

            tried_move_state_max_value = -999
            tried_move_with_max_state_value = None
            for possible_move in possible_moves:
                # get value of this state number
                tried_move_state_value = self.get_move_state_value(env, possible_move)

                if tried_move_state_value > tried_move_state_max_value:
                    tried_move_with_max_state_value = possible_move
                    tried_move_state_max_value = tried_move_state_value

            move = tried_move_with_max_state_value

        #do the move eventually
        env.board[move] = self.player_number
        # env.print_array(env.board)

    def get_possible_moves(self, env):
        possible_moves = []
        for i in range(env.rows):
            for j in range(env.columns):
                if env.board[i, j] == 0:
                    possible_moves.append((i, j))
        return possible_moves

    def update_state_history(self, state_number):
        self.state_history.append(state_number)

    def update_state_values(self, env):
        # 1 - agent won | 0 - otherwise
        reward = env.reward(self.player_number)
        target = reward

        #start updating with the latest state
        for previous_state in reversed(self.state_history):
            # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state))
            previous_state_value = self.state_values[previous_state] + self.alpha*(target - self.state_values[previous_state])
            self.state_values[previous_state] = previous_state_value
            target = previous_state_value

        # when we are done updating state values
        self.reset_history()

    def get_move_state_value(self, env, move):
        # make a move
        env.board[move] = self.player_number

        move_state_number = env.get_state_number(env.board)
        move_state_value = self.state_values[move_state_number]

        # redo move
        env.board[move] = 0

        return move_state_value

    def get_possible_move_state_values_board(self, env, change_player_numbers_to_symbols=True):
        copied_board = env.board.astype(str)

        if change_player_numbers_to_symbols:
            copied_board[ copied_board == '1'] = 'x'
            copied_board[copied_board == '2'] = 'o'

        possible_moves = self.get_possible_moves(env)
        for possible_move in possible_moves:
            copied_board[possible_move[0], possible_move[1]] = self.get_move_state_value(env, possible_move)

        return copied_board







