import pygame as pg
from playing_field import PlayingField

class TetrisGame:

    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tetris")

        self.__screen_x = 600
        self.__screen_y = 500
        self.__screen = pg.display.set_mode((
            self.__screen_x, self.__screen_y)
        )

        self.__fps_clock = pg.time.Clock()
        self.__fps = 25
        self.__fps_clock.tick(self.__fps)

        self.__pf = PlayingField(self.__screen)

    def play(self):

        while 1:
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break
                self.__pf.handle_pg_event(event)
            self.__pf.tick()
        pg.quit()

if __name__ == '__main__':
    game = TetrisGame()
    game.play()
