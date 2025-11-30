import time
from typing import Callable
from numpy import rot90, array


class FigureServer:

    def __init__(self, ids, x, y, color, figure_number_type):
        self.ids = int(ids)
        self.x = int(x)
        self.y = int(y)
        self.color = int(color)
        self.figure_number_type = figure_number_type
        self.__figure_type = self.random_figure(self.figure_number_type)

    @staticmethod
    def random_figure(__figure_number_type):
        figures_cord = [
            # линия
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            # L-образная
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 1]],
            # обратная L-образная
            [[0, 1, 0],
             [0, 1, 0],
             [1, 1, 0]],
            # квадрат
            [[1, 1],
             [1, 1]],
            # Z-образная
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            # # обратная Z-образная
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
            # T-образная
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
        ]
        return figures_cord[__figure_number_type]

    def get_figure(self):
        return self.__figure_type

    def set_figure(self, figure):
        self.__figure_type = figure

    def left_move(self, collision_func: Callable[[int, int], bool]):
        if self.collision_prob(collision_func, next_x=-1):
            self.x -= 1

    def right_move(self, collision_func: Callable[[int, int], bool]):
        if self.collision_prob(collision_func, next_x=1):
            self.x += 1

    def rotate(self, collision_func, k=1):
        rotated_figure = rot90(array(self.__figure_type), k)
        if self.collision_prob_rotate(collision_func, rotated_figure):
            self.__figure_type = rotated_figure.tolist()

    def falling(self, collision_func: Callable[[int, int], bool]):
        if self.collision_prob(collision_func, next_y=1):
            self.y += 1

    def remove_row(self, y):
        for x in range(len(self.__figure_type)):
            del self.__figure_type[x][y]

    def collision_prob(self, collision_func: Callable[[int, int], bool], next_x=0, next_y=0):
        for block_x in range(len(self.__figure_type)):
            for block_y in range(len(self.__figure_type[block_x])):
                if self.__figure_type[block_x][block_y]:
                    if collision_func(
                            self.x + block_x + next_x,
                            self.y + block_y + next_y
                    ):
                        return False
        return True

    def collision_prob_rotate(self, collision_func: Callable[[int, int], bool], rotated_figure):
        for block_x in range(len(rotated_figure)):
            for block_y in range(len(rotated_figure[block_x])):
                if rotated_figure[block_x][block_y]:
                    if collision_func(
                        self.x + block_x,
                        self.y + block_y
                    ):
                        return False
        return True
