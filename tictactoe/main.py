from tictactoe.Agent import Agent
from tictactoe.Environment import Environment
import numpy as np
import matplotlib.pyplot as plt

# inefficient (calculation for impossible board positions) but works.
from tictactoe.Human import Human

# inspired by:
# https://github.com/lazyprogrammer/machine_learning_examples/blob/master/rl/tic_tac_toe.py

def get_state_number_winner_ended_triple(env, verbose_lvl=2):
    number_winner_ended = []
    for state_number in range(env.num_states):
        board = env.get_board_from_state_number(state_number, print_board=False)
        env.board = board
        env.check_game_ended(force_recalculate=True)
        number_winner_ended.append((state_number, env.game_ended, env.winner))

        if verbose_lvl == 1:
            if state_number % 500 == 0:
                print(f"state {state_number + 1} out of {env.num_states}. {round((state_number + 1) * 100 / env.num_states, 1)} % done")
        if verbose_lvl == 2:
            if state_number % 500 == 0:
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
            state_values[state] = state_value

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

            state_values[state] = state_value

        state_value = 0.5
        state_values[state] = state_value

    return state_values


def play_game(p1, p2, env, draw=False, draw_state_values=False):
    # choose player starting the game randomly
    current_player = None
    if np.random.rand() < 0.5:
        current_player = p1
    else:
        current_player = p2

    while not env.check_game_ended(force_recalculate=True):
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if draw:
            env.print_array(env.board)
            if draw_state_values and isinstance(current_player, Agent):
                print('\n Computer possible move state values:')
                print(current_player.get_possible_move_state_values_board(env))
                print('\n -------------------------------------')

        # current player makes a move
        current_player.take_action(env)

        # update state history
        state = env.get_state_number(env.board)
        p1.update_state_history(state)
        p2.update_state_history(state)

    game_nr = len(p2.points)
    if isinstance(p1, Agent):
        if env.winner == p1.player_number:
            p1.points.append((game_nr, p1.points[-1][1] + 1))
        elif env.winner == p2.player_number:
            p1.points.append((game_nr, p1.points[-1][1]))
        else:
            p1.points.append((game_nr, p1.points[-1][1] + 0.5))

    if isinstance(p2, Agent):
        if env.winner == p2.player_number:
            p2.points.append((game_nr, p2.points[-1][1] + 1))
        elif env.winner == p1.player_number:
            p2.points.append((game_nr, p2.points[-1][1]))
        else:
            p2.points.append((game_nr, p2.points[game_nr - 1][1] + 0.5))

    if env.winner == p1.player_number and isinstance(p1, Human) or env.winner == p2.player_number and isinstance(p2, Human):
        print('Ghrrr! Watch your back human! Next time I will triumph! \n')

    if draw:
        env.print_array(env.board)

    # update the value function
    p1.update_state_values(env)
    p2.update_state_values(env)

    # finally
    env.clear_board()

# ----------------------------------------------------
env = Environment(3, 4)
p1 = Agent(player_number=1)  # player x
p1.eps = 0.2
p1.alpha = 0.2

p2 = Agent(player_number=2)  # player o
p2.eps = 0.2
p2.alpha = 0.2

# set initial state values for both players
state_winner_triples = get_state_number_winner_ended_triple(env, verbose_lvl=1)
env.state_number_winner_ended_triple = state_winner_triples

Vx = initialV_x(env, state_winner_triples)
p1.set_state_values(Vx)

Vo = initialV_o(env, state_winner_triples)
p2.set_state_values(Vo)

number_of_games_to_be_played = 2500
for game_nr in range(number_of_games_to_be_played):
    if game_nr % 100 == 0:
        print(f'game number: {game_nr}')
    play_game(p1, p2, env, draw=False)

game_nr1, points1 = zip(*p1.points)
game_nr2, points2 = zip(*p2.points)

plt.plot(game_nr1, points1, label=f'p1. eps: {p1.eps}, alpha: {p1.alpha}')
plt.plot(game_nr2, points2, label=f'p2. eps: {p2.eps}, alpha: {p2.alpha}')
plt.legend()
plt.xlabel('Game Number')
plt.ylabel('Points')
plt.show()

# Print initial state values for both trained computer-agents
# print('p2: \n', p2.get_possible_move_state_values_board(env))
# print('p1: \n', p1.get_possible_move_state_values_board(env))

human = Human()
human.set_symbol(2)
while True:
    # show if greedy action or exploration chosen?
    p1.verbose = True

    play_game(human, p1, env, draw=True, draw_state_values=True)

    answer = input("Dare to challenge me you carbon-based life form? [y/n]: ")
    if answer and answer.lower()[0] == 'n':
        break
