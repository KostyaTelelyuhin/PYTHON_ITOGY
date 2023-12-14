# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MUHE_GrxOFfGBcpUrDLqOntvD1YOAWRF

Hello

"""

import math
import random
import numpy as np
import pygame


RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D


g = 10
k = 1 # В будущем можно поправить, чтоб вверх ногами летало

WIDTH = 800
HEIGHT = 600
FPS = 30
class Square:
    def __init__(self, screen):
        #Размер
        self.a = 10
        # Положение
        self.x = 1/4 * WIDTH
        self.y = 3/4 * HEIGHT - self.a
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

    def oppor_jump(self):
        if self.y == 3/4 * HEIGHT - self.a:
            return True
        # Дописать, чтоб можно было от квадратов прыгать
        return False

    def jump(self):
        if self.oppor_jump() == True:
            self.vy = -30
            self.omega = -0.15

    def move(self):
        if self.y + self.a > 3/4 * HEIGHT:
            self.y = 3/4 * HEIGHT - self.a
            self.omega = 0
            self.vy = 0
            self.angle = 0
        elif self.y + self.a == 3/4 * HEIGHT:
            self.y = self.y + self.vy
            self.angle = self.angle + self.omega
        else:
            self.y = self.y + self.vy
            self.vy = self.vy + g
            self.angle = self.angle + self.omega


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = Square(screen)
finished = False
while not finished:
    screen.fill(WHITE)
    player.draw()
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONUP:
            player.jump()
    player.move()
    #pygame.draw.line(screen, BLACK, (1, 3/4*HEIGHT), (WIDTH, 3/4*HEIGHT), 2)
    pygame.display.update()