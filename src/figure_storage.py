from typing import Iterator
from figure import Figure

class FigureStorage:
    def __init__(self):
        self.__figures = []

    def get_falling(self) -> Figure | None:
        try:
            return self.__figures[-1]
        except Exception:
            return None

    def set_falling(self, figure) -> Figure:
        if len(self.__figures):
            self.__figures[-1] = figure
        else:
            self.__figures.append(figure)
        return figure

    def preempt_falling(self, figure) -> Figure:
        self.__figures.append(figure)
        return figure

    def __iter__(self) -> Iterator[Figure]:
        return iter(self.__figures)

    def fallen_figures(self) -> Iterator[Figure]:
        return self.__figures[0:-1]

    def add_figure(self, state):
        self.__figures.append(state)

    def del_figure(self, figure):
        self.__figures.pop(self.__figures.index(figure))

    def get_figure_st(self, idx=-1):
        return self.__figures[idx]

    def get_all(self):
        return self.__figures

