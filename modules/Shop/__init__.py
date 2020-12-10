import pygame

import modules
from modules import Game
from modules.Corn.Corn import plant


class Shop(pygame.Surface):
    def __init__(self, flag=False) -> None:
        super().__init__((1000, 500), pygame.SRCALPHA)
        self.on = flag
        self.rect = self.get_rect()
        self.rect.center = (1024 / 2, 868 / 2 - 100)
        self.fill((255, 255, 255, 0))
        self.button('corn', 10, 10, 100, 100, (255, 255, 255), (255, 255, 0), lambda x=70, y=660, z=0: plant(x, y, z))
        self.button('corn', 120, 10, 100, 100, (255, 255, 255), (255, 255, 0), lambda x=318, y=660, z=1: plant(x, y, z))
        self.button('corn', 230, 10, 100, 100, (255, 255, 255), (255, 255, 0), lambda x=580, y=660, z=2: plant(x, y, z))
        self.button('corn', 340, 10, 100, 100, (255, 255, 255), (255, 255, 0), lambda x=835, y=660, z=3: plant(x, y, z))
        self.button('exit', 450, 10, 100, 100, (255, 0, 0), (0, 0, 255), Game.Game.handle_shop)

    def button(self, msg, x, y, w, h, ic, ac, action):
        if self.on:
            def text_objects(text, font):
                text_surface = font.render(text, True, (0, 0, 0))
                return text_surface, text_surface.get_rect()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + w + self.rect.left > mouse[0] > x + self.rect.left and y + h + self.rect.top > mouse[
                1] > y + self.rect.top:
                pygame.draw.rect(self, ac, (x, y, w, h))
                if click[0] == 1:
                    action()
            else:
                pygame.draw.rect(self, ic, (x, y, w, h))

            small_text = pygame.font.Font('font/dimbo_regular.ttf', 40)
            text_surf, text_rect = text_objects(msg, small_text)
            text_rect.center = (x + (w / 2), y + (h / 2))
            self.blit(text_surf, text_rect)


def open_shop(event, shop_rect: pygame.Rect, on):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if shop_rect.collidepoint(mouse) and not on:
        if click[0] == 1:
            event()
