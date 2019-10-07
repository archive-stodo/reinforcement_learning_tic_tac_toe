from tictactoe.environment import Environment

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