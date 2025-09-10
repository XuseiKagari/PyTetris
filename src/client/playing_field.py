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
    MOVE_ACTIVE_INSTANT_FALL = auto()


class PlayingField:
    def __init__(self, screen: pg.Surface):
        self.__lines = 0

        self.f1 = pg.font.Font(None, 20)

        self.__screen = screen

        self.field_h = 20
        self.field_w = 10
        self.__cell = 20

        self.__storage = FigureStorage()

        self.__event_bus = Queue()

        screen_x, screen_y = screen.get_size()
        self.initial_cord_x = int((screen_x - self.__cell * self.field_w) / 2)
        self.initial_cord_y = int((screen_y - self.__cell * self.field_h) / 2)

        self.__fall_from_x = int(self.field_w / 2) - 1
        self.__fall_from_y = 0

        self.__next_figure = None

        self.game_over = False

    def __draw_figures(self):
        for figure in self.__storage:
            fig = figure.get_figure()
            for _x in range(len(fig)):
                for _y in range(len(fig[_x])):
                    if fig[_x][_y]:
                        self.__draw_block(
                            self.initial_cord_x + self.__cell * (figure.x + _x),
                            self.initial_cord_y + self.__cell * (figure.y + _y),
                            figure.color
                        )

    def __draw_next_figure(self, next_figure):
        text_next_figure = self.f1.render('Следующая фигура', False, "White")
        self.__screen.blit(text_next_figure, (
            self.initial_cord_x + self.__cell * (self.field_w + 2),
            self.initial_cord_y))
        pg.draw.rect(self.__screen, "black",(
            self.initial_cord_x + self.__cell * (self.field_w + 2),
            self.initial_cord_y + self.__cell,
            self.__cell * 4, self.__cell * 4))
        fig = next_figure.get_figure()
        for _x in range(len(fig)):
            for _y in range(len(fig[_x])):
                if fig[_x][_y]:
                    self.__draw_block(
                        self.initial_cord_x + self.__cell * (self.field_w + _x + 2),
                        self.initial_cord_y + self.__cell * (_y + 1),
                        next_figure.color
                    )

    def __draw_playing_field(self):

        text_level = self.f1.render('Уровень: ' + str(self.__current_level(self.__lines)), False, "White")
        self.__screen.blit(text_level, (
            self.initial_cord_x + self.__cell * (self.field_w + 2),
            self.initial_cord_y + self.__cell * 5))

        pg.draw.rect(self.__screen, "grey",
                     (self.initial_cord_x, self.initial_cord_y, self.__cell * self.field_w,
                      self.__cell * self.field_h))

        for x in range(self.field_w):
            for y in range(self.field_h):
                pg.draw.rect(self.__screen, "black",
                             (self.initial_cord_x + self.__cell * x, self.initial_cord_y + self.__cell * y,
                              self.__cell, self.__cell), 1)

    def __draw_block(self, cord_x, cord_y, color):
        pg.draw.rect(self.__screen, color.value[0], (cord_x + 1, cord_y + 1, self.__cell - 1, self.__cell - 1), 0, 3)
        pg.draw.rect(self.__screen, color.value[1], (cord_x + 1, cord_y + 1, self.__cell - 4, self.__cell - 4), 0, 3)
        pg.draw.circle(self.__screen, color.value[0], (cord_x + self.__cell / 2, cord_y + self.__cell / 2), 5)

    def __is_collided_func(self, x, y) -> bool:
        if x < 0 or x >= self.field_w:
            return True
        if y < 0 or y >= self.field_h:
            return True
        for figure in self.__storage.fallen_figures():
            fig = figure.get_figure()
            for _x in range(len(fig)):
                for _y in range(len(fig[_x])):
                    if fig[_x][_y]:
                        if figure.x + _x == x and figure.y + _y == y:
                            return True
        return False

    def __is_wrapped_func_excluded(self, exclude):
        def __is_collided_func(x, y) -> bool:
            if x < 0 or x >= self.field_w:
                return True
            if y < 0 or y >= self.field_h:
                return True
            for idx, figure in enumerate(self.__storage.fallen_figures()):
                if exclude == idx:
                    continue
                fig = figure.get_figure()
                for _x in range(len(fig)):
                    for _y in range(len(fig[_x])):
                        if fig[_x][_y]:
                            if figure.x + _x == x and figure.y + _y == y:
                                return True
            return False

        return __is_collided_func

    def __buffer_field(self, y):
        buffer_state = {}
        for fig_idx, figure in enumerate(self.__storage.fallen_figures()):
            fig = figure.get_figure()
            for _x in range(len(fig)):
                for _y in range(len(fig[_x])):
                    if fig[_x][_y]:
                        actual_y = figure.y + _y
                        idx = actual_y
                        if buffer_state.get(idx, None) is None:
                            buffer_state[idx] = []
                        buffer_state[idx].append((fig_idx, _y))
        return buffer_state.get(y, [])

    def __remove_filled(self):
        for y in range(self.field_h - 1, -1, -1):
            buffer_state = self.__buffer_field(y)
            if len(buffer_state) == self.field_w:
                self.__lines += 1
                for item in set(buffer_state):
                    fig_idx, chip_y = item
                    self.__storage.fallen_figures()[fig_idx].remove_row(chip_y)
                for idx, figure in enumerate(self.__storage.fallen_figures()):
                    figure.fast_falling(self.__is_wrapped_func_excluded(idx))

    def __fall_speed(self, level) -> int:
        return pow(0.8 - ((level - 1) * 0.007), level - 1)

    def __current_level(self, lines):
        return 1 + int(lines/10)

    def tick(self):
        self.__draw_playing_field()

        if self.__next_figure is None:
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)
            self.__draw_next_figure(self.__next_figure)
        falling_figure = self.__storage.get_falling()
        if falling_figure is None:
            self.__storage.set_falling(self.__next_figure)
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)
            self.__draw_next_figure(self.__next_figure)
            falling_figure = self.__storage.get_falling()

        if not falling_figure.free_fall(self.__is_collided_func, self.__fall_speed(
                self.__current_level(self.__lines))):
            self.__storage.set_falling(self.__next_figure)
            self.__next_figure = Figure(self.__fall_from_x, self.__fall_from_y)
            self.__draw_next_figure(self.__next_figure)
            falling_figure = self.__storage.get_falling()
            if not falling_figure.free_fall(self.__is_collided_func, self.__fall_speed(
                    self.__current_level(self.__lines))):
                self.game_over = True
                return
        self.__remove_filled()

        while not self.__event_bus.empty():
            evt = self.__event_bus.get()
            if evt == PFEvents.MOVE_ACTIVE_FALL:
                falling_figure.fast_falling(self.__is_collided_func)
            if evt == PFEvents.MOVE_ACTIVE_LEFT:
                falling_figure.left_move(self.__is_collided_func)
            if evt == PFEvents.MOVE_ACTIVE_RIGHT:
                falling_figure.right_move(self.__is_collided_func)
            if evt == PFEvents.MOVE_ACTIVE_ROTATE:
                falling_figure.rotate(self.__is_collided_func)
            if evt == PFEvents.MOVE_ACTIVE_INSTANT_FALL:
                falling_figure.instant_falling(self.__is_collided_func)

        self.__draw_figures()

    def handle_pg_event(self, event: Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_FALL)
            if event.key == pg.K_LEFT:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_LEFT)
            if event.key == pg.K_RIGHT:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_RIGHT)
            if event.key == pg.K_UP:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_ROTATE)
            if event.key == pg.K_SPACE:
                self.__event_bus.put(PFEvents.MOVE_ACTIVE_INSTANT_FALL)


