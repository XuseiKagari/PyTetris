class Figure:
    def __init__(self, x, y, color, figure_type):
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.__figure_type = figure_type
