import pygame

from . import Config
from . import Object

# from .Animals import *
from .Animals.Chicken import Coop
from .Animals.Sheep import Pasture
from .Config import Money
from .Fishing import Fishing
from .Player import Farmer


class Game():
    def __init__(self):
        self.SIZE = (1024, 768)
        self.INTERFACE = (1024, 80)

        self.screen = pygame.display.set_mode(size=(self.SIZE[0], self.SIZE[1] + self.INTERFACE[1]))
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.RUNNING = True

        self.objects = {'player': [pygame.sprite.Group(), []], 'chicken': [pygame.sprite.Group(), []],
                        'sheep': [pygame.sprite.Group(), []]}
        self.set_up()
        self.player = Farmer()

        self.coop = Coop()
        self.pasture = Pasture()
        self.fishing = Fishing(self.player)

        self.player.add_block_area(self.coop.coop_area, self.pasture.pasture_area, self.fishing.fishing_block_1,
                                   self.fishing.fishing_block_2, self.fishing.fishing_block_3)
        self.player.add_sell_area(self.coop, self.pasture, self.fishing)

    @staticmethod
    def set_up():
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('MY_FARM')

    def set_object(self, key: str, item: pygame.sprite.Sprite):
        self.objects[key][0].add(item)
        self.objects[key][1].append(item)

    def event_handler(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.RUNNING = False
        if e.type == pygame.QUIT:
            self.RUNNING = False

    def blit_surface(self):
        # self.screen.blit(self.fishing, self.fishing.fishing_area)
        pass

    def draw_sprites(self, obj: dict):
        for key in obj.keys():
            item = obj[key][0]
            item.draw(self.screen)
            for drawable in obj[key][1]:
                if hasattr(drawable, 'is_drawable') and drawable.is_drawable:
                    drawable.draw_self(self.screen)
                if hasattr(drawable, 'auto') and drawable.is_auto:
                    drawable.auto()

    def run(self):
        self.set_object('player', self.player)
        self.set_object('player', Money())
        while self.RUNNING:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.player.act_handler(event, self.set_object)
                pass
            self.event_handler(event)
            self.screen.fill((255, 255, 255))
            self.screen.blit(Config.BG_IMG, (0, self.INTERFACE[1]))
            self.blit_surface()
            self.draw_sprites(self.objects)
            self.player.handle_event(event)
            pygame.display.update()
        if not self.RUNNING:
            pygame.quit()
