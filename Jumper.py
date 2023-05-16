import pygame

import random

from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )
clock = pygame.time.Clock()
# Define constants for the screen width and height
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
# Initialize pygame
pygame.init()
pressed_keys = pygame.key.get_pressed()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.jump = int(5)
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            if(self.jump != 0):
                self.rect.move_ip(0, -40)
                self.jump -= 1
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((50, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(SCREEN_HEIGHT+20, SCREEN_HEIGHT+100),
            )
        )
        self.speed = random.randint(1, 8)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()

def Jumper():

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 500)

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Variable to keep the main loop running
    running = True

    while(running):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    running = False
            
            elif event.type == QUIT:
                running = False
      
            elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
                new_enemy = Platform()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # adds downward movment on the player so it acts like a gravity
        
            # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        
        enemies.update()

        screen.fill([0,0,0])

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # checks if  the player has colided with the platform sprite     
        if pygame.sprite.spritecollideany(player,enemies):
            player.jump = 5
            collision = pygame.sprite.spritecollideany(player,enemies)
            player.rect.y = collision.rect[1]-20
            player.rect.move_ip(0,-collision.speed)
        else:
            player.rect.move_ip(0,10)



        screen.blit(player.surf, player.rect)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

Jumper()
