import random, time
from enum import Enum
from typing import Callable
from numpy import rot90, array


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
        return figure

    def get_figure(self):
        return self.__figure_type

    def set_figure(self, figure):
        self.__figure_type = figure

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def left_move(self, playing_field):
        if self.check_pos(playing_field, next_x=-1):
            self.__x -= 1

    def right_move(self, playing_field):
        if self.check_pos(playing_field, next_x=1):
            self.__x += 1

    def rotate(self, playing_field, k=1):
        rotated_figure = rot90(array(self.__figure_type), k)
        # if self.check_rotate(playing_field, rotated_figure):
        #     self.__figure_type = rotated_figure.tolist()

    def fast_falling(self, is_collided_func: Callable, field: tuple[int, int]):
        if self.check_pos(is_collided_func, field, next_y=1):
            self.y += 1

    def instant_falling(self, playing_field):
        y = 0
        for i in range(playing_field.field_h):
            if not self.check_pos(playing_field, next_y=i):
                break
            y = i
        self.__y += y

    def free_fall(self, is_collided_func: Callable, field: tuple[int, int], fall_speed=0.5):
        if time.time() - self.__last_fall > fall_speed:  # свободное падение фигуры
            if not self.check_pos(is_collided_func, field, next_y=1):
                return False
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                self.y += 1
                self.__last_fall = time.time()
                return True
        return True

    def check_pos(self, is_collided_func, field: tuple[int, int], next_x=0, next_y=0):
        w, h = field
        for block_x in range(len(self.__figure_type)):
            for block_y in range(len(self.__figure_type[block_x])):
                if self.__figure_type[block_x][block_y]:
                    if self.x + block_x + next_x >= w or self.x + block_x + next_x < 0:
                        return False
                    elif self.y + block_y + next_y >= h or self.y + block_y + next_y < 0:
                        return False
                    print(self.x + block_x + next_x, self.y + block_y + next_y)
                    if is_collided_func(self.x + block_x + next_x, self.y + block_y + next_y):
                        return False
        return True

    def check_rotate(self, playing_field, rotated_figure):
        for block_x in range(len(rotated_figure)):
            for block_y in range(len(rotated_figure[block_x])):
                if rotated_figure[block_x][block_y] == 'x':
                    if self.__x + block_x >= playing_field.field_w or self.__x + block_x < 0:
                        return False
                    elif self.__y + block_y >= playing_field.field_h or self.__y + block_y < 0:
                        return False
                    if playing_field.get_playing_field(self.__x + block_x, self.__y + block_y) != "X":
                        return False
        return True


