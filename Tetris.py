import pygame
import random, time, sys
from pygame.locals import *

screen_x, screen_y = 600, 500
cell, field_h, field_w = 20, 20, 10
initialCord_x = (screen_x - cell * field_w) / 2
initialCord_y = (screen_y - cell * field_h) / 2
empty = "x"
pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
fps_clock = pygame.time.Clock()
fps = 25
fall_speed = 0.5
colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0)) # синий, зеленый, красный, желтый
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30)) # светло-синий, светло-зеленый, светло-красный, светло-желтый

def main():
    running = True
    fps_clock.tick(fps)
    playingField = creatPF()
    nextFigure = {"x": initialCord_x + (cell * field_w) / 2, "y": initialCord_y + 20, "Figure": NextFigure()}
    fallingFig = {"x": initialCord_x + (cell * field_w) / 2, "y": initialCord_y + 20, "Figure": RandomFigure()}
    going_down = False
    going_left = False
    going_right = False

    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    points = 0

    while running:

        if fallingFig == None:
            fallingFig = nextFigure
            nextFigure = {"x": initialCord_x + (cell * field_w) / 2, "y": initialCord_y + 20, "Figure": NextFigure()}
            last_fall = time.time()


        DrawFallingFigure(fallingFig)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:

                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and checkPos(playingField, fallingFig, next_x=-1):
                    fallingFig['x'] -= cell
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(playingField, fallingFig, next_x=1):
                    fallingFig['x'] += cell
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(playingField, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(playingField, fallingFig, next_y=1):
                        fallingFig['y'] += cell
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(cell, field_h * cell):
                        if not checkPos(playingField, fallingFig, next_y=i):
                            break
                        fallingFig['y'] += i - cell

        if time.time() - last_fall > fall_speed:  # свободное падение фигуры
            if not checkPos(playingField, fallingFig, next_y=1):  # проверка "приземления" фигуры
                addToCup(playingField, fallingFig)  # фигура приземлилась, добавляем ее в содержимое стакана

                fallingFig = None
            else: # фигура пока не приземлилась, продолжаем движение вниз
                fallingFig['y'] += cell
                last_fall = time.time()

        pygame.display.flip()
        drawingPF(playingField)

    pygame.quit()


def creatPF():
    PF = []
    for x in range(field_w):
        PF.append([])
        for y in range(field_h):
            PF[x].append(empty)
    return PF



def drawingPF(PF):
    pygame.draw.rect(screen, "grey",
                     (initialCord_x, initialCord_y, cell * field_w, cell * field_h))

    for x in range(len(PF)):
        for y in range(len(PF[x])):
            pygame.draw.rect(screen, "black",
                     (initialCord_x + cell * x, initialCord_y + cell * y, cell, cell), 1)
            drawBlock(initialCord_x + cell * x, initialCord_y + cell * y, PF[x][y])


def drawBlock(cord_x, cord_y, color):
    if color == "x":
        return

    pygame.draw.rect(screen, colors[color], (cord_x + 1, cord_y + 1, cell - 1, cell - 1), 0, 3)
    pygame.draw.rect(screen, lightcolors[color], (cord_x + 1, cord_y + 1, cell - 4, cell - 4), 0, 3)
    pygame.draw.circle(screen, colors[color], (cord_x + cell / 2, cord_y + cell / 2), 5)


def RandomFigure():
    figuresCord = [
        # линия
        [[-2, 0], [-1, 0], [0, 0], [ 1, 0]],
        # L-образная
        [[-1, 1], [-1, 0], [0, 0], [ 1, 0]],
        # обратная L-образная
        [[ 1, 1], [-1, 0], [0, 0], [ 1, 0]],
        # квадрат
        [[-1, 1], [ 0, 1], [0, 0], [-1, 0]],
        # Z-образная
        [[ 1, 0], [ 1, 1], [0, 0], [-1, 0]],
        # обратная Z-образная
        [[ 0, 1], [-1, 0], [0, 0], [ 1, 0]],
        # T-образная
        [[-1, 1], [ 0, 1], [0, 0], [ 1, 0]],
    ]
    figure = random.choice(figuresCord)

    for j in range(random.randint(0, 3)):
        for i in range(len(figure)):
            x_new = figure[i][1]
            y_new = figure[i][0]
            figure[i][0] = -x_new
            figure[i][1] = y_new
    return (figure, random.randint(0, len(colors)-1))

def NextFigure():
    figure = RandomFigure()
    for x, y in figure[0]:
        drawBlock(initialCord_x + cell * (14 + x), initialCord_y + cell * (5 - y), figure[1])
    return figure

def DrawFallingFigure(fallingFig):
    figure = fallingFig["Figure"]
    x = fallingFig["x"]
    y = fallingFig["y"]
    for block_x, block_y in figure[0]:
        drawBlock(x + cell * block_x, y + cell * block_y, figure[1])

def checkPos(playingField, fallingFig, next_x=0, next_y=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
    figure = fallingFig["Figure"]
    x = int((fallingFig["x"]-initialCord_x) / cell)
    y = int((fallingFig["y"]-initialCord_y) / cell)
    for block_x, block_y in figure[0]:
        if y + block_y >=19 or playingField[x + block_x + next_x][y + block_y + next_y] != "x":
            return False
    return True

def addToCup(playingField, fallingFig):
    figure = fallingFig["Figure"]
    x =  int((fallingFig["x"] - initialCord_x) / cell)
    y =  int((fallingFig["y"] - initialCord_y) / cell)
    for block_x, block_y in figure[0]:
        playingField[x+block_x][y+block_y] = figure[1]

main()