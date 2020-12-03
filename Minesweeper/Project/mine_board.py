import random as rand
import numpy as np


class Board:

    def __init__(self, rows, cols, no_of_bombs, main_matrix):
        self.rows = rows
        self.cols = cols
        self.no_of_bombs = no_of_bombs
        self.main_matrix = main_matrix

    def place_bombs(self):
        i = 0;
        coord_list = []
        while i < self.no_of_bombs:
            rand_x = rand.randint(0, self.rows - 1)
            rand_y = rand.randint(0, self.cols - 1)
            if (rand_x, rand_y) not in coord_list:
                self.main_matrix[rand_x][rand_y] = 8
                coord_list.append((rand_x, rand_y))
                i += 1

    @staticmethod
    def padding(aux_matrix, x, y):
        if aux_matrix[x - 1][y - 1] != 8:
            aux_matrix[x - 1][y - 1] += 1
        if aux_matrix[x - 1][y] != 8:
            aux_matrix[x - 1][y] += 1
        if aux_matrix[x - 1][y + 1] != 8:
            aux_matrix[x - 1][y + 1] += 1

        if aux_matrix[x][y - 1] != 8:
            aux_matrix[x][y - 1] += 1
        if aux_matrix[x][y] != 8:
            aux_matrix[x][y] += 1
        if aux_matrix[x][y + 1] != 8:
            aux_matrix[x][y + 1] += 1

        if aux_matrix[x + 1][y - 1] != 8:
            aux_matrix[x + 1][y - 1] += 1
        if aux_matrix[x + 1][y] != 8:
            aux_matrix[x + 1][y] += 1
        if aux_matrix[x + 1][y + 1] != 8:
            aux_matrix[x + 1][y + 1] += 1

    def place_numbers(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.main_matrix[i][j] == 8:
                    self.padding(self.main_matrix, i, j)

    def print_matrix(self):
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                print(self.main_matrix[i][j], end=" ")
            print()

matrix = np.zeros((100,100),dtype=int)
test = Board(15,15,25,matrix)
test.place_bombs()
test.place_numbers()
test.print_matrix()





