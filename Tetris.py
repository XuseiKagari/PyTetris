import pygame
import random, time
import numpy as np

class FigureStorage:
    def __init__(self):
        self.__figure = []

    def set_figure(self, idx, state):
        self.__figure[idx] = state

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.randint(0, 3)
        self.figure_type = self.random_figure()

    @staticmethod
    def random_figure():
        figures_cord = [
            # линия
            [["oooo"],
             ["xxxx"],
             ["oooo"],
             ["oooo"]],
            # L-образная
            [["xoo"],
             ["xoo"],
             ["xxo"]],
            # обратная L-образная
            [["oox"],
             ["oox"],
             ["oxx"]],
            # квадрат
            [["xx"],
             ["xx"]],
            # Z-образная
            [["xxo"],
             ["oxx"],
             ["ooo"]],
            # обратная Z-образная
            [["oxx"],
             ["xxo"],
             ["ooo"]],
            # T-образная
            [["oxo"],
             ["xxx"],
             ["ooo"]]
        ]
        figure = random.choice(figures_cord)
        return figure


    def left_move(self):
        if self.check_pos(playingField, next_x=-1):
            self.x -= 1
            going_left = True
            going_right = False
            last_side_move = time.time()

    def right_move(self):
        if self.check_pos(playingField, next_x=1):
            self.x += 1
            going_right = True
            going_left = False
            last_side_move = time.time()

    def rotate(self, k=3):
        a = np.array(self.figure_type)
        figure_type = np.rot90(a, k).tolist()


    def fast_falling(self):
        going_down = True
        if self.check_pos(playingField, next_y=1):
            self.y += 1
            last_move_down = time.time()

    # мгновенный сброс вниз
    def instant_falling(self):
        going_down = False
        going_left = False
        going_right = False
        for i in range(cell, field_h * cell):
            if not self.check_pos(playingField, next_y=i):
                break
            self.y += i - 1

    def free_fall(self):
        if time.time() - last_fall > fall_speed:  # свободное падение фигуры
            if not self.check_pos(playingField, next_y=1):  # проверка "приземления" фигуры
                fallingFig = None
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                self.y += 1
                last_fall = time.time()

    def check_pos(self, playingField, next_x=0, next_y=0):

        for block_x, block_y in self.figure_type:
            if self.y + block_y >= 19 or playingField[self.x + block_x + next_x][self.y + block_y + next_y] != "X":
                return False
        return True


class PlayingField:
    __playing_field = []
    __field_h = 20
    __field_w = 10
    __cell = 20
    colors = ((0, 0, 225),      # синий
              (0, 225, 0),      # зеленый
              (225, 0, 0),      # красный
              (225, 225, 0))    # желтый

    light_colors = ((30, 30, 255),   # светло-синий
                    (50, 255, 50),   # светло-зеленый
                    (255, 30, 30),   # светло-красный
                    (255, 255, 30))  # светло-желтый

    def __init__(self, screen_x, screen_y):
        self.initial_cord_x = (screen_x - self.__cell * self.__field_w) / 2
        self.initial_cord_y = (screen_y - self.__cell * self.__field_h) / 2
        for x in range(self.__field_w):
            self.__playing_field.append([])
            for y in range(self.__field_h):
                self.__playing_field[x].append("X")

    def drawing_playing_field(self, screen):
        pygame.draw.rect(screen, "grey",
                         ( self.initial_cord_x,  self.initial_cord_y,  self.__cell * self.__field_w, self.__cell * self.__field_h))

        for x in range(len(self.__playing_field)):
            for y in range(len(self.__playing_field[x])):
                pygame.draw.rect(screen, "black",
                                 ( self.initial_cord_x + self.__cell * x,  self.initial_cord_y + self.__cell * y, self.__cell, self.__cell), 1)
                self.draw_block(screen, self.initial_cord_x + self.__cell * x,  self.initial_cord_y + self.__cell * y, self.__playing_field[x][y])

    def draw_block(self, screen, cord_x, cord_y, color):
        if color == "x":
            return

        pygame.draw.rect(screen, self.colors[color], (cord_x + 1, cord_y + 1, self.__cell - 1, self.__cell - 1), 0, 3)
        pygame.draw.rect(screen, self.light_colors[color], (cord_x + 1, cord_y + 1, self.__cell - 4, self.__cell - 4), 0, 3)
        pygame.draw.circle(screen, self.colors[color], (cord_x + self.__cell / 2, cord_y + self.__cell / 2), 5)

class TetrisGame:
    pygame.init()
    __screen_x = 600
    __screen_y = 500
    __screen = pygame.display.set_mode((__screen_x, __screen_y))
    __fps_clock = pygame.time.Clock()
    __fps = 25
    fall_speed = 0.5
    pf = PlayingField(__screen_x, __screen_y)


    def play(self):

        running = True
        self.__fps_clock.tick(self.__fps)
        next_figure = Figure(pf.initialCord_x + (cell * field_w) / 2, pf.initialCord_y + 20)
        falling_figure = Figure(pf.initialCord_x + (cell * field_w) / 2, pf.initialCord_y + 20)

        pygame.display.set_caption("Tetris")

        while running:

            if falling_figure == None:
                falling_figure = next_figure
                next_figure = {"x": initialCord_x + (cell * field_w) / 2, "y": initialCord_y + 20, "Figure": NextFigure()}

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    # перемещение фигуры вправо и влево
                    if event.key == pygame.K_LEFT:
                        falling_figure.left_move()

                    elif event.key == pygame.K_RIGHT:
                        falling_figure.right_move()

                    # поворачиваем фигуру, если есть место
                    elif event.key == pygame.K_UP:
                        falling_figure.rotate()

                    # ускоряем падение фигуры
                    elif event.key == pygame.K_DOWN:
                        falling_figure.fast_falling()

                    # мгновенный сброс вниз
                    elif event.key == pygame.K_RETURN:
                        falling_figure.instant_falling()

            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    game = TetrisGame

