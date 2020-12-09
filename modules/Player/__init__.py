import pygame

from modules.Config import FARMER_SHEET, FARMER_IMG, FISHING_IMG
from modules.Object import Object


class Farmer(Object):
    def __init__(self):
        self.left_states = {0: (1850, 7, 55, 72), 1: (1770, 6, 55, 72), 2: (1691, 6, 55, 72), 3: (1610, 6, 55, 72)}
        self.right_states = {0: (13, 6, 55, 70), 1: (93, 6, 55, 72), 2: (173, 6, 55, 72), 3: (253, 6, 55, 72)}
        self.up_states = {0: (13, 404, 55, 72), 1: (93, 404, 55, 72), 2: (173, 404, 55, 72), 3: (253, 404, 55, 72)}
        self.down_states = {0: (491, 404, 55, 72), 1: (570, 404, 55, 72), 2: (651, 404, 55, 72), 3: (732, 404, 55, 72)}
        Object.__init__(self, FARMER_IMG, 500, 350, self.left_states, self.right_states, self.up_states,
                        self.down_states,
                        FARMER_SHEET)
        self.block_area = []
        self.sell_area = []
        self.act_target = "default"
        self.is_auto = False
        self.fishing_mod = False

    def set_fishing_mod(self, fishing_mod):
        if fishing_mod:
            self.image = FARMER_IMG
        else:
            self.image = FISHING_IMG

    def handle_event(self, event):
        act = True
        if len(self.block_area) > 0:
            for block in self.block_area:
                block = block.get_rect() if type(block) is not pygame.Rect else block
                if self.rect.colliderect(block):
                    if self.rect.top <= block.bottom:
                        self.rect.y += 10
                    elif self.rect.right >= block.left:
                        self.rect.x -= 10
                    elif self.rect.left <= block.right:
                        self.rect.x += 100
                    elif self.rect.bottom <= block.top:
                        self.rect.y -= 10
                    act = False

        if event.type == pygame.KEYDOWN and act:
            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')

    def add_block_area(self, *stuff):
        # print(type(stuff))
        self.block_area.extend(stuff)

    def add_sell_area(self, *stuff):
        self.sell_area.extend(stuff)

    def act_handler(self, event, handler):
        if len(self.sell_area) > 0:
            for block in self.sell_area:
                block_rect = block.get_sell_rect() if type(block) is not pygame.Rect else block
                if block_rect.contains(self.rect) or block_rect.colliderect(self.rect):
                    print(block)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            block.add(handler)
