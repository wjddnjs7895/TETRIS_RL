import numpy as np
import pygame, sys, random, time
from BLOCKS import *
from pygame.locals import *


def State() : 
    class State :
        def __init__(self) : 
            self.board = BOARD

        def is_done(self) : 
            return check_end(self.board)

        def next(self, action) : 
            global CURR_BLOCK
            global BOARD
            CURR_BLOCK.shape = CURR_BLOCK.shape_lst[action[0]]
            CURR_BLOCK.locX = action[1]
            CURR_BLOCK.hard_drop(CURR_BLOCK.shape,BOARD)
            print(CURR_BLOCK.shape)
            if CURR_BLOCK.check_block_collision(CURR_BLOCK.shape, CURR_BLOCK.locX, CURR_BLOCK.locY+1, BOARD) : 
                for x in range(4) : 
                    for y in range(4) : 
                        if CURR_BLOCK.shape[y * 4 + x] : 
                            print(y * 4 + x)
                            print(x)
                            print(y)
                            print(CURR_BLOCK.locX)
                            print('---------------------------------')
                            BOARD[CURR_BLOCK.locX + x][CURR_BLOCK.locY + y] = CURR_BLOCK.idx
                CURR_BLOCK = None
                block_generator()
            return State()

        def legal_action(self) : 
            global CURR_BLOCK
            return CURR_BLOCK.legal_action
    return State()

def block_select(shape) :
    if shape == 0 : return MINO_I()
    elif shape == 1 : return MINO_O()
    elif shape == 2 : return MINO_Z()
    elif shape == 3 : return MINO_S()
    elif shape == 4 : return MINO_J()
    elif shape == 5 : return MINO_L()
    else : return MINO_T()

def line_erase(board) :
    global SCORE
    t_board = list(np.transpose(board))
    result_board = []
    erase_count = 0

    for y in range(HEIGHT) :
        flag = 1
        for x in range(WIDTH) :  
            if not t_board[y][x]: 
                flag = 0
                break
        if flag : erase_count += 1
        else : result_board.append(t_board[y])
    for _ in range(erase_count) : 
        result_board.insert(0,[0,0,0,0,0,0,0,0,0,0])
    SCORE += erase_count * 10 * erase_count
    return np.transpose(np.array(result_board))
            

def random_generator() : 
    idx_lst = [0,1,2,3,4,5,6]
    #random.shuffle(idx_lst) 강화학습의 난이도를 낮추기 위해 블럭 순서 고정
    return idx_lst

def block_generator() : 
    global CURR_BLOCK
    global block_lst

    if len(block_lst) <= 7 : 
        block_lst += random_generator()

    if not CURR_BLOCK : 
        CURR_BLOCK = block_select(block_lst[0])
        del block_lst[0]
    
def block_change() : 
    global limit
    global CURR_BLOCK
    if CURR_BLOCK.check_block_collision(CURR_BLOCK.shape, CURR_BLOCK.locX, CURR_BLOCK.locY+1, BOARD) : 
        for x in range(4) : 
            for y in range(4) : 
                if CURR_BLOCK.shape[x * 4 + y] : 
                    BOARD[CURR_BLOCK.locX + x][CURR_BLOCK.locY + y] = CURR_BLOCK.idx
        CURR_BLOCK = None
        block_generator()

def block_hold() :
    global CURR_BLOCK
    global HOLD_BLOCK
    if HOLD_BLOCK : 
        temp = CURR_BLOCK
        CURR_BLOCK = HOLD_BLOCK
        HOLD_BLOCK = temp
    else : 
        HOLD_BLOCK = CURR_BLOCK
        CURR_BLOCK = None
        block_generator()

def block_move(flag) : 
    if flag[0] : 
        CURR_BLOCK.soft_drop(CURR_BLOCK.shape,BOARD)
    if flag[1] :
        CURR_BLOCK.moveX(CURR_BLOCK.shape, 0, BOARD)
    if flag[2] :        
        CURR_BLOCK.moveX(CURR_BLOCK.shape, 1, BOARD)

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

def check_end(board) :
    for i in range(10) : 
        if board[i][1] : 
            return True
    return False

def game_end() : 
    global BOARD
    global SCORE
    for x in range(10) : 
        for y in range(20) : 
            BOARD[x][y] = 0
    SCORE = 0
    game_main_loop()

def game_start() :
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, GAME_SPEED)
    time.sleep(2)

def game_main_loop() : 
    global counter
    global limit
    global CURR_BLOCK
    global HOLD_BLOCK
    global BOARD
    global rotating
    MOVE_SPEED = 1
    #time.sleep(0.05)
    WINDOWWIDTH = 1400
    WINDOWHEIGHT = 1160
    BLOCK_SIZE = 36
    FLAW_SIZE = 200
    START_X = 156 + FLAW_SIZE
    START_Y = 50 + FLAW_SIZE
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('TETRIS')


    top_layer = pygame.image.load("resources/top_layer.png")
    bottom_layer = pygame.image.load("resources/bottom_layer.png")
    left_layer = pygame.image.load("resources/left_layer.png")
    right_layer = pygame.image.load("resources/right_layer.png")
    inside_layer = pygame.image.load("resources/inside_layer.png")
    back_ground = pygame.image.load("resources/back_ground.png")
    inside_back_ground = pygame.image.load("resources/inside_back_ground.png")
    hold_background = pygame.image.load("resources/hold_background.png")
    next_background = pygame.image.load("resources/next_background.png")
    small_next_background = pygame.image.load("resources/small_next_background.png")
    guide_block = pygame.image.load("resources/guide_block.png")

    block_colors_dic = {
        'block_blue' : pygame.image.load("resources/block_blue.png"), #MINO_J
        'block_purple' : pygame.image.load("resources/block_purple.png"), #MINO_T
        'block_skyblue' : pygame.image.load("resources/block_skyblue.png"), #MINO_I
        'block_red' : pygame.image.load("resources/block_red.png"), #MINO_Z
        'block_orange' : pygame.image.load("resources/block_orange.png"), #MINO_L
        'block_yellow' : pygame.image.load("resources/block_yellow.png"), #MINO_O
        'block_green' : pygame.image.load("resources/block_green.png") #MINO_S
    }
    back_ground = pygame.transform.scale(back_ground,(2000,1160))
    inside_back_ground = pygame.transform.scale(inside_back_ground,(360,720))
    windowSurface.blit(back_ground, [0, 0])
    windowSurface.blit(inside_back_ground, [START_X, START_Y])
    windowSurface.blit(inside_layer, [START_X, START_Y])
    windowSurface.blit(hold_background, [FLAW_SIZE + 16, FLAW_SIZE + 50])
    windowSurface.blit(next_background, [FLAW_SIZE + 550, FLAW_SIZE + 20])
    windowSurface.blit(small_next_background, [FLAW_SIZE + 550, FLAW_SIZE + 170])

    windowSurface.blit(top_layer, [FLAW_SIZE, FLAW_SIZE])
    windowSurface.blit(bottom_layer, [137 + FLAW_SIZE, 545 + FLAW_SIZE])
    windowSurface.blit(left_layer, [137 + FLAW_SIZE, 207 + FLAW_SIZE])
    windowSurface.blit(right_layer, [516 + FLAW_SIZE, 207 + FLAW_SIZE])

    block_generator()

    SPEED = 4
    MOVE_SPEED = SPEED / MOVE_SPEED
    if counter  %  MOVE_SPEED == 0 : 
        if limit and not rotating: 
            if CURR_BLOCK.check_block_collision(CURR_BLOCK.shape, CURR_BLOCK.locX, CURR_BLOCK.locY+1, BOARD) : 
                for x in range(4) : 
                    for y in range(4) : 
                        if CURR_BLOCK.shape[x * 4 + y] : 
                            BOARD[CURR_BLOCK.locX + x][CURR_BLOCK.locY + y] = CURR_BLOCK.idx
                CURR_BLOCK = None
                block_generator()
            CURR_BLOCK.locY += 1
            limit = 0

    if counter & 2 == 0 : 
        rotating = 0

    '''
    for event in pygame.event.get() : 
        if event.type == QUIT : 
            pygame.quit()
            sys.exit()
        if event.type == USEREVENT : 
            limit = 1
            counter = counter + 1 if counter < 100000000 else 0
        if event.type == KEYDOWN : 
            if event.key == K_z : 
                CURR_BLOCK.rotate(0, BOARD, CURR_BLOCK.shape_lst)
                rotating = 1
            if event.key == K_x : 
                CURR_BLOCK.rotate(1, BOARD, CURR_BLOCK.shape_lst)
                rotating = 1
            if event.key == K_c : 
                MOVE_FLAG[0] = 1
            if event.key == K_SPACE : 
                CURR_BLOCK.hard_drop(CURR_BLOCK.shape,BOARD)
                if CURR_BLOCK.check_block_collision(CURR_BLOCK.shape, CURR_BLOCK.locX, CURR_BLOCK.locY+1, BOARD) : 
                    for x in range(4) : 
                        for y in range(4) : 
                            if CURR_BLOCK.shape[x * 4 + y] : 
                                BOARD[CURR_BLOCK.locX + x][CURR_BLOCK.locY + y] = CURR_BLOCK.idx
                    CURR_BLOCK = None
                    block_generator()
            if event.key == K_DOWN : 
                MOVE_FLAG[0] = 1
            if event.key == K_LEFT : 
                MOVE_FLAG[1] = 1
            if event.key == K_RIGHT : 
                MOVE_FLAG[2] = 1
            if event.key == K_LSHIFT : 
                block_hold()
        if event.type == KEYUP : 
            if event.key == K_c : 
                MOVE_FLAG[0] = 0
            if event.key == K_DOWN : 
                MOVE_FLAG[0] = 0
            if event.key == K_LEFT : 
                MOVE_FLAG[1] = 0
            if event.key == K_RIGHT : 
                MOVE_FLAG[2] = 0


    block_move(MOVE_FLAG)
    '''
    BOARD = line_erase(BOARD)
    guideY = CURR_BLOCK.guide_block(CURR_BLOCK.shape, BOARD)
    
    for x in range(4) : 
        for y in range(4) : 
            if CURR_BLOCK.shape[x * 4 + y] : 
                blit_alpha(windowSurface, block_colors_dic['block_'+CURR_BLOCK.color], [START_X + BLOCK_SIZE * (CURR_BLOCK.locX +x) , START_Y + BLOCK_SIZE * (CURR_BLOCK.locY + y + guideY)], 50)
                blit_alpha(windowSurface, guide_block, [START_X + BLOCK_SIZE * (CURR_BLOCK.locX +x) , START_Y + BLOCK_SIZE * (CURR_BLOCK.locY + y + guideY)], 100)

    for x in range(4) : 
        for y in range(4) : 
            if CURR_BLOCK.shape[x * 4 + y] : 
                windowSurface.blit(block_colors_dic['block_'+CURR_BLOCK.color], [START_X + BLOCK_SIZE * (CURR_BLOCK.locX +x) , START_Y + BLOCK_SIZE * (CURR_BLOCK.locY + y)])

    for x in range(WIDTH) : 
        for y in range(HEIGHT) : 
            if BOARD[x][y] : 
                windowSurface.blit(block_colors_dic['block_'+BLOCKS_COLOR[int(BOARD[x][y]) - 1]], [START_X + BLOCK_SIZE * x , START_Y + BLOCK_SIZE * y])
    
    next_block_lst = [block_select(block_lst[0]), block_select(block_lst[1]), block_select(block_lst[2]), block_select(block_lst[3]), block_select(block_lst[4])]
    for i in range(len(next_block_lst)) :
        next0_block = pygame.image.load("resources/"+BLOCKS_IDX[next_block_lst[0].idx - 1]+".png")
        next1_block = pygame.image.load("resources/"+BLOCKS_IDX[next_block_lst[1].idx - 1]+".png")
        next2_block = pygame.image.load("resources/"+BLOCKS_IDX[next_block_lst[2].idx - 1]+".png")
        next3_block = pygame.image.load("resources/"+BLOCKS_IDX[next_block_lst[3].idx - 1]+".png")
        next4_block = pygame.image.load("resources/"+BLOCKS_IDX[next_block_lst[4].idx - 1]+".png")
        next0_block = pygame.transform.rotozoom(next0_block, 0, 0.8)
        next1_block = pygame.transform.rotozoom(next1_block, 0, 0.7)
        next2_block = pygame.transform.rotozoom(next2_block, 0, 0.7)
        next3_block = pygame.transform.rotozoom(next3_block, 0, 0.7)
        next4_block = pygame.transform.rotozoom(next4_block, 0, 0.7)

        windowSurface.blit(next0_block, [FLAW_SIZE + 559, FLAW_SIZE + 50])
        windowSurface.blit(next1_block, [FLAW_SIZE + 559, FLAW_SIZE + 65 + 100 * 1])
        windowSurface.blit(next2_block, [FLAW_SIZE + 559, FLAW_SIZE + 65 + 99 * 2])
        windowSurface.blit(next3_block, [FLAW_SIZE + 559, FLAW_SIZE + 65 + 99 * 3])
        windowSurface.blit(next4_block, [FLAW_SIZE + 559, FLAW_SIZE + 65 + 99 * 4])

        if HOLD_BLOCK : 
            holding_block = pygame.image.load("resources/"+BLOCKS_IDX[HOLD_BLOCK.idx - 1]+".png")
            holding_block = pygame.transform.rotozoom(holding_block, 0, 0.8)
            windowSurface.blit(holding_block, [FLAW_SIZE + 23, FLAW_SIZE + 70])
   
    if check_end(BOARD) : game_end()

    pygame.display.update()

#                 0          1          2          3         4          5          6   
BLOCKS_IDX = ['BLOCK_I', 'BLOCK_O', 'BLOCK_Z', 'BLOCK_S', 'BLOCK_J', 'BLOCK_L', 'BLOCK_T']
BLOCKS_COLOR = ['skyblue', 'yellow', 'red', 'green', 'blue', 'orange', 'purple']

CURR_BLOCK = None
HOLD_BLOCK = None
SCORE = 0
block_lst = []
WIDTH = 10
HEIGHT = 20
BOARD = np.zeros((WIDTH, HEIGHT))
MOVE_FLAG =[0, 0, 0] # down, left, right
GAME_SPEED = 100
counter = 0
limit = 1
rotating = 0

'''
BOARD = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,2,2],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,2,2],
[0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,7,0,3,3],
[0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,7,7,3,3,5],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,7,5,5,5],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,1,1,1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,2,2,6,6,6],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,4,6],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,4,4]])

#block_lst.append(7)

game_start()
while True : 
    game_main_loop()
'''