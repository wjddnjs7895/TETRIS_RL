from Client_Tetris import State, game_start, game_main_loop, SCORE, CURR_BLOCK, BOARD, game_end
from MCTS_Tetris import pv_mcts_scores
from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import tensorflow as tf
from pathlib import Path
import numpy as np
import pickle, os

SP_GAME_COUNT = 5
SP_TEMPERATURE = 1.0

def write_data(history) : 
    now = datetime.now()
    os.makedirs('./data/', exist_ok = True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode = 'wb') as f : 
        pickle.dump(history, f)

def play(model) :
    game_start()
    history = []
    
    state = State()
    '''
    state.board = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]])
    '''
    game_main_loop(BOARD)
    while True : 
        game_main_loop(BOARD)
        if state.is_done() : 
            print('================================SCORE================================')
            print("SCORE :", SCORE[0])
            print('')
            game_end()
            break

        scores = pv_mcts_scores(model, state, SP_TEMPERATURE)

        policies = [0] * DN_OUTPUT_SIZE
        for action, policy in zip(range(len(state.legal_action())), scores) : 
            policies[action] = policy
        history.append([state.board, policies, None])

        action = np.random.choice(len(state.legal_action()), p = scores)

        state = state.next(state.legal_action()[action])


    value = SCORE[0]
    for i in range(len(history)) : 
        history[i][2] = value
    return history

def self_play() : 
    history = []

    model = load_model('./model/best.h5')

    for i in range(SP_GAME_COUNT) : 
        h = play(model)
        history.extend(h)

        print('/rSelfPlay {}/{}'.format(i + 1, SP_GAME_COUNT), end = '')
    print('')

    write_data(history)

    K.clear_session()
    del model
    