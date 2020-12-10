from os import path

import pygame

ROOT_DIR = path.dirname(path.dirname(__file__))
images_folder = path.join(ROOT_DIR, "images")
img = pygame.image.load(path.join(images_folder, 'money.png'))

BG_IMG = pygame.image.load(path.join(images_folder, 'BG_IMG.png'))
FARMER_IMG = pygame.image.load(path.join(images_folder, 'FARMER_IMG.png'))
FISHING_IMG = pygame.transform.scale(pygame.image.load(path.join(images_folder, 'fishing.png')), (130, 140))
FARMER_SHEET = pygame.image.load(path.join(images_folder, 'FARMER_SHEET.png'))

CHICKEN_IMG = pygame.image.load(path.join(images_folder, 'chicken.png'))
SHEEP_IMG = pygame.image.load(path.join(images_folder, 'sheep.png'))
FISH_IMG = [
    pygame.image.load(path.join(images_folder, 'smallfish.png')),
    pygame.image.load(path.join(images_folder, 'mediumfish.png')),
    pygame.image.load(path.join(images_folder, 'largefish.png'))]

CORN_IMG = [
    pygame.image.load(path.join(images_folder, 'corn_start.png')),
    pygame.image.load(path.join(images_folder, 'corn_mid.png')),
    pygame.image.load(path.join(images_folder, 'corn_full_2.png'))]

pygame.font.init()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('font/retro.ttf', size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Money(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((0, 10), (60, 60))
        self.image = img
        self.point = 0
        self.is_drawable = True

    def draw_self(self, screen):
        draw_text(screen, str(self.point), 65, 70 + int(len(str(self.point)) * 10), 12)

# class
