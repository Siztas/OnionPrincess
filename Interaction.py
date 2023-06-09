import pygame
from settings import *


class NPC(pygame.sprite.Sprite):
    def __init__(self,pos,groups,surface,player):
        super().__init__(groups)
        self.sprite_type = 'NPC'
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.cool_down = 400
        self.player = player


    def creat_chat(self):
        print('chat')

class Transmit(pygame.sprite.Sprite):
    def __init__(self,pos,groups,surface,player,level):
        super().__init__(groups)
        self.sprite_type = 'Transmit'
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.cool_down = 400
        self.player = player
        self.level = level


    def creat_chat(self):
        pass




