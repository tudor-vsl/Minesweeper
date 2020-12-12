import random as rand
import numpy as np
from Minesweeper.Project.mine_board import *


class Board:

    def __init__(self, rows, cols, no_of_bombs, main_matrix):
        self.rows = rows
        self.cols = cols
        self.no_of_bombs = no_of_bombs
        self.main_matrix = main_matrix
        self.coord_list = []

    def place_bombs(self):
        i = 0;
        while i < self.no_of_bombs:
            rand_x = rand.randint(0, self.rows - 1)
            rand_y = rand.randint(0, self.cols - 1)
            if (rand_x, rand_y) not in self.coord_list:
                self.main_matrix[rand_x][rand_y] = 9
                self.coord_list.append((rand_x, rand_y))
                i += 1
        print("Nr de bombe este: ", len(self.coord_list))
        print("Lista bombe: ", self.coord_list)

    @staticmethod
    def padding(aux_matrix, x, y):
        if aux_matrix[x - 1][y - 1] != 9:
            aux_matrix[x - 1][y - 1] += 1
        if aux_matrix[x - 1][y] != 9:
            aux_matrix[x - 1][y] += 1
        if aux_matrix[x - 1][y + 1] != 9:
            aux_matrix[x - 1][y + 1] += 1

        if aux_matrix[x][y - 1] != 9:
            aux_matrix[x][y - 1] += 1
        if aux_matrix[x][y] != 9:
            aux_matrix[x][y] += 1
        if aux_matrix[x][y + 1] != 9:
            aux_matrix[x][y + 1] += 1

        if aux_matrix[x + 1][y - 1] != 9:
            aux_matrix[x + 1][y - 1] += 1
        if aux_matrix[x + 1][y] != 9:
            aux_matrix[x + 1][y] += 1
        if aux_matrix[x + 1][y + 1] != 9:
            aux_matrix[x + 1][y + 1] += 1

    def place_numbers(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.main_matrix[i][j] == 9:
                    self.padding(self.main_matrix, i, j)

    def print_matrix(self):
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                print(self.main_matrix[i][j], end=" ")
            print()

"""matrix = np.zeros((100,100),dtype=int)
test = Board(13,14,25,matrix)
test.place_bombs()
test.place_numbers()
test.print_matrix()"""





