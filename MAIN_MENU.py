# -*- coding: utf-8 -*-
"""TYPE_OBJECTS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IGGI6db5pljA5k15aofnAexAOJ_EKm4u
"""

import math
import random
import numpy as np
import pygame
import random
import sys

from pygame.locals import (
    RLEACCEL,
    KEYDOWN,
    K_SPACE,
    K_ESCAPE,
    QUIT,
)

import type_objects
import type_players
import Functions_from_main


RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D



pygame.init()
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

g = 1
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))


main_menu_image = pygame.image.load("/Users/forcs2/Desktop/Geometry_dash/MAIN_MENU.png")

f1 = open('/Users/forcs2/Desktop/Geometry_dash/LEVEL1.txt', 'r')
LEVEL1 = f1.read()
LEVEL1 = LEVEL1.replace(' ', '')

class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
def level(LEVEL):
    Floor_position = 3/4 * HEIGHT
    TYPE_PLAYER = 'square'

    Level_massive = LEVEL.split(';')

    image1 = pygame.image.load("/Users/forcs2/Desktop/Geometry_dash/Background.png")
    image2 = pygame.image.load("/Users/forcs2/Desktop/Geometry_dash/Ground.png")
    image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))
    image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))



    player_sq = type_players.Player_Square(screen)
    player_ufo = type_players.UFO(screen)
    player_pl = type_players.Player()

    Jump = False
    type_player = TYPE_PLAYER
    floor_position = Floor_position
    finished = False

    Triangles, Rectangles, Portals = Functions_from_main.make_level(Level_massive)

    while not finished:

        screen.blit(image1, (0, -HEIGHT//4))
        screen.blit(image2, (0, HEIGHT//4*3))

        if type_player == 'square':
            player_sq.draw()
        if type_player == 'ufo':
            player_ufo.draw()
        if type_player == 'plane':
            screen.blit(player_pl.surf, player_pl.rect)


        for r in Rectangles:
            r.draw()
            #столкновение с прямоугольниками
            if type_player == 'square':
                if abs(r.x - r.l / 2 - player_sq.x - player_sq.a) <= 7 and abs(r.y - r.h / 2 - player_sq.y) < r.h /2  + player_sq.a:
                    level(LEVEL)
            if type_player == 'ufo':
                if abs(r.x - r.l / 2 - player_ufo.x - player_ufo.a) <= 7 and abs(r.y - r.h / 2 - player_ufo.y) < r.h /2  + player_ufo.a:
                    level(LEVEL)
            if type_player == 'plane':
                #Поправить, чтоб был самолет

                if not Functions_from_main.intersection(player_pl.x, player_pl.rect.bottom,0, player_pl.rect.width,player_pl.rect.height, r.x, r.y, 0, r.l,r.h):
                    level(LEVEL)

        #нахождение пола, потолка
        if type_player == 'square':
            floor_position = Functions_from_main.find_floor_pos(player_sq, Rectangles)
        if type_player == 'ufo':
            floor_position = Functions_from_main.find_floor_pos(player_ufo, Rectangles)
        if type_player == 'square':
            ceil_position = Functions_from_main.find_ceil_pos(player_sq, Rectangles)
        if type_player == 'ufo':
            ceil_position = Functions_from_main.find_ceil_pos(player_ufo, Rectangles)

        #Рисование порталов, преобразование типа игрока
        for p in Portals:
            p.draw()
            if type_player == 'square':
                if not Functions_from_main.intersection(player_sq.x, player_sq.y,player_sq.angle, player_sq.a* 2, player_sq.a * 2, p.x, p.y, 0, 10, 200):
                    type_player = p.type
                    if p.type == 'ufo':
                        player_ufo = type_players.UFO(screen, player_sq.x, player_sq.y)
                    if p.type == 'square':
                        player_sq = type_players.Player_Square(screen, player_sq.x, player_sq.y)
                    if p.type == 'plane':
                        player_pl = type_players.Player(player_sq.y)

            if type_player == 'ufo':
                if not Functions_from_main.intersection(player_ufo.x, player_ufo.y,player_ufo.angle, player_ufo.a* 2, player_ufo.a * 2, p.x, p.y, 0, 10, 200):
                    type_player = p.type
                    if p.type == 'ufo':
                        player_ufo = type_players.UFO(screen, player_ufo.x, player_ufo.y)
                    if p.type == 'square':
                        player_sq = type_players.Player_Square(screen, player_ufo.x, player_ufo.y)
                    if p.type == 'plane':
                        # На волю всевышнего
                        player_pl = type_players.Player(player_ufo.y)
            if type_player == 'plane':
                #Поправить!!
                if not Functions_from_main.intersection(player_pl.x, player_pl.rect.bottom,0, 30,30, p.x, p.y, 0, 10,200):
                    type_player = p.type
                    if p.type == 'ufo':
                        player_ufo = type_players.UFO(screen, player_pl.x, player_pl.rect.bottom)
                    if p.type == 'square':
                        player_sq = type_players.Player_Square(screen, player_pl.x, player_pl.rect.bottom)

        for t in Triangles:
            t.draw()
            if type_player == 'square':
                if not Functions_from_main.intersection(player_sq.x, player_sq.y,player_sq.angle, player_sq.a* 2, player_sq.a * 2, t.x, t.y, t.angle, t.l, t.h ):
                    level(LEVEL)
            if type_player == 'ufo':
                if not Functions_from_main.intersection(player_ufo.x, player_ufo.y,player_ufo.angle, player_ufo.a* 2, player_ufo.a * 2, t.x, t.y, t.angle, t.l, t.h ):
                    level(LEVEL)
            if type_player == 'plane':
                if not Functions_from_main.intersection(player_pl.x, player_pl.rect.bottom,0, 30,30, t.x, t.y, 0, t.l,t.h):
                    level(LEVEL)


        clock.tick(FPS)
        if type_player == 'plane':
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                elif event.type == QUIT:
                    running = False
            pressed_keys = pygame.key.get_pressed()
            player_pl.update(pressed_keys)
            pygame.display.flip()


        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    Jump = True
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                    Jump = False
                if Jump:
                    if type_player == 'square':
                        player_sq.jump(Rectangles, floor_position)
                    if type_player == 'ufo':
                        player_ufo.jump()

        if type_player == 'square':
            player_sq.move(floor_position)
            player_sq.move(floor_position)
        if type_player == 'ufo':
            player_ufo.move(floor_position, ceil_position)
            player_ufo.move(floor_position, ceil_position)
        for p in Portals:
            p.move()
            p.move()
        num_tr = len(Triangles)
        for i in range(num_tr):
            Triangles[i].move()
            Triangles[i].move()
        for r in Rectangles:
            r.move()
            r.move()
        #pygame.draw.line(screen, BLACK, (1, 3/4*HEIGHT), (WIDTH, 3/4*HEIGHT), 2)
        pygame.display.update()



def open_window_creative():

    new_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Креатив")


    #button1_cr = Button(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, white, "Амогус")
    button2_cr = Button(0, 0, 800, 600, white, "Для продолжения необходимо заплатить денюжку", main_menu)
    #button3_cr = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, white, "Цифра или Арктика?")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    button2_cr.check_click(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main_menu()

        new_window.fill(BLACK)
       # button1_cr.draw()
        button2_cr.draw()
       # button3_cr.draw()
        pygame.display.update()

def fun1():
    level(LEVEL1)
def fun2():
    level(LEVEL2)
def fun3():
    level(LEVEL3)


def open_window_level():
    # Создание нового окна
    new_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Уровни")

    # Кнопки в новом окне
    button1_lv = Button(250, 100, 350, 50, white, "Просто песенка про пиво", fun1)
    button2_lv = Button(WIDTH // 2 - 100, HEIGHT // 2, 270, 50, white, "Физтех", fun2)
    button3_lv = Button(WIDTH // 2 - 100, 500, 270, 50, white, "Цифра или Арктика?", fun3)
    time_skip = 0
    # Основной цикл нового окна
    while True:
        time_skip = time_skip + 1

        if time_skip < 20:
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    button1_lv.check_click(pos)
                    button2_lv.check_click(pos)
                    button3_lv.check_click(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main_menu()
        new_window.fill(BLUE)
        button1_lv.draw()
        button2_lv.draw()
        button3_lv.draw()
        pygame.display.update()


def main_menu():
    button1 = Button(30, 110, 160, 160, white, "Скины", open_window_creative)
    button2 = Button(270, 70, 250, 250, white, "Уровни", open_window_level)
    button3 = Button(580, 110, 160, 160, white, "Креатив", open_window_creative)
    screen.blit(main_menu_image, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    button1.check_click(pos)
                    button2.check_click(pos)
                    button3.check_click(pos)

        pygame.display.update()


main_menu()