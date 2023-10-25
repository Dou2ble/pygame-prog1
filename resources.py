#!/usr/bin/env python3

import pygame

TOTAL_W = 1280
TOTAL_H = 720

TEXTURE_BACKGROUND = pygame.image.load("background.png")
TEXTURE_SCALED_BACKGROUND = pygame.transform.scale(TEXTURE_BACKGROUND, (TOTAL_W, TOTAL_H))

TEXTURE_ENEMY = pygame.image.load("enemy.png")
TEXTURE_SCALED_ENEMY = pygame.transform.scale(TEXTURE_ENEMY, (32, 32))
TEXTURE_SCALED_ENEMY = pygame.transform.scale(TEXTURE_ENEMY, (32, 32))
TEXTURE_SCALED_FLIPPED_ENEMY = pygame.transform.flip(TEXTURE_SCALED_ENEMY, True, False)

pygame.font.init()
FONT_SIZE = 32
FONT_THALEAH = pygame.font.Font("ThaleahFat.ttf", FONT_SIZE)

COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_TRANSPARENT = (0, 0, 0, 0)
