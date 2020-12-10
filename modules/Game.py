import runpy
import time

import pygame
import random

from pygame import font

from . import Config
from .Animals.Chicken import Coop
from .Animals.Sheep import Pasture
from .Config import Money, FISH_IMG
from .Fishing import Fishing, Fish
from .Player import Farmer
from .Shop import Shop, open_shop


class Game():
    is_shop_on = False
    money = Money()
    corn = pygame.sprite.Group()
    player = Farmer()
    fishing = Fishing(player)

    def __init__(self):
        self.SIZE = (1024, 768)
        self.INTERFACE = (1024, 80)

        self.event_list = []
        self.screen = pygame.display.set_mode(size=(self.SIZE[0], self.SIZE[1] + self.INTERFACE[1]))
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.RUNNING = True
        self.money.point = 100
        self.objects = {'player': [pygame.sprite.Group(), []], 'chicken': [pygame.sprite.Group(), []],
                        'sheep': [pygame.sprite.Group(), []], 'fish': [pygame.sprite.Group(), []]}
        self.set_up()
        self.coop = Coop()
        self.shop_area = pygame.Rect((900, 470, 150, 90))
        self.shop = Shop()
        self.pasture = Pasture()
        # self.fishing = Fishing(self.player)
        self.player.add_block_area(self.coop.coop_area, self.pasture.pasture_area, self.fishing.fishing_block_1,
                                   self.fishing.fishing_block_2, self.fishing.fishing_block_3, self.shop_area
                                   )
        self.player.add_sell_area(self.coop, self.pasture, self.fishing)

    @staticmethod
    def set_up():
        pygame.init()
        # pygame.font.init()
        pygame.display.set_caption('MY_FARM')

    @staticmethod
    def handle_shop():
        Game.is_shop_on = not Game.is_shop_on

    def set_object(self, key: str, item: pygame.sprite.Sprite, mode: bool = True):
        if mode is True:
            self.objects[key][0].add(item)
            self.objects[key][1].append(item)
        else:
            self.objects[key][0].remove(item)
            self.objects[key][1].pop()

    def event_handler(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.RUNNING = False
        if e.type == pygame.QUIT:
            self.RUNNING = False

    def blit_surface(self):
        # self.screen.blit(self.fishing, self.fishing.fishing_area)
        if self.is_shop_on:
            self.screen.blit(Shop(True), self.shop.rect)
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

    def handle_fishing(self, event):
        if hasattr(self.fishing, 'bar'):
            self.fishing.bar.update()
            print(event)
            if event.type == pygame.KEYDOWN:
                for k in [pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT]:
                    if event.key == k:
                        self.fishing.bar.kill()
                        self.fishing.__delattr__('bar')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.stop_fishing()

    def stop_fishing(self):
        if hasattr(self.fishing, 'bar'):
            success = self.fishing.bar.success()
            if success:
                fish = Fish(190, 190, random.choice(FISH_IMG))
                self.set_object('fish', fish)
                click_event = fish.get_click()
                self.event_list.append(click_event)
            self.fishing.bar.kill()
            self.fishing.__delattr__('bar')
            self.player.update('reset')
            self.player.rect.center = (230, 210)

    def run(self, event):
        self.set_object('player', self.player)
        self.set_object('player', self.money)
        while self.RUNNING:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if len(self.event_list) > 0:
                    for e in self.event_list:
                        a = e(self.set_object, self.objects['fish'][1][len(self.objects['fish'][1]) - 1],
                              pygame.mouse.get_pos(), pygame.mouse.get_pressed(), self.money)
                        if a:
                            self.event_list.pop()
                if event.type == pygame.KEYDOWN:
                    self.player.act_handler(event, self.set_object)
            self.handle_fishing(event)
            self.event_handler(event)
            self.screen.fill((255, 255, 255))
            self.screen.blit(Config.BG_IMG, (0, self.INTERFACE[1]))
            self.player.handle_event(event)
            self.draw_sprites(self.objects)
            self.blit_surface()
            open_shop(Game.handle_shop, self.money.rect, Game.is_shop_on)
            self.corn.draw(self.screen)
            self.corn.update()
            pygame.display.update()
        if not self.RUNNING:
            pygame.display.quit()
            pygame.quit()


menuImg = pygame.image.load("images/farm.jpg")

black = (0, 0, 0)
font_title = 'font/dimbo_regular.ttf'
font_name = 'font/dimbo_regular.ttf'
width = 1024
height = 768
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

game_display = Game()
game_display = game_display.screen


def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def message_display(text):
    largetext = pygame.font.Font(font_title, 70)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((width / 2), (height / 2))
    game_display.blit(textsurf, textrect)

    pygame.display.update()

    time.sleep(2)


def farm(x1, y1):
    game_display.blit(menuImg, (x1, y1))


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                return "stop"
            elif action == "quit":
                pygame.quit()

    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))
    pygame.font.init()
    smalltext = pygame.font.Font('font/dimbo_regular.ttf', 40)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2), y + (h / 2)))
    game_display.blit(textsurf, textrect)


def game_intro(run):
    x1 = (width * 0)
    y1 = (height * 0)
    intro = True
    x = (width * .37)
    y = (height * .19)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        if intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            farm(x1, y1)

            largetext = pygame.font.Font('font/dimbo_regular.ttf', 70)
            textsurf, textrect = text_objects("PyFarm", largetext)
            textrect.center = ((width / 2), (height / 3))
            game_display.blit(textsurf, textrect)
            t = button("START", 150, 550, 100, 50, white, green, "play")
            if t == 'stop':
                intro = False
            button("QUIT", 750, 550, 100, 50, white, red, "quit")
            pygame.display.update()
        else:
            # game_display.fill(black)
            run(event)
            # clock.tick(30)
