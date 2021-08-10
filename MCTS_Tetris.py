from Client_Tetris import print_board, reset, get_score, get_tempscore, reset_temp
from dual_network import DN_INPUT_SHAPE
from math import sqrt
import tensorflow as tf
from tensorflow.keras.models import load_model
from pathlib import Path
import numpy as np
import math

RECUR_COUNT = 0
PV_EVALUATE_COUNT = 500 #추론 1회당 시뮬레이션 횟수

def predict(model, state) : 
    a, b, c = DN_INPUT_SHAPE
    x = state.board
    x = tf.expand_dims(x,-1)
    x = tf.expand_dims(x,0)

    y = model.predict(x, batch_size = 1)
    #print("\n\ny : ", y)

    policies = []
    for i in range(len(state.legal_action())) : 
        policies.append(y[0][0][i])
    sum_p = sum(policies) if sum(policies) else 1
    for i in range(len(policies)) : 
        policies[i] /= sum_p
    #print("\n\npolicies : ", policies)

    value = y[1][0][0] 
    return policies, value

def nodes_to_scores(nodes) : #노드의 시행 횟수를 리스트로 반환
    scores = []
    for c in nodes : 
        scores.append(c.n)
    #print("scores : ", scores)
    return scores

def pv_mcts_scores(model, state, temperature) : 
    class Node : 
        def __init__(self, state, p) : 
            self.state = state
            self.p = p
            self.w = 0
            self.n = 0
            self.child_nodes = None
        
        def evaluate(self) : 
            global RECUR_COUNT
            #print("RECUR_COUNT : ", RECUR_COUNT)
            if self.state.is_done() : 
                value = get_tempscore() if self.state.is_done() else -1
                value -= 20

                print("SIMULATION SCORE : ", get_tempscore())

                self.w += value
                self.n += 1
                reset_temp()
                return value
            
            if not self.child_nodes : 
                policies, value = predict(model, self.state)
                self.w += value
                self.n += 1

                self.child_nodes = []
                for action, policy in zip(self.state.legal_action(), policies) : 
                    self.child_nodes.append(Node(self.state.test(action), policy))
                #print("SCORE : ", get_tempscore())
                reset_temp()
                #print('==========================================')
                return value
            
            else :
                RECUR_COUNT += 1
                value = self.next_child_node().evaluate()
                self.w += value
                self.n += 1
                return value

        def next_child_node(self) : 
            C_PUCT = 1.0
            t = sum(nodes_to_scores(self.child_nodes))
            pucb_values = []
            #print("child_node.w / child_node.n : ", end = ' ')
            for child_node in self.child_nodes : 
                pucb_values.append((child_node.w / child_node.n if child_node.n else 0.0) + C_PUCT * child_node.p * sqrt(t) / (1 + child_node.n))
                #print(child_node.w / child_node.n if child_node.n else 0.0, end = ' / ')
            #print('')

            #print("pucb_values : ", pucb_values)
            self.state.test(self.state.legal_action()[np.argmax(pucb_values)])
            return self.child_nodes[np.argmax(pucb_values)]
            
            
    
    root_node = Node(state, 0)

    reset()
    reset_temp()
    for i in range(PV_EVALUATE_COUNT) : 
        global RECUR_COUNT
        RECUR_COUNT = 0
        root_node.evaluate()
        if i % 50 == 0 :  print("i : ", i)
    scores = nodes_to_scores(root_node.child_nodes)
    if temperature == 0 : 
        action = np.argmax(scores)
        scores = np.zeros(len(scores))
        scores[action] = 1
    else : 
        scores = boltzman(scores, temperature)
    return scores

def pv_mcts_action(model, temperature = 0) : 
    def pv_mcts_action(state) : 
        scores = pv_mcts_scores(model, state, temperature)
        return np.random.choice(state.legal_action(), p = scores)

    return pv_mcts_action

def boltzman(xs, temperature) : 
    xs = [x ** (1/temperature) for x in xs]
    return [x / sum(xs) for x in xs]