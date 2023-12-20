# -*- coding: utf-8 -*-
"""main2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mYeO0DqyOPheW1TJPlcv_nTreeWwY08A
"""

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

f = open('/Users/forcs2/Downloads/LEVEL1.txt', 'r')
#LEVEL = f.read()
LEVEL = '600, 450, portal, plane;800, 450, rect, 100, 60;785, 350, tr;815, 350, tr'
LEVEL = LEVEL.replace(' ','')

import type_objects
import type_players

def find_floor_pos(player, Rectangles):
    Floor = [3/4 * HEIGHT]
    for r in Rectangles:
        if r.y < player.y + player.a:
            continue
        if abs(r.x - player.x) >  r.l / 2:
            continue
        Floor.append(r.y - r.h)
    Floor.sort()
    return Floor[0]

def find_ceil_pos(player, Rectangles):
    Ceil = [0]
    for r in Rectangles:
        if r.y > player.y + player.a:
            continue
        if abs(r.x - player.x) >  r.l / 2:
            continue
        Ceil.append(r.y)
    Ceil.sort()
    return Ceil[-1]


def intersection(x1, y1, angle1, l1, h1, x2, y2, angle2, l2, h2):
    angle = angle1 - angle2
    x = x1 - x2
    y = y1 - y2

    if abs(x + h1 / 2 * np.cos(angle) + l1 / 2 * np.sin(angle)) < l2/2 and abs(y + h1 / 2 * np.sin(angle) - l1 / 2 * np.cos(angle)) < h2/2:
        return False
    elif abs(x - h1 / 2 * np.cos(angle) + l1 / 2 * np.sin(angle)) < l2/2 and abs(y - h1 / 2 * np.sin(angle) - l1 / 2 * np.cos(angle)) < h2/2:
        return False
    elif abs(x - h1 / 2 * np.cos(angle) - l1 / 2 * np.sin(angle)) < l2/2 and abs(y - h1 / 2 * np.sin(angle) + l1 / 2 * np.cos(angle)) < h2/2:
        return False
    elif abs(x + h1 / 2 * np.cos(angle) - l1 / 2 * np.sin(angle)) < l2/2 and abs(y + h1 / 2 * np.sin(angle) + l1 / 2 * np.cos(angle)) < h2/2:
        return False
    angle = angle2 - angle1
    x = x2 - x1
    y = y2 - y1
    if abs(x + h2 / 2 * np.cos(angle) + l2 / 2 * np.sin(angle)) < l1/2 and abs(y + h2 / 2 * np.sin(angle) - l2 / 2 * np.cos(angle)) < h1/2:
        return False
    elif abs(x - h2 / 2 * np.cos(angle) + l2 / 2 * np.sin(angle)) < l1/2 and abs(y - h2 / 2 * np.sin(angle) - l2 / 2 * np.cos(angle)) < h1/2:
        return False
    elif abs(x - h2 / 2 * np.cos(angle) - l2 / 2 * np.sin(angle)) < l1/2 and abs(y - h2 / 2 * np.sin(angle) + l2 / 2 * np.cos(angle)) < h1/2:
        return False
    elif abs(x + h2 / 2 * np.cos(angle) - l2 / 2 * np.sin(angle)) < l1/2 and abs(y + h2 / 2 * np.sin(angle) + l2 / 2 * np.cos(angle)) < h1/2:
        return False
    else:
        return True






pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
Floor_position = 3/4 * HEIGHT
TYPE_PLAYER = 'square'

Level_massive = LEVEL.split(';')

image1 = pygame.image.load("/Users/forcs2/Desktop/Background.png")
image2 = pygame.image.load("/Users/forcs2/Desktop/Ground.png")

# Масштабирование картинок до размеров окна
image1 = pygame.transform.scale(image1, (WIDTH, HEIGHT))
image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))


def make_level(Level_massive):
    Triangles = []
    Rectangles = []
    Portals = []
    #Добавление всякой херни в массивы
    for i in Level_massive:
        obj = i.split(',')
        if obj[2] == 'tr':
            if len(obj) == 3:
                t = type_objects.triangle(obj[0], obj[1], screen)
                Triangles.append(t)
            elif len(obj) == 4:
                t = type_objects.triangle(obj[0], obj[1], screen, obj[3])
                Triangles.append(t)
        elif obj[2] == 'rect':
            rect = type_objects.Rectangle(obj[0], obj[1], screen, obj[3], obj[4])
            Rectangles.append(rect)

        elif obj[2] == 'portal':
            port = type_objects.Portal(obj[0], obj[1], obj[3], screen)
            Portals.append(port)
    return Triangles, Rectangles, Portals


def main():
    player_sq = type_players.Player_Square(screen)
    player_ufo = type_players.UFO(screen)
    player_pl = type_players.Player()

    Jump = False
    type_player = TYPE_PLAYER
    floor_position = Floor_position
    finished = False

    Triangles, Rectangles, Portals = make_level(Level_massive)

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
                    main()
            if type_player == 'ufo':
                if abs(r.x - r.l / 2 - player_ufo.x - player_ufo.a) <= 7 and abs(r.y - r.h / 2 - player_ufo.y) < r.h /2  + player_ufo.a:
                    main()
            if type_player == 'plane':
                #Поправить, чтоб был самолет

                if not intersection(player_pl.x, player_pl.rect.bottom,0, player_pl.rect.width,player_pl.rect.height, r.x, r.y, 0, r.l,r.h):
                    main()

        #нахождение пола, потолка
        if type_player == 'square':
            floor_position = find_floor_pos(player_sq, Rectangles)
        if type_player == 'ufo':
            floor_position = find_floor_pos(player_ufo, Rectangles)
        if type_player == 'square':
            ceil_position = find_ceil_pos(player_sq, Rectangles)
        if type_player == 'ufo':
            ceil_position = find_ceil_pos(player_ufo, Rectangles)

        #Рисование порталов, преобразование типа игрока
        for p in Portals:
            p.draw()
            if type_player == 'square':
                if not intersection(player_sq.x, player_sq.y,player_sq.angle, player_sq.a* 2, player_sq.a * 2, p.x, p.y, 0, 10, 200):
                    type_player = p.type
                    if p.type == 'ufo':
                        player_ufo = type_players.UFO(screen, player_sq.x, player_sq.y)
                    if p.type == 'square':
                        player_sq = type_players.Player_Square(screen, player_sq.x, player_sq.y)
                    if p.type == 'plane':
                        player_pl = type_players.Player(player_sq.y)

            if type_player == 'ufo':
                if not intersection(player_ufo.x, player_ufo.y,player_ufo.angle, player_ufo.a* 2, player_ufo.a * 2, p.x, p.y, 0, 10, 200):
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
                if not intersection(player_pl.x, player_pl.rect.bottom,0, 30,30, p.x, p.y, 0, 10,200):
                    type_player = p.type
                    if p.type == 'ufo':
                        player_ufo = type_players.UFO(screen, player_pl.x, player_pl.rect.bottom)
                    if p.type == 'square':
                        player_sq = type_players.Player_Square(screen, player_pl.x, player_pl.rect.bottom)

        for t in Triangles:
            t.draw()
            if type_player == 'square':
                if not intersection(player_sq.x, player_sq.y,player_sq.angle, player_sq.a* 2, player_sq.a * 2, t.x, t.y, t.angle, t.l, t.h ):
                    main()
            if type_player == 'ufo':
                if not intersection(player_ufo.x, player_ufo.y,player_ufo.angle, player_ufo.a* 2, player_ufo.a * 2, t.x, t.y, t.angle, t.l, t.h ):
                    main()
            if type_player == 'plane':
                if not intersection(player_pl.x, player_pl.rect.bottom,0, 30,30, t.x, t.y, 0, t.l,t.h):
                    main()


        clock.tick(FPS)
        if type_player == 'plane':
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        running = False

        # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = False
            pressed_keys = pygame.key.get_pressed()
            player_pl.update(pressed_keys)
            #screen.blit(player_pl.surf, player_pl.rect)
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
main()