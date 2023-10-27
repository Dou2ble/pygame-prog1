#!/usr/bin/env python3

import pygame

import resources

# the player should be a game.playere but due to python limitation i cannot type it
def render_hud(player) -> pygame.Surface:
  surf = pygame.Surface((resources.TOTAL_W, resources.TOTAL_H), pygame.SRCALPHA)

  text = resources.FONT_THALEAH.render(f"health: {player.health}", True, resources.COLOR_TEXT) 
  text_rect = text.get_rect()
  text_rect.y += resources.TOTAL_H-resources.FONT_SIZE

  surf.blit(text, text_rect)

  return surf