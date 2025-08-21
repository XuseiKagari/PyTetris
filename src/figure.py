import random, time
from enum import Enum
from typing import Callable
from numpy import rot90, array, flip


class Color(Enum):
        BLUE = ((0, 0, 225), (30, 30, 255))
        GREEN = ((0, 225, 0), (50, 255, 50))
        RED = ((225, 0, 0), (255, 30, 30))
        YELLOW = ((225, 225, 0), (255, 255, 30))

class Figure:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.color = random.choice([*Color])
        self.__figure_type = self.random_figure()
        self.__last_fall = time.time()

    @staticmethod
    def random_figure():
        figures_cord = [
            # линия
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            # # L-образная
            # [['o', 'x', 'o'],
            #  ['o', 'x', 'o'],
            #  ['o', 'x', 'x']],
            # # обратная L-образная
            # [['o', 'x', 'o'],
            #  ['o', 'x', 'o'],
            #  ['x', 'x', 'o']],
            # # квадрат
            # [['x', 'x'],
            #  ['x', 'x']],
            # # Z-образная
            # [['x', 'x', 'o'],
            #  ['o', 'x', 'x'],
            #  ['o', 'o', 'o']],
            # # обратная Z-образная
            # [['o', 'x', 'x'],
            #  ['x', 'x', 'o'],
            #  ['o', 'o', 'o']],
            # # T-образная
            # [['o', 'x', 'o'],
            #  ['x', 'x', 'x'],
            #  ['o', 'o', 'o']]
        ]
        figure = random.choice(figures_cord)
        rotated_figure = flip(rot90(figure, 1), 0)
        return rotated_figure.tolist()

    def get_figure(self):
        return self.__figure_type

    def set_figure(self, figure):
        self.__figure_type = figure

    def left_move(self, collision_func: Callable):
        if self.collision_prob(collision_func, next_x=-1):
            self.x -= 1

    def right_move(self, collision_func: Callable):
        if self.collision_prob(collision_func, next_x=1):
            self.x += 1

    def rotate(self, collision_func, k=1):
        rotated_figure = rot90(array(self.__figure_type), k)
        if self.collision_prob_rotate(collision_func, rotated_figure):
            self.__figure_type = rotated_figure.tolist()

    def fast_falling(self, collision_func: Callable):
        if self.collision_prob(collision_func, next_y=1):
            self.y += 1

    def instant_falling(self, playing_field):
        y = 0
        for i in range(playing_field.field_h):
            if not self.collision_prob(playing_field, next_y=i):
                break
            y = i
        self.__y += y

    def free_fall(self, collision_func: Callable, fall_speed=0.5):
        if time.time() - self.__last_fall > fall_speed:  # свободное падение фигуры
            if not self.collision_prob(collision_func, next_y=1):
                return False
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                self.y += 1
                self.__last_fall = time.time()
                return True
        return True

    def collision_prob(self, collision_func: Callable, next_x=0, next_y=0):
        for block_x in range(len(self.__figure_type)):
            for block_y in range(len(self.__figure_type[block_x])):
                if self.__figure_type[block_x][block_y]:
                    if collision_func(
                        self.x + block_x + next_x,
                        self.y + block_y + next_y
                    ):
                        return False
        return True

    def collision_prob_rotate(self, collision_func: Callable, rotated_figure):
        for block_x in range(len(rotated_figure)):
            for block_y in range(len(rotated_figure[block_x])):
                if rotated_figure[block_x][block_y]:
                    if collision_func(
                        self.x + block_x,
                        self.y + block_y
                    ):
                        return False
        return True


