from typing import Iterator
from figure_s import FigureServer


class FigureStorageServer:
    def __init__(self):
        self.__figures = {}

    def get_falling(self) -> FigureServer | None:
        try:
            return self.__figures[max(self.__figures)]
        except Exception:
            return None

    def set_falling(self, figure) -> FigureServer:
        self.__figures[figure.id] = figure
        return figure

    def __iter__(self) -> Iterator[FigureServer]:
        return iter(self.__figures.values())

    def fallen_figures(self) -> list[FigureServer]:
        sorted_items = sorted(self.__figures.items())
        return [figure for _, figure in sorted_items[:-1]]

    def del_figure(self, ids):
        del self.__figures[ids]