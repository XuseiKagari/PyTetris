from pygame.event import Event
from enum import Enum, auto
import pygame as pg
from queue import Queue
from figure import Figure
from figure_storage import FigureStorage


class PFEvents(Enum):
    MOVE_ACTIVE_LEFT = auto()
    MOVE_ACTIVE_RIGHT = auto()
    MOVE_ACTIVE_ROTATE = auto()
    MOVE_ACTIVE_FALL = auto()

class PlayingField:

    def __init__(self, screen: pg.Surface):
        self.__fall_speed = 0.5

        self.__screen = screen

        self.__playing_field = []
        self.field_w = 5
        self.field_h = 10
        self.field = tuple([self.field_w, self.field_h])
        self.__cell = 20

        self.__storage = FigureStorage()

        self.__event_bus = Queue()

        screen_x, screen_y = screen.get_size()
        self.initial_cord_x = int((screen_x - self.__cell * self.field_w) / 2)
        self.initial_cord_y = int((screen_y - self.__cell * self.field_h) / 2)

        self.__fall_from_x = self.field_w / 2 - 1
        self.__fall_from_y = 0

        self.__next_figure = None

        for x in range(self.field_w):
            self.__playing_field.append([])
            for y in range(self.field_h):
                self.__playing_field[x].append("X")
        self.__init_playing_field()

    def __init_playing_field(self):
        for x in range(self.field_w):
            for y in range(self.field_h):
                self.__playing_field[x][y] = "X"
    
    def __draw_figures(self):
        for figure in self.__storage:
            fig = figure.get_figure()
            x = figure.x
            y = figure.y
            for _x in range(len(fig)):
                for _y in range(len(fig[_x])):
                    if fig[_x][_y]:
                        self.draw_block(
                            self.initial_cord_x + self.__cell * (x + _x),
                            self.initial_cord_y + self.__cell * (y + _y), 
                            figure.color
                        )

    def __draw_playing_field(self):
        pg.draw.rect(self.__screen, "grey",
                    (self.initial_cord_x,  self.initial_cord_y,  self.__cell * self.field_w,
                     self.__cell * self.field_h))
        for x in range(len(self.__playing_field)):
            for y in range(len(self.__playing_field[x])):
                pg.draw.rect(self.__screen, "black",
                             (self.initial_cord_x + self.__cell * x,  self.initial_cord_y + self.__cell * y,
                              self.__cell, self.__cell), 1)

    def check_line_filled(self, y):
        for x in range(self.field_w):
            if self.__playing_field[x][y] == 'X':
                return False
        return True

    def find_filled_rows(self):
        removed_lines = 0
        y = self.field_h - 1
        while y >= 0:
            if self.check_line_filled(y):
                for pushDownY in range(y, 0, -1):
                    for x in range(self.field_w):
                        if x - 1 >= 0 and self.__playing_field[x][pushDownY] == self.__playing_field[x - 1][pushDownY]:
                            continue
                        figure = self.__playing_field[x][pushDownY]
                        if figure == "X":
                            y -= 1
                            break
                        fig = figure.get_figure()
                        fig_y = figure.get_y()
                        for fig_x in range(len(fig)):
                            if len([fig_x]) > 1:
                                del fig[fig_x][pushDownY - fig_y]
                                figure.set_figure(fig)
                                figure.set_y(fig_y + 1)
                            else:
                                del fig[fig_x][pushDownY - fig_y]
                                figure.set_figure(fig)
                for x in range(self.field_w):
                    self.__playing_field[x][0] = "X"
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    def draw_block(self, cord_x, cord_y, color):
        pg.draw.rect(self.__screen, color.value[0], (cord_x + 1, cord_y + 1, self.__cell - 1, self.__cell - 1), 0, 3)
        pg.draw.rect(self.__screen, color.value[1], (cord_x + 1, cord_y + 1, self.__cell - 4, self.__cell - 4), 0, 3)
        pg.draw.circle(self.__screen, color.value[0], (cord_x + self.__cell / 2, cord_y + self.__cell / 2), 5)

    def is_collided_func(self, x, y) -> bool:
        for figure in self.__storage.fallen_figures():
            fig = figure.get_figure()
            for _x in range(len(fig)):
                for _y in range(len(fig[_x])):
                    print(x, y, _x,  _y)
                    if self.initial_cord_x + _x == x and self.initial_cord_y + _y == y:
                        return False
        return False

    def tick(self):
        self.__draw_playing_field()

        if self.__next_figure is None:
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)
        falling_figure = self.__storage.get_falling()
        if falling_figure is None:
            self.__storage.set_falling(self.__next_figure)
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)
            falling_figure = self.__storage.get_falling()

        if not falling_figure.free_fall(self.is_collided_func, self.field):
            self.__storage.preempt_falling(self.__next_figure)
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)

        while not self.__event_bus.empty():
            evt = self.__event_bus.get()
            if evt == PFEvents.MOVE_ACTIVE_FALL:
                falling_figure.fast_falling(self.is_collided_func, self.field)
                self.__storage.set_falling(falling_figure)
            if evt == PFEvents.MOVE_ACTIVE_LEFT:
                falling_figure.left_move(self)
                self.__storage.set_falling(falling_figure)
            if evt == PFEvents.MOVE_ACTIVE_RIGHT:
                falling_figure.right_move(self)
                self.__storage.set_falling(falling_figure)
            if evt == PFEvents.MOVE_ACTIVE_ROTATE:
                falling_figure.rotate(self)
                self.__storage.set_falling(falling_figure)
        self.__draw_figures()

    def handle_pg_event(self, event: Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_FALL)
            if event.key == pg.K_LEFT:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_LEFT)
            if event.key == pg.K_RIGHT:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_RIGHT)
            if event.key == pg.K_r:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_ROTATE)
