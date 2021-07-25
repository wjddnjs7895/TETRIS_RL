from Client_Tetris import State
from MCTS_Tetris import pv_mcts_action
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np

EP_GAME_COUNT = 10

def play(next_actions) : 
    state = State()

    while True :
        if state.is_done() : 
            break
        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)

        state = state.next(action)
    return first_player_point(state)

def evaluate_algorithm_of(label, next_actions) : 
    total_point = 0
    for i in range(EP_GAME_COUNT) : 
        total_point += play(next_actions)

        print('/rEvaluate {}/{}'.format(i + 1, EP_GAME_COUNT), end = '')
    print('')

    average_point = total_point / EP_GAME_COUNT
    print(label, average_point)

def evaluate_best_player() : 
    model = load_model('./model/best.h5')

    next_pv_mcts_action = pv_mcts_action(model, 0.0)

    next_actions = (next_pv_mcts_action, random_action)
    evaluate_algorithm_of('VS_Random', next_actions)

    next_actions = (next_pv_mcts_action, alpha_beta_action)
    evaluate_algorithm_of('VS_MCTS', next_actions)

    K.clear_Session()
    del model