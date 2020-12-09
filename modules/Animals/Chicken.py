import pygame

from ..Config import CHICKEN_IMG
from ..Object import Object


class Chicken(Object):
    count = 0

    def __init__(self, x, y, area: pygame.Rect):
        Object.__init__(self, CHICKEN_IMG, x, y)
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


class Coop(pygame.Surface):
    def __init__(self) -> None:
        super().__init__((160, 300), pygame.SRCALPHA)
        self.coop_area = pygame.Rect(850, 80, 160, 300)
        self.fill((0, 0, 0, 0))
        self.sell_area = pygame.Rect(850, 380, 160, 100)

    def add(self, event: classmethod):
        chicken = Chicken(self.coop_area.centerx, self.coop_area.centery, self.coop_area)
        event('chicken', chicken)
        Chicken.count += 1
        print(Chicken.count)

    def get_sell_rect(self) -> pygame.Rect:
        return self.sell_area
