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



class Player(pygame.sprite.Sprite):
    def __init__(self, y = 450):
        super(Player, self).__init__()
        self.surf = pygame.image.load("/Users/forcs2/Desktop/Geometry_dash/x210.jpg").convert()
        self.x = 1/4 *WIDTH
        self.y = y
        self.angle = 0
        self.rect = self.surf.get_rect(
            center=(self.x, self.y)
        )
        self.v = 0


    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if self.v != 0:
            self.rect.move_ip(0, self.v)
            self.y += self.v
            self.angle = 57.29578 * math.atan2(-self.v, 30)
            self.rotate()
        if pressed_keys[K_SPACE]:
            self.v = self.v - 2
        self.v = self.v + 1
        if self.rect.bottom >= 3/4*HEIGHT and self.v >= 0:
            self.rect.bottom = 3/4*HEIGHT
            self.v = 0
            self.angle += 5
            if self.angle > -1:
                self.angle = 0
                self.y = self.rect.centery
                self.x = self.rect.centerx
            self.rotate3()
        if self.rect.top <= 0 and self.v <= 0:
            self.rect.top = 0
            self.v = 0
            self.angle = self.angle - 5
            if self.angle < 1:
                self.angle = 0
                self.y = self.rect.centery
                self.x = self.rect.centerx
            self.rotate2()

    def rotate(self):
        self.surf = pygame.transform.rotate(pygame.image.load("/Users/forcs2/Downloads/spiral.png").convert(), self.angle)
        self.rect = self.surf.get_rect(
            center=(self.x, self.y)
        )

    def rotate2(self):
        self.surf = pygame.transform.rotate(pygame.image.load("/Users/forcs2/Downloads/spiral.png").convert(), self.angle)
        self.rect = self.surf.get_rect(
            centerx=self.x,
            top=self.rect.top
        )

    def rotate3(self):
        self.surf = pygame.transform.rotate(pygame.image.load("/Users/forcs2/Downloads/spiral.png").convert(), self.angle)
        self.rect = self.surf.get_rect(
            centerx=self.x,
            bottom=self.rect.bottom
        )





class UFO:
    def __init__(self, screen, x = 1/4 * WIDTH, y = 3/4 * HEIGHT - 15):
        #Размер
        self.a = 15
        # Положение
        self.x = x
        self.y = y
        # Угол поворота
        self.angle = 0
        # Скорости
        self.vx = 0
        self.vy = 0
        self.omega = 0
        self.color = YELLOW
        self.screen = screen
    def draw(self):
        pygame.draw.lines(self.screen, self.color, True, [(self.x - self.a,self.y + self.a/3),
                                                          (self.x + self.a, self.y + self.a/3),
                                                          (self.x + self.a ,self.y + self.a),
                                                          (self.x - self.a ,self.y + self.a)], 2)
        pygame.draw.arc(self.screen, self.color, (self.x - 3/4*self.a, self.y - 3/4 *self.a , 3 * self.a/2,8*  self.a/3 ),0,  3.1415926,2)

    def oppor_jump(self):
            return True

    def jump(self):
        if self.oppor_jump() == True:
            self.vy = -12
            self.omega = 0

    def stop_jump(self):
        self.vy = 0
        self.omega = 0
        self.angle = 0

    def move(self, floor_position, ceil_position):
        # Штуки с полом: первая
       # print(ceil_position)
        if self.y + self.a > floor_position:
            self.y = floor_position - self.a
            self.omega = 0
            self.vy = 0
            self.angle = 0
        elif self.y + self.a == floor_position:
            self.y = self.y + self.vy
            self.angle = self.angle + self.omega
        else:
            self.y = self.y + self.vy
            self.vy = self.vy + g
            self.angle = self.angle + self.omega

        if ceil_position >= self.y - self.a:
            #print(ceil_position)
            self.y = self.a + ceil_position + self.a/2

class Player_Square:
    def __init__(self, screen, x = 1/4 * WIDTH, y = 3/4 * HEIGHT - 15):
        #Размер
        self.a = 15
        # Положение
        self.x = x
        self.y = y
        # Угол поворота
        self.angle = 0
        # Скорости
        self.vx = 0
        self.vy = 0
        self.omega = 0
        self.color = BLACK
        self.screen = screen
    def draw(self):
        pygame.draw.lines(self.screen, self.color, True, [(self.x - self.a*(np.cos(self.angle) - np.sin(self.angle)),
                                                            self.y + self.a* (np.cos(self.angle) + np.sin(self.angle))),
                                                          (self.x + self.a * (np.cos(self.angle) + np.sin(self.angle)),
                                                           self.y + self.a * (np.cos(self.angle) - np.sin(self.angle))),
                                                          (self.x + self.a * (np.cos(self.angle) - np.sin(self.angle)),
                                                           self.y - self.a * (np.cos(self.angle) + np.sin(self.angle))),
                                                          (self.x - self.a * (np.cos(self.angle) + np.sin(self.angle)),
                                                           self.y - self.a * (np.cos(self.angle) - np.sin(self.angle)))], 1 )

    def oppor_jump(self, Rectangles, floor_pos):
        if self.y == 3/4 * HEIGHT - self.a:
            return True
        for r in Rectangles:
            if abs(r.x - self.x) < self.a + r.l/2 and floor_pos == self.y + self.a:
                return True
        return False

    def jump(self, Rectangles ,floor_pos):
        if self.oppor_jump(Rectangles , floor_pos) == True:
            self.vy = -12
            self.omega = -0.15

    def stop_jump(self):
        self.vy = 0
        self.omega = 0
        self.angle = 0

    def move(self, floor_position):
        if self.y + self.a > floor_position:
            self.y = floor_position - self.a
            self.omega = 0
            self.vy = 0
            self.angle = 0
        elif self.y + self.a == floor_position:
            self.y = self.y + self.vy
            self.angle = self.angle + self.omega
        else:
            self.y = self.y + self.vy
            self.vy = self.vy + g
            self.angle = self.angle + self.omega