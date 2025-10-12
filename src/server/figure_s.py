
class FigureServer:

    def __init__(self, ids, x, y, color, figure_type):
        self.id = int(ids)
        self.x = int(x)
        self.y = int(y)
        self.color = int(color)
        self.__figure_type = figure_type


