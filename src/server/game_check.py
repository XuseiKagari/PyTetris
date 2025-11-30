from typing import Callable

class GameCheck:

    def __init__(self, figure_storage):
        self.__lines = 0
        self.field_h = 20
        self.field_w = 10
        self.__storage = figure_storage



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

    def remove_filled(self):
        for y in range(self.field_h - 1, -1, -1):
            buffer_state = self.__buffer_field(y)
            if len(buffer_state) == self.field_w:
                self.__lines += 1
                for item in set(buffer_state):
                    fig_idx, chip_y = item
                    self.__storage.fallen_figures()[fig_idx].remove_row(chip_y)
                for idx, figure in enumerate(self.__storage.fallen_figures()):
                    figure.fast_falling(self.__is_wrapped_func_excluded(idx))


    def check_move(self, ids, x, y):
        falling_figure = self.__storage.get_falling()
        if falling_figure.ids == ids:
            if falling_figure.x > x:
                falling_figure.left_move(self.__is_collided_func)
            if falling_figure.x < x:
                falling_figure.right_move(self.__is_collided_func)
            while falling_figure.y < y:
                falling_figure.falling(self.__is_collided_func)

    def check_rotate(self, ids):
        falling_figure = self.__storage.get_falling()
        if falling_figure.ids == ids:
            falling_figure.rotate(self.__is_collided_func)
