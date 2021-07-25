import random

WIDTH = 10
HEIGHT = 20
#                 0          1          2          3         4          5          6   
BLOCKS_IDX = ['BLOCK_I', 'BLOCK_O', 'BLOCK_Z', 'BLOCK_S', 'BLOCK_J', 'BLOCK_L', 'BLOCK_T']
CW_SRS = [
    [[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]],
    [[0,0],[-1,0],[-1,-1],[0,2],[-1,2]],
    [[0,0],[1,0],[1,1],[0,-2],[1,-2]],
    [[0,0],[1,0],[1,-1],[0,2],[1,2]]
    ]
CCW_SRS = [
    [[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]],
    [[0,0],[1,0],[1,1],[0,2],[1,2]],
    [[0,0],[1,0],[1,1],[0,-2],[1,-2]],
    [[0,0],[-1,0],[-1,1],[0,2],[-1,2]]
    ]

class BLOCK : 
    def __init__(self) : 
        self.locX = 4      #LEFT_TOP
        self.locY = 0
        self.type = 0 #블록 타입 첫번째 모양으로 고정
        #self.type = random.randrange(0,4)

    def rotate(self, dir, board, shape_lst) : 
        if dir == 1 : #CW
            if self.type == 0 : 
                temp = 3
            else:
                temp = self.type - 1
            for i in range(5) : 
                if not self.check_block_collision(shape_lst[temp], self.locX + CCW_SRS[self.type][i][0], self.locY + CCW_SRS[self.type][i][1],board) and not self.check_wall_collision(shape_lst[temp], self.locX + CCW_SRS[self.type][i][0], self.locY + CCW_SRS[self.type][i][1]) : 
                    self.locX += CCW_SRS[self.type][i][0]
                    self.locY += CCW_SRS[self.type][i][1]
                    self.type = temp
                    self.shape = self.shape_lst[self.type]
                    break
        else :  #CCW
            if self.type == 3 : 
                temp = 0
            else : 
                temp = self.type + 1
            for i in range(5) : 
                if not self.check_block_collision(shape_lst[temp], self.locX + CW_SRS[self.type][i][0], self.locY + CW_SRS[self.type][i][1],board) and not self.check_wall_collision(shape_lst[temp], self.locX + CW_SRS[self.type][i][0], self.locY + CW_SRS[self.type][i][1]) :
                    self.locX += CW_SRS[self.type][i][0]
                    self.locY += CW_SRS[self.type][i][1]
                    self.type = temp
                    self.shape = self.shape_lst[self.type]
                    break

    def soft_drop(self, shape, board) : 
        if not self.check_block_collision(shape, self.locX, self.locY+1, board) : 
            self.locY += 1

    def hard_drop(self, shape, board) :
        while not self.check_block_collision(shape, self.locX, self.locY+1, board) : 
            self.locY += 1

    def moveX(self, shape, dir, board) : 
        DX = [-1, 1]
        if not self.check_block_collision(shape, self.locX + DX[dir], self.locY, board) and not self.check_wall_collision(shape, self.locX + DX[dir], self.locY): 
            self.locX += DX[dir]

    def guide_block(self, shape, board) : 
        tempX = self.locX
        tempY = self.locY
        while True : 
            if self.check_block_collision(shape, tempX, tempY, board) : 
                break
            tempY += 1
        return tempY - self.locY - 1

    def check_block_collision(self, shape, tempX, tempY, board) : 
        for x in range(4) : 
            for y in range(4) : 
                if shape[x*4 + y] :
                    try : 
                        if board[tempX + x][tempY + y]  or tempY + y >= HEIGHT: 
                            return True  
                    except : 
                        return True
        return False

    def check_wall_collision(self, shape, tempX, tempY) : 
        for x in range(4) : 
            for y in range(4) : 
                if shape[x*4 + y] :
                    if tempX + x < 0 or tempX + x >= WIDTH : 
                        return True
        return False

class MINO_I(BLOCK) : 
    def __init__(self) : 
        super().__init__()
        self.color = 'skyblue'
        self.idx = 1
        self.shape_lst = [
            [0,0,0,0,
            1,1,1,1,
            0,0,0,0,
            0,0,0,0],
            
            [0,0,1,0,
            0,0,1,0,
            0,0,1,0,
            0,0,1,0],

            [0,0,0,0,
            0,0,0,0,
            1,1,1,1,
            0,0,0,0],   

            [0,1,0,0,
            0,1,0,0,
            0,1,0,0,
            0,1,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]] #17개
        self.shape = self.shape_lst[self.type]

class MINO_O(BLOCK) : 
    def __init__(self)  :
        super().__init__()
        self.color = 'yellow'
        self.idx = 2
        self.shape_lst = [
            [0,0,0,0,
            0,0,0,0,
            0,1,1,0,
            0,1,1,0],
            
            [0,0,0,0,
            0,0,0,0,
            0,1,1,0,
            0,1,1,0],
            
            [0,0,0,0,
            0,0,0,0,
            0,1,1,0,
            0,1,1,0],
            
            [0,0,0,0,
            0,0,0,0,
            0,1,1,0,
            0,1,1,0]]
        self.legal_action = [[0, -1], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]] #9개
        self.shape = self.shape_lst[self.type]

class MINO_Z(BLOCK) : 
    def __init__(self) :
        super().__init__() 
        self.color = 'red'
        self.idx = 3
        self.shape_lst = [
            [0,0,0,0,
            1,1,0,0,
            0,1,1,0,
            0,0,0,0],
            
            [0,0,0,0,
            0,0,1,0,
            0,1,1,0,
            0,1,0,0],
            
            [0,0,0,0,
            0,0,0,0,
            1,1,0,0,
            0,1,1,0],
            
            [0,0,0,0,
            0,1,0,0,
            1,1,0,0,
            1,0,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]] #17개
        self.shape = self.shape_lst[self.type]

class MINO_S(BLOCK) : 
    def __init__(self) : 
        super().__init__()
        self.color = 'green'
        self.idx = 4
        self.shape_lst = [
            [0,0,0,0,
            0,1,1,0,
            1,1,0,0,
            0,0,0,0],
            
            [0,0,0,0,
            0,1,0,0,
            0,1,1,0,
            0,0,1,0],
            
            [0,0,0,0,
            0,0,0,0,
            0,1,1,0,
            1,1,0,0],
            
            [0,0,0,0,
            1,0,0,0,
            1,1,0,0,
            0,1,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]] #17개
        self.shape = self.shape_lst[self.type]

class MINO_J(BLOCK) : 
    def __init__(self) :
        super().__init__()
        self.color = 'blue'
        self.idx = 5
        self.shape_lst = [
            [0,0,0,0,
            1,0,0,0,
            1,1,1,0,
            0,0,0,0],
            
            [0,0,0,0,
            0,1,1,0,
            0,1,0,0,
            0,1,0,0],
            
            [0,0,0,0,
            0,0,0,0,
            1,1,1,0,
            0,0,1,0],
            
            [0,0,0,0,
            0,1,0,0,
            0,1,0,0,
            1,1,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], 
                             [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]] #34개
        self.shape = self.shape_lst[self.type]

class MINO_L(BLOCK) : 
    def __init__(self) :
        super().__init__()
        self.color = 'orange'
        self.idx = 6
        self.shape_lst = [
            [0,0,0,0,
            0,0,1,0,
            1,1,1,0,
            0,0,0,0],
            
            [0,0,0,0,
            0,1,0,0,
            0,1,0,0,
            0,1,1,0],
            
            [0,0,0,0,
            0,0,0,0,
            1,1,1,0,
            1,0,0,0],
            
            [0,0,0,0,
            1,1,0,0,
            0,1,0,0,
            0,1,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], 
                             [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]] #34개
        self.shape = self.shape_lst[self.type]

class MINO_T(BLOCK) : 
    def __init__(self) : 
        super().__init__()
        self.color = 'purple'
        self.idx = 7
        self.shape_lst = [
            [0,0,0,0,
            0,1,0,0,
            1,1,1,0,
            0,0,0,0],
            
            [0,0,0,0,
            0,1,0,0,
            0,1,1,0,
            0,1,0,0],
            
            [0,0,0,0,
            0,0,0,0,
            1,1,1,0,
            0,1,0,0],
            
            [0,0,0,0,
            0,1,0,0,
            1,1,0,0,
            0,1,0,0]]
        self.legal_action = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, -1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], 
                             [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]] #34개
        self.shape = self.shape_lst[self.type]
