import pygame

from modules.Config import CORN_IMG
from modules import Game


class Corn(pygame.sprite.Sprite):
    field = [True, True, True, True]

    def __init__(self, x, y, field):
        pygame.sprite.Sprite.__init__(self)
        self.images = CORN_IMG
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x  # 318 for plot 2
        self.rect.y = y  # 580 for plot 2
        self.grow_time = 4000
        self.grow_time2 = 10000
        self.last = pygame.time.get_ticks()
        self.can_harvest = False
        self.field_count = field

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.grow_time:
            self.image = self.images[1]
            if now - self.last >= self.grow_time2:
                self.image = self.images[2]
                self.can_harvest = True
            if self.can_harvest and Game.Game.player.rect.colliderect(self.rect):
                self.harvest()

    def harvest(self):
        self.kill()
        Game.Game.money.point += 50
        Corn.field[self.field_count] = True


def plant(x, y, field):
    if Corn.field[field]:
        if Game.Game.money.point < 10:
            return
        corn = Corn(x, y, field)
        Game.Game.corn.add(corn)
        Game.Game.money.point -= 10
        Corn.field[field] = False
        return

    # 60, 580 ;; 318 580 835
