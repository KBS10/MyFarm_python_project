import random
import pygame
from pygame.sprite import AbstractGroup

from modules.Config import FISH_IMG
from modules.Object import Object


class Fish(Object):
    count = 0

    def __init__(self, x, y, image):
        Object.__init__(self, image, x, y)
        self.is_auto = False

    def click(self, event, target, mouse, click, money):
        x, y, w, h = target.rect
        print(x, y, w, h)
        print(mouse)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1:
                event('fish', target, False)
                money.point += 100
                return True

    def get_click(self):
        return lambda event, target, mouse, click, money: self.click(event, target, mouse, click, money)


class FishMonitor(pygame.sprite.Sprite):

    def __init__(self, event: classmethod) -> None:
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (210, 220)
        self.is_running = False
        self.event = event
        self.bar_x = 0
        self.flag_x = random.randint(0, 100)
        self.move = 10
        event('player', self)
        self.flag = pygame.Surface((20, 10))
        self.flag.fill((0, 255, 0))
        self.point = pygame.Surface((10, 10))
        self.point.fill((255, 0, 0))

    def kill(self) -> None:
        self.event('player', self, False)

    def update(self) -> None:
        self.image.fill((0, 0, 0))
        self.image.blit(self.flag, (self.flag_x, 0))
        self.image.blit(self.point, (self.bar_x, 0))
        self.bar_x = (self.bar_x + self.move) % 100

    def success(self) -> bool:
        self.move = 0
        print(abs(self.bar_x - self.flag_x))
        if abs(self.bar_x - self.flag_x) < 30:
            return True
        return False


class Fishing(pygame.Surface):
    do_fishing = False

    def __init__(self, player) -> None:
        super().__init__((65, 50), pygame.SRCALPHA)
        self.fishing_area = pygame.Rect(210, 190, 65, 50)
        self.fishing_block_1 = pygame.Rect(290, 80, 50, 110)
        self.fishing_block_2 = pygame.Rect(0, 80, 175, 130)
        self.fishing_block_3 = pygame.Rect(210, 80, 65, 45)
        self.fill((0, 0, 0))
        self.set_alpha(80)
        self.act_area = pygame.Rect(210, 190, 65, 50)

        self.player = player

    def add(self, event: classmethod):
        self.player.set_fishing_mod()
        self.player.rect.center = (150, 100)
        self.__setattr__('bar', FishMonitor(event))

    def get_sell_rect(self) -> pygame.Rect:
        return self.act_area
