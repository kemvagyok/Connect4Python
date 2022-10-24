from typing import List

from board import Board

import numpy as np

class Node:
    def __init__(self, value=None, board=None, depth = None, col = None):
        self.MAX = float('inf')
        self.MIN = -float('inf')
        self.depth = depth
        self.board = board
        self.children = []
        self.col = col
        self.value = None

    def build(self, depth : int, maxDepth : int, actual_player_index : int, other_player_index: int, board: Board):
            depth=depth+1
            if(depth<maxDepth):
                if(board.get_winner()==None):
                    for col in board.get_valid_steps():
                        newBoard = board.copy()
                        newBoard.step(actual_player_index,col)
                        newNode = Node(board = newBoard, depth=depth, col = col)
                        newNode.build(depth,maxDepth,other_player_index,actual_player_index,newBoard)
                        self.children.append(newNode)

    def miniMaxSearch(self) -> int:
            self.value = self.maxValue(-float('inf'), float('inf'))

    def maxValue(self, alpha, beta) -> int:
        value = self.MIN
        if (len(self.children)==0):
            return self.evaluate()
        value = self.MIN
        for child in self.children:
            value = max(value, child.minValue(alpha, beta))
            if value >= beta:
                break
            alpha = max(alpha, value)
        self.value = value
        return value

    def minValue(self, alpha, beta) -> int:
        if (len(self.children)==0):
            return self.evaluate()
        value = self.MAX
        for child in self.children:
            value = min(value, child.maxValue(alpha, beta))
            if value <= alpha:
                break
            beta = min(beta, value)
        self.value = value
        return value

    def evaluate(self) -> int:
        state = self.board.get_state()
        if self.board.get_last_player_index() == 1:
            o_color = 2
        elif self.board.get_last_player_index() == 2:
            o_color = 1
        #my_fours = self.checkForStreak(state, 1, 4)
        my_threes = self.checkForStreak(state, 1, 3)
        my_twos = self.checkForStreak(state, 1, 2)
        #comp_fours = self.checkForStreak(state, 2, 4)
        comp_threes = self.checkForStreak(state, 2, 3)
        comp_twos = self.checkForStreak(state, 2, 2)
        return (my_threes * 5+ my_twos*2) - (comp_threes * 5 + comp_twos*2)

    def checkForStreak(self, state, color, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalStreak(i, j, state, streak)
                    count += self.horizontalStreak(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    def verticalStreak(self, row, column, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, column, state, streak):
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, state, streak):
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

class StudentPlayer:
    def __init__(self, player_index: int, board_size: List[int], n_to_connect: int):
        self.__n_to_connect = n_to_connect
        self.__board_size = board_size
        self.__player_index = player_index
        self.__board = Board(self.__board_size, self.__n_to_connect)

    def step(self, last_player_col: int) -> int:
        self.__board.step(2,last_player_col)
        # if last_player_col != -1:
            #self.__board.step(self._other_player_index, last_player_col)

        root = Node(depth=0,board = self.__board)
        root.build(0, 3, 1, 2, self.__board)

        root.miniMaxSearch()

        maxIndex = 0
        for index in range(1, len(root.children)):
            if(root.children[index].value != None):
                if(root.children[maxIndex].value < root.children[index].value):
                    maxIndex = index
        col = root.children[maxIndex].col# your logic here
        self.__board.step(self.__player_index,col)
        return col

asd = StudentPlayer(1,[6,7],4)
asd.step(1)
asd.step(1)
asd.step(1)


