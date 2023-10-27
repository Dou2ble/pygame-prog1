#!/usr/bin/env python3

import math
import random

import pygame
import hud

import resources
import utils


# A entity consists of a x and y coordinates and a rotation wich is in degrees (0 is up, 180 is down)
class Entity():
    def __init__(self, x: float, y: float, rotation: float) -> None:
        self.x = x
        self.y = y
        self.rotation = rotation
    
    def rotate_to(self, x: float, y: float) -> None:
        # if the target and entity are too close to eachother skip the rotation
        if utils.distance((self.x, self.y), (x, y)) < 5:
            return

        # Calculate the difference in the x and y coordinates
        dx = x - self.x
        dy = y - self.y

        angle_radians = math.atan2(dy, dx)
        self.rotation = math.degrees(angle_radians) + 90
        # so that we don't get any negative values
        self.rotation %= 360

    def move(self, dt: float, speed: float) -> None:
        rad = math.radians(self.rotation - 90)

        dx = speed * math.cos(rad) * dt
        dy = speed * math.sin(rad) * dt

        self.x += dx
        self.y += dy


PLAYER_SIZE = 35
PLAYER_SPEED = 300.0
PLAYER_GUN_COOLDOWN = 0.05
class Player(Entity):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 0.0)

        self.health = 10
        # the gun delay is used to make sure that the player can't shoot every frame
        # every frame gun_delay is set dt lowe until the player can shoot again (it hits 0)
        self.gun_delay = PLAYER_GUN_COOLDOWN


    def to_rect(self) -> tuple[int, int, int, int]:
        return (int(player.x - PLAYER_SIZE/2), int(player.y - PLAYER_SIZE/2), PLAYER_SIZE, PLAYER_SIZE)

BULLET_SIZE = 5
BULLET_SPEED = 1000.0
BULLET_COLOR = (255, 174, 0)
class Bullet(Entity):
    def __init__(self, x: float, y: float, rotation: float, spread: bool = False) -> None:
        super().__init__(x, y, rotation)

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, BULLET_COLOR, (int(self.x), int(self.y)), BULLET_SIZE)

ENEMY_RADIUS = 16
class Enemy(Entity):
    def __init__(self, x: float, y: float, rotation: float, hp: int) -> None:
        super().__init__(x, y, rotation)
        self.speed = PLAYER_SPEED * random.uniform(0.5, 0.7)
        self.hp = hp

    def hit(self, damage: int = 1) -> None:
        self.hp -= damage
    
    def move(self, dt) -> None:
        super().move(dt, self.speed)

    def draw(self, surf) -> None:
        if self.rotation > 0 and self.rotation < 180:
            surf.blit(resources.TEXTURE_SCALED_FLIPPED_ENEMY, (self.x - ENEMY_RADIUS, self.y - ENEMY_RADIUS))
        else:
            surf.blit(resources.TEXTURE_SCALED_ENEMY, (self.x - ENEMY_RADIUS, self.y - ENEMY_RADIUS))

player = Player(100, 100)
bullets: list[Bullet] = []

ENEMIES_SPAWN_COOLDOWN = 1 # higher number -> slower spawning
# how far away enemies should spawn from the player
ENEMY_SPAWN_DISTANCE = 200
enemies_spawn_delay = ENEMIES_SPAWN_COOLDOWN*2
enemies: list[Enemy] = []

def render_game() -> pygame.Surface:
    surf = pygame.Surface((resources.TOTAL_W, resources.TOTAL_H))
    # surf.fill(COLOR_WHITE)
    surf.blit(resources.TEXTURE_SCALED_BACKGROUND, (0, 0))

    # the player and the gun
    pygame.draw.rect(surf, resources.COLOR_RED, player.to_rect())

    # the bullets
    for bullet in bullets:
        bullet.draw(surf)

    # the enemies
    for enemy in enemies:
        enemy.draw(surf)
        # pygame.draw.circle(surf, COLOR_RED, (int(enemy.x), int(enemy.y)), ENEMY_SIZE)
    
    hud_surf = hud.render_hud(player)
    surf.blit(hud_surf, (0, 0))

    return surf

# returns if true if the game should continue going
def update_game(events: list[pygame.event.Event], dt: float) -> bool:
    # handle events
    for event in events:
        if event.type == pygame.QUIT:
            return False

    ## handle keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += PLAYER_SPEED * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= PLAYER_SPEED * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += PLAYER_SPEED * dt
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= PLAYER_SPEED * dt

    ## handle mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    # update player rotation
    player.rotate_to(mouse_pos[0], mouse_pos[1])

    # update player gun_delay
    player.gun_delay -= dt
    # update the enemies spawn delay
    global enemies_spawn_delay
    enemies_spawn_delay -= dt


    # spawn a enemy if the spawn delay is zero or lower
    if enemies_spawn_delay <= 0:
        while True:
            # generate new random positions for the enemy to spawn at
            x = random.uniform(0, resources.TOTAL_W)
            y = random.uniform(0, resources.TOTAL_H)

            # if the new position is more than ENEMY_SPAWN_DISTANCE away from the player spawn the enemy and break the loop
            if utils.distance((player.x, player.y), (x, y)) > ENEMY_SPAWN_DISTANCE:
                enemies.append(Enemy(x, y, 0, 5))
                enemies_spawn_delay = ENEMIES_SPAWN_COOLDOWN

                break


    # if left mouse button
    if mouse_buttons[0] and player.gun_delay <= 0:
        bullets.append(Bullet(player.x, player.y, player.rotation, True))
        player.gun_delay = PLAYER_GUN_COOLDOWN

    # simulate all bullets
    for i, bullet in enumerate(bullets):
        # check if the bullet is in bounds, if yes pop it
        if bullet.x > resources.TOTAL_W + BULLET_SIZE or bullet.y > resources.TOTAL_H + BULLET_SIZE or bullet.x < -BULLET_SIZE or bullet.y < -BULLET_SIZE:
            bullets.pop(i)
            continue

        # check if it has hit a enemy
        for enemy in enemies:
            if utils.distance((bullet.x, bullet.y), (enemy.x, enemy.y)) <= ENEMY_RADIUS:
                enemy.hit()
                # TODO: fix so that i dont have to use a try except here
                try:
                    bullets.pop(i)
                except:
                    pass



        # move the bullet
        bullet.move(dt, BULLET_SPEED)

    # simulate all enemies
    for i, enemy in enumerate(enemies):
        # if the enemy is dead remove it
        if enemy.hp <= 0:
            enemies.pop(i)
            continue
        
        enemy.rotate_to(player.x, player.y)
        enemy.move(dt)

        if utils.distance((enemy.x, enemy.y), (player.x, player.y)) < PLAYER_SIZE:
            player.health -= 1
            enemies.pop(i)
            continue


    return True
