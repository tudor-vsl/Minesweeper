import random as rand
import numpy as np


class Board:
    """ I decided to create a class named Board for an easier management of the code """

    def __init__(self, rows, cols, no_of_bombs, main_matrix):
        """ Initialzing the 5 atributes of the class """
        self.rows = rows
        self.cols = cols
        self.no_of_bombs = no_of_bombs
        self.main_matrix = main_matrix
        self.coord_list = []

    def place_bombs(self):
        """ This method randomly chooses where to place the bombs and manages their coordinates with a list """
        i = 0
        while i < self.no_of_bombs:
            rand_x = rand.randint(0, self.rows - 1)
            rand_y = rand.randint(0, self.cols - 1)
            if (rand_x, rand_y) not in self.coord_list:
                self.main_matrix[rand_x][rand_y] = 9
                self.coord_list.append((rand_x, rand_y))
                i += 1

    @staticmethod
    def padding(aux_matrix, x, y):
        """ The padding method adds 1 to each value in the main matrix if it has a mine as a neighbour. It finds all
                the values equal with 9 and adds 1 to their neighbours """
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
        """ Calling the function and creating our matrix"""
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.main_matrix[i][j] == 9:
                    self.padding(self.main_matrix, i, j)

    def print_matrix(self):
        """ Function that prints the matrix"""
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                print(self.main_matrix[i][j], end=" ")
            print()
