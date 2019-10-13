from tictactoe.environment import Environment

# inefficient (calculation for impossible board positions) but works.
def get_state_number_winner_ended_triple(env, verbose_lvl=2):
    number_winner_ended = []
    for state_number in range(env.num_states):
        board = env.get_board_from_state_number(state_number, print_board=False)
        env.board = board
        env.check_game_ended(force_recalculate=True)
        number_winner_ended.append((state_number, env.game_ended, env.winner))

        if verbose_lvl == 1:
            print(f"state {state_number + 1} out of {env.num_states}. {round((state_number + 1) * 100 / env.num_states, 1)} % done")
        if verbose_lvl == 2:
            env.print_array(board)
            print(number_winner_ended[-1])

    return number_winner_ended


def play_game(p1, p2, env, draw=False):
    current_player = None

    while not env.game_over():
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()

        #current player makes a move
        current_player.take_action(env)

        # update state history
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.draw_board()

    # update the value function
    p1.update(env)
    p2.update(env)