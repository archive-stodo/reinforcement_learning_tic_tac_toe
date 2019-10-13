from tictactoe.Agent import Agent
from tictactoe.Environment import Environment
import numpy as np

# inefficient (calculation for impossible board positions) but works.
from tictactoe.Human import Human


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

    env.state_number_winner_ended_triple = number_winner_ended

    return number_winner_ended


def initialV_x(env, state_winner_ended_triples):
    state_values = np.zeros(env.num_states)

    for state, winner, ended in state_winner_ended_triples:
        if ended:
            if winner == 1:
                state_value = 1
            else:
                state_value = 0.5
        state_value = 0.5
        state_values[state] = state_value

    return state_values


def initialV_o(env, state_winner_ended_triples):
    state_values = np.zeros(env.num_states)

    for state, winner, ended in state_winner_ended_triples:
        if ended:
            if winner == 0:
                state_value = 1
            else:
                state_value = 0.5
        state_value = 0.5
        state_values[state] = state_value

    return state_values


def play_game(p1, p2, env, draw=False):
    current_player = p1

    while not env.check_game_ended(force_recalculate=True):
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if draw:
            if draw == 1 and current_player == p1:
                env.print_array(env.board)
            if draw == 2 and current_player == p2:
                env.print_array(env.board)

        #current player makes a move
        current_player.take_action(env)

        # update state history
        state = env.get_state_number()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.print_array(env.board)

    # update the value function
    p1.update_state_values(env)
    p2.update_state_values(env)

# ----------------------------------------------------

# train the agent
p1 = Agent(player_number=1) # player x
p2 = Agent(player_number=2) # player o

# set initial state values for both players
env = Environment(3, 3)
state_winner_triples = get_state_number_winner_ended_triple(env, verbose_lvl=0)

Vx = initialV_x(env, state_winner_triples)
p1.set_state_values(Vx)

Vo = initialV_o(env, state_winner_triples)
p2.set_state_values(Vo)

number_of_games_to_be_played = 10000
for game_nr in range(number_of_games_to_be_played):
    if game_nr % 200 == 0:
        print(f'game number: {game_nr}')
    play_game(p1, p2, env)

# play human vs. agent
# do you think the agent learned to play the game well?
human = Human()
human.set_symbol(2)

while True:
    p1.verbose = True
    play_game(p1, human, env, draw=True)
    # I made the agent player 1 because I wanted to see if it would
    # select the center as its starting move. If you want the agent
    # to go second you can switch the human and AI.
    # answer = input("Play again? [Y/n]: ")
    # if answer and answer.lower()[0] == 'n':
    #   break