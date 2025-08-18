import pygame as pg
import random, time
from enum import Enum
from numpy import rot90, array


class Color(Enum):
        BLUE = ((0, 0, 225), (30, 30, 255))
        GREEN = ((0, 225, 0), (50, 255, 50))
        RED = ((225, 0, 0), (255, 30, 30))
        YELLOW = ((225, 225, 0), (255, 255, 30))


class FigureStorage:
    def __init__(self):
        self.__figure = []

    def app_figure(self, state):
        self.__figure.append(state)

    def get_figure(self, idx=-1):
        return self.__figure[idx]

    def get_all(self):
        return self.__figure

class Figure:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)
        self.__color = random.choice([*Color])
        self.__figure_type = self.random_figure()
        self.__last_fall = time.time()
    @staticmethod
    def random_figure():
        figures_cord = [
            # линия
            [['o', 'o', 'o', 'o'],
             ['x', 'x', 'x', 'x'],
             ['o', 'o', 'o', 'o'],
             ['o', 'o', 'o', 'o']],
            # L-образная
            [['o', 'x', 'o'],
             ['o', 'x', 'o'],
             ['o', 'x', 'x']],
            # обратная L-образная
            [['o', 'x', 'o'],
             ['o', 'x', 'o'],
             ['x', 'x', 'o']],
            # квадрат
            [['x', 'x'],
             ['x', 'x']],
            # Z-образная
            [['x', 'x', 'o'],
             ['o', 'x', 'x'],
             ['o', 'o', 'o']],
            # обратная Z-образная
            [['o', 'x', 'x'],
             ['x', 'x', 'o'],
             ['o', 'o', 'o']],
            # T-образная
            [['o', 'x', 'o'],
             ['x', 'x', 'x'],
             ['o', 'o', 'o']]
        ]
        figure = random.choice(figures_cord)
        return figure

    def get_figure(self):
        return self.__figure_type

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.__color

    def left_move(self, playing_field):
        if self.check_pos(playing_field, next_x=-1):
            self.__x -= 1

    def right_move(self, playing_field):
        if self.check_pos(playing_field, next_x=1):
            self.__x += 1

    def rotate(self, playing_field, k=3):
        a = array(self.__figure_type)
        self.__figure_type = rot90(a, k).tolist()
        if not self.check_pos(playing_field):
            self.__figure_type = rot90(a, -k).tolist()

    def fast_falling(self, playing_field):
        going_down = True
        if self.check_pos(playing_field, next_y=1):
            self.__y += 1

    def instant_falling(self, playing_field):
        for i in range(playing_field.get_field_h()):
            if not self.check_pos(playing_field, next_y=i):
                break
            y = i
        self.__y += y

    def free_fall(self, playing_field, fall_speed):
        if time.time() - self.__last_fall > fall_speed:  # свободное падение фигуры
            if not self.check_pos(playing_field, next_y=1):  # проверка "приземления" фигуры
                playing_field.app_playing_field(self)
                return False
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                self.__y += 1
                self.__last_fall = time.time()
                return True
        return True

    def check_pos(self, playing_field, next_x=0, next_y=0):

        for block_x in range(len(self.__figure_type)):
            for block_y in range(len(self.__figure_type[block_x])):
                if self.__figure_type[block_x][block_y] == 'x':
                    if self.__x + block_x + next_x >= playing_field.get_field_w() or self.__x + block_x + next_x < 0:
                        return False
                    elif self.__y + block_y + next_y >= playing_field.get_field_h() or self.__y + block_y + next_y < 0:
                        return False
                    if playing_field.get_playing_field(self.__x + block_x + next_x, self.__y + block_y + next_y) != "X":
                        return False
        return True


class PlayingField:
    __playing_field = []
    __field_h = 20
    __field_w = 10
    __cell = 20

    def __init__(self, screen_x, screen_y):
        self.initial_cord_x = int((screen_x - self.__cell * self.__field_w) / 2)
        self.initial_cord_y = int((screen_y - self.__cell * self.__field_h) / 2)
        for x in range(self.__field_w):
            self.__playing_field.append([])
            for y in range(self.__field_h):
                self.__playing_field[x].append("X")

    def app_playing_field(self, figure):
        fig = figure.get_figure()
        x = figure.get_x()
        y = figure.get_y()
        for block_x in range(len(fig)):
            for block_y in range(len(fig[block_x])):
                if fig[block_x][block_y] == 'x':
                    self.__playing_field[x + block_x][y + block_y] = figure

    def update_playing_field(self, storage):
        for x in range(self.__field_w):
            for y in range(self.__field_h):
                self.__playing_field[x][y] = "X"
        for figure in storage:
            fig = figure.get_figure()
            x = figure.get_x()
            y = figure.get_y()
            for block_x in range(len(fig)):
                for block_y in range(len(fig[block_x])):
                    if fig[block_x][block_y] == 'x':
                        self.__playing_field[x + block_x][y + block_y] = figure

    def get_playing_field(self, x, y):
        return self.__playing_field[x][y]

    def get_field_h(self):
        return self.__field_h

    def get_field_w(self):
        return self.__field_w

    def drawing_playing_field(self, screen):
        pg.draw.rect(screen, "grey",
                    (self.initial_cord_x,  self.initial_cord_y,  self.__cell * self.__field_w,
                     self.__cell * self.__field_h))

        for x in range(len(self.__playing_field)):
            for y in range(len(self.__playing_field[x])):
                pg.draw.rect(screen, "black",
                             (self.initial_cord_x + self.__cell * x,  self.initial_cord_y + self.__cell * y,
                              self.__cell, self.__cell), 1)
                if self.__playing_field[x][y] != "X":
                    self.draw_block(screen, self.initial_cord_x + self.__cell * x,
                                    self.initial_cord_y + self.__cell * y, self.__playing_field[x][y].get_color())

    def drawing_falling_figure(self, screen, falling_figure):
        fig = falling_figure.get_figure()
        x = falling_figure.get_x()
        y = falling_figure.get_y()
        color = falling_figure.get_color()
        for block_x in range(len(fig)):
            for block_y in range(len(fig[block_x])):
                if fig[block_x][block_y] == 'x':
                    self.draw_block(screen, self.initial_cord_x + self.__cell * (x + block_x),
                                    self.initial_cord_y + self.__cell * (y + block_y), color)

    def draw_block(self, screen, cord_x, cord_y, color):
        pg.draw.rect(screen, color.value[0], (cord_x + 1, cord_y + 1, self.__cell - 1, self.__cell - 1), 0, 3)
        pg.draw.rect(screen, color.value[1], (cord_x + 1, cord_y + 1, self.__cell - 4, self.__cell - 4), 0, 3)
        pg.draw.circle(screen, color.value[0], (cord_x + self.__cell / 2, cord_y + self.__cell / 2), 5)


class TetrisGame:
    pg.init()
    pg.display.set_caption("Tetris")
    __screen_x = 600
    __screen_y = 500
    __screen = pg.display.set_mode((__screen_x, __screen_y))
    __fps_clock = pg.time.Clock()
    __fps = 25
    fall_speed = 0.5
    pf = PlayingField(__screen_x, __screen_y)
    storage = FigureStorage()

    def play(self):

        running = True
        self.__fps_clock.tick(self.__fps)
        next_figure = Figure(self.pf.get_field_w() / 2 - 1, 0)
        falling_figure = Figure(self.pf.get_field_w() / 2 - 1, 0)
        self.storage.app_figure(falling_figure)
        while running:
            pg.display.flip()
            self.pf.drawing_playing_field(self.__screen)
            if falling_figure is None:
                falling_figure = next_figure
                self.storage.app_figure(falling_figure)
                next_figure = Figure(self.pf.get_field_w() / 2 - 1, 0)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:

                    # перемещение фигуры вправо и влево
                    if event.key == pg.K_LEFT:
                        falling_figure.left_move(self.pf)

                    elif event.key == pg.K_RIGHT:
                        falling_figure.right_move(self.pf)

                    # поворачиваем фигуру, если есть место
                    elif event.key == pg.K_UP:
                        falling_figure.rotate(self.pf)

                    # ускоряем падение фигуры
                    elif event.key == pg.K_DOWN:
                        falling_figure.fast_falling(self.pf)

                    # мгновенный сброс вниз
                    elif event.key == pg.K_SPACE:
                        falling_figure.instant_falling(self.pf)

            self.pf.drawing_falling_figure(self.__screen, falling_figure)
            if not falling_figure.free_fall(self.pf, self.fall_speed):
                falling_figure = None

        pg.quit()

if __name__ == '__main__':
    game = TetrisGame()
    game.play()
