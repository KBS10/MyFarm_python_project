import pygame

import modules
from .. import Game
from ..Config import SHEEP_IMG
from ..Object import Object


class Sheep(Object):
    count = 0

    def __init__(self, x, y, area: pygame.Rect):
        Object.__init__(self, SHEEP_IMG, x, y)
        self.area = area

    def update(self, direction: str):
        if direction == 'left':
            self.rect.x -= 10 if self.rect.left > self.area.left else 0
        if direction == 'right':
            self.rect.x += 10 if self.rect.right < self.area.right else 0
        if direction == 'up':
            self.rect.y -= 10 if self.rect.top > self.area.top else 0
        if direction == 'down':
            self.rect.y += 10 if self.rect.bottom < self.area.bottom else 0
        if self.image != self.sheet:
            if direction == 'left':
                self.clip(self.left_states)
            if direction == 'right':
                self.clip(self.right_states)
            if direction == 'up':
                self.clip(self.up_states)
            if direction == 'down':
                self.clip(self.down_states)
            self.image = self.sheet.subsurface(self.sheet.get_clip())


class Pasture(pygame.Surface):
    def __init__(self) -> None:
        super().__init__((230, 310), pygame.SRCALPHA)
        self.pasture_area = pygame.Rect(620, 80, 230, 310)
        self.fill((0, 0, 0, 0))
        self.act_area = pygame.Rect(620, 390, 230, 100)

    def add(self, event: classmethod):
        if Game.Game.money.point < 100:
            return
        sheep = Sheep(self.pasture_area.centerx, self.pasture_area.centery, self.pasture_area)
        event('chicken', sheep)
        Sheep.count += 1
        print(Sheep.count)
        Game.Game.money.point -= 100

    def get_sell_rect(self) -> pygame.Rect:
        return self.act_area
