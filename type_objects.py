import math
import random
import numpy as np
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    KEYDOWN,
    K_SPACE,
    K_ESCAPE,
    QUIT,
)


RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D


g = 1
k = 1 # В будущем можно поправить, чтоб вверх ногами летало

WIDTH = 800
HEIGHT = 600
FPS = 30



class triangle:
    def __init__(self, x, y , screen,angle = 0):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle)
        self.screen = screen
        self.vx = -7
        self.h = float(30)
        self.l = float(15)
        self.color = BLACK
    def move(self):
        self.x = self.x + self.vx
    def draw(self):
        if self.angle == 0:
            pygame.draw.polygon(self.screen, self.color,[[self.x-self.l , self.y],[self.x+self.l, self.y],[self.x, self.y-self.h]] )
        if self.angle == 3.1415926:
            pygame.draw.polygon(self.screen, self.color,[[self.x, self.y],[self.x+self.l, self.y - self.h],[self.x - self.l, self.y-self.h]])

class Rectangle:
    def __init__(self, x, y, screen, h = 30, l = 30):
        self.x = float(x)
        self.y = float(y)
        self.screen = screen
        self.vx = -7
        self.h = float(h)
        self.l = float(l)
        self.color = CYAN
    def move(self):
        self.x = self.x + self.vx
    def draw(self):
        pygame.draw.polygon(self.screen, self.color,[[self.x - self.l/2, self.y - self.h],[self.x + self.l/2, self.y - self.h],[self.x + self.l/2, self.y], [self.x - self.l/2, self.y]] )

class Portal:
    def __init__(self,x, y,type,screen):
        # Центр низа портала
        self.x = float(x)
        self.y = float(y)
        self.type = type
        self.screen = screen
        self.vx = -7
        if type == 'plane':
            self.color = BLUE
        elif type == 'square':
            print(1)
            self.color = GREEN
        elif type == 'ufo':
            self.color = RED
    def draw(self):
        pygame.draw.ellipse(self.screen, self.color, (self.x, self.y - 100, 15, 100), 2)
    def move(self):
        self.x = self.x + self.vx