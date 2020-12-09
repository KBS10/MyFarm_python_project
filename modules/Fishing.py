import pygame

from modules.Config import FISH_IMG
from modules.Object import Object


class Fish(Object):
    count = 0

    def __init__(self, image, area):
        super().__init__(image, 35, 35, area)


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
        # if not Fishing.do_fishing:
        # fish = Fish(FISH_IMG[0], self.fishing_area)
        # event('player', fish)
        # Fish.count += 1
        # print(Fish.count)
        print('test')
        self.player.set_fishing_mod(False)
        self.player.rect.center = (210, 190)

    def get_sell_rect(self) -> pygame.Rect:
        return self.act_area
