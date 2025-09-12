from time import sleep
import pygame as pg
from playing_field import PlayingField
from figure_storage import FigureStorage
from button import Button
from client import Client


class TetrisGame:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Tetris")

        self.__screen_x = 600
        self.__screen_y = 500
        self.__screen = pg.display.set_mode((self.__screen_x, self.__screen_y))

        self.__fps_clock = pg.time.Clock()
        self.__fps = 25
        self.__fps_clock.tick(self.__fps)

        self.__fs = FigureStorage()

        self.__pf = PlayingField(self.__screen, self.__fs)


    def main_menu(self):
        self.__screen.fill((0, 0, 0))
        play_button = Button(250, 50, 100, 40, (255, 140, 0), 'Новая игра',
                             hover_color=(255, 100, 0), sound_path='../sound/button_click.mp3')
        net_play_button = Button(250, 100, 100, 40, (255, 140, 0), 'Сетевая игра',
                                 hover_color=(255, 100, 0), sound_path='../sound/button_click.mp3')
        settings_button = Button(250, 150, 100, 40, (255, 140, 0), 'Настройки',
                                 hover_color=(255, 100, 0), sound_path='../sound/button_click.mp3')
        exit_button = Button(250, 200, 100, 40, (255, 140, 0), 'Выход',
                             hover_color=(255, 100, 0), sound_path='../sound/button_click.mp3')
        while True:
            pg.display.flip()
            for event in pg.event.get():

                for btn in [play_button, net_play_button, settings_button, exit_button]:
                    btn.handle_event(event)
                    btn.draw(self.__screen)

                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.USEREVENT and event.button == exit_button:
                    return
                if event.type == pg.USEREVENT and event.button == play_button:
                    self.play()

                if event.type == pg.USEREVENT and event.button == net_play_button:
                    self.net_play()

                if event.type == pg.USEREVENT and event.button == settings_button:
                    self.settings_menu()


    def settings_menu(self):
        self.__screen.fill((0, 0, 0))
        back_button = Button(250, 100, 100, 40, (255, 140, 0), 'Назад',
                             hover_color=(255, 100, 0), sound_path='../sound/button_click.mp3')
        while True:
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.USEREVENT and event.button == back_button:
                    return
                for btn in [back_button]:
                    btn.handle_event(event)
                    btn.draw(self.__screen)

    def play(self):
        self.__screen.fill((0, 0, 0))
        while True:
            pg.display.flip()
            if self.__pf.game_over:
                return

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                self.__pf.handle_pg_event(event)
            self.__pf.tick()
            sleep(0.1)

    def net_play(self):
        client = Client(('localhost', 8080), self.__fs)
        self.__screen.fill((0, 0, 0))
        while True:
            pg.display.flip()
            if self.__pf.game_over:
                return

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                self.__pf.handle_pg_event(event)
            self.__pf.tick()
            sleep(0.1)

if __name__ == '__main__':
    game = TetrisGame()
    game.main_menu()
    pg.quit()
