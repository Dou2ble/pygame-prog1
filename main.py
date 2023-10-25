#!/usr/bin/env python3

# Example file showing a basic pygame "game loop"
import pygame
import sys

import game
import hud

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

def mainloop() -> None:
    running = True

    previous_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - previous_time) / 1000.0  # Delta time in seconds
        previous_time = current_time

        running = game.update_game(pygame.event.get(), dt)
        game_surface = game.render_game()
        screen.blit(game_surface, (0, 0))
        

        # flip() the display to put your work on screen
        pygame.display.flip()

def quit() -> None:
    pygame.quit()
    sys.exit(0)

def main() -> None:
    mainloop()
    quit()

if __name__ == "__main__":
    main()
