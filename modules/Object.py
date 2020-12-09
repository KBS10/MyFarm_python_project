import random
import pygame
from os import path
import modules.Config

directions = ['left', 'right', 'up', 'down']


class Object(pygame.sprite.Sprite):
    def __init__(self, image, width, height, left_states={}, right_states={}, up_states={}, down_states={}, sheet=None,
                 area=(0, 1024, 80, 848)):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.sheet = image if sheet is None else sheet
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.last = pygame.time.get_ticks()
        self.count = 0
        self.area_left, self.area_right, self.area_top, self.area_bottom = area
        self.is_auto = True

        # define how do working rectangles
        self.left_states = left_states  # x y width height
        self.right_states = right_states
        self.up_states = up_states
        self.down_states = down_states

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        if direction == 'left':
            self.rect.x -= 10 if self.rect.left > self.area_left else 0
        if direction == 'right':
            self.rect.x += 10 if self.rect.right < self.area_right else 0
        if direction == 'up':
            self.rect.y -= 10 if self.rect.top > self.area_top else 0
        if direction == 'down':
            self.rect.y += 10 if self.rect.bottom < self.area_bottom else 0
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

    def auto_move(self):
        self.count = (self.count + 1) % 8
        if self.count == 0:
            self.update(random.choice(directions))

    def auto(self):
        self.auto_move()


if __name__ == "__main__":
    pass
