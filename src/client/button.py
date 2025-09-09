import pygame as pg

class Button:
    def __init__(self, x, y, width, height, color, text=None, font_size=20, hover_color=None, sound_path=None):
        self.__text = text
        self.__font_size = font_size
        self.__button_surface = pg.Surface((width, height))
        self.__button_rect = self.__button_surface.get_rect(topleft=(x, y))
        self.__color = color
        self.__button_surface.fill(color)
        if hover_color:
            self.__hover_color = hover_color
        else:
            self.__hover_color = color
        if sound_path:
            self.__sound = pg.mixer.Sound(sound_path)

        self.__is_hovered = False

    def draw(self, screen):
        if self.__is_hovered:
            self.__button_surface.fill(self.__hover_color)
        else:
            self.__button_surface.fill(self.__color)

        screen.blit(self.__button_surface, self.__button_rect.topleft)
        if self.__text is not None:
            self.__create_text(screen)
        self.__check_hover()

    def __create_text(self, screen):
        font = pg.font.Font(None, self.__font_size)
        text_surface = font.render(self.__text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.__button_rect.center)
        screen.blit(text_surface, text_rect)

    def __check_hover(self):
        self.__is_hovered = self.__button_rect.collidepoint(pg.mouse.get_pos())

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.__is_hovered:
            if self.__sound:
                self.__sound.play()
            pg.event.post(pg.event.Event(pg.USEREVENT, button=self))
