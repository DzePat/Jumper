import pygame

import random

from pygame.locals import (
        RLEACCEL,
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
pygame.display.set_caption("Jumper")

bird_images = ["bird1.png",
               "bird2.png",
               "bird3.png",
               "bird4.png",
               "bird5.png",
               "bird6.png",
               "bird7.png",
               "bird8.png",
               "bird9.png"]


# Define a player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("cat.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.jump = 0
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            if(self.jump != 0):
                self.rect.move_ip(0, -9)
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
            self.kill()

# Platform class which creates platform objects for player to stand on
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.image.load("Flat.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(SCREEN_HEIGHT+20, SCREEN_HEIGHT+100),
            )
        )
        self.speed = random.randint(1, 3)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.surf = pygame.image.load(bird_images[0]).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.image_index = 0
        self.rect = self.surf.get_rect(
            center=(
                -20,
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)
    def update(self):
        self.image_index += 1
        if self.image_index >= 90:
            self.image_index = 0
        if self.image_index%10 == 0:
            index = int(self.image_index/10)
            self.surf = pygame.image.load(bird_images[index]).convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

def Jumper():

    # Create a custom event for adding a new platform
    ADDPLATFORM = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDPLATFORM, 1200)
    #create a custom event for adding a new enemy
    ADDENEMIES = pygame.USEREVENT +2
    pygame.time.set_timer(ADDENEMIES, 2000)


    #initiating first platform
    firstplatform = Platform()
    firstplatform.rect.x = 200-25
    firstplatform.rect.y = 700-25
    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    player.rect.x = 200 - 10
    player.rect.y = 680 - 50

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    platforms.add(firstplatform)
    all_sprites.add(firstplatform)
    
    enemies = pygame.sprite.Group()


    # Variable to keep the main loop running
    running = True

    while(running):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    running = False
            
            elif event.type == QUIT:
                running = False
      
            elif event.type == ADDPLATFORM:
            # Create the new platform and add it to sprite groups
                new_platform = Platform()
                platforms.add(new_platform)
                all_sprites.add(new_platform)
            
            elif event.type == ADDENEMIES:
            # Create the new enemy and add it to sprite groups
                new_enemy = Bird()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            
        
            # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # moves all platforms up once depeneding on the speed of the platform
        platforms.update()
        
        enemies.update()

        # checks if  the player has colided with the platform sprite     
        if pygame.sprite.spritecollideany(player,platforms):
            collision = pygame.sprite.spritecollideany(player,platforms)
            if(collision.rect[1] < player.rect.y):
                player.jump = 0
                
            elif(collision.rect[1] > player.rect.y):
                player.jump = 40
                player.rect.y = collision.rect[1]-45
                player.rect.move_ip(0,-collision.speed)
        else:
            # adds downward movment on the player so it acts like a gravity
            player.rect.move_ip(0,4)
        
        # checks collision with the birds 
        if pygame.sprite.spritecollideany(player,enemies):
            collision1 = pygame.sprite.spritecollideany(player,enemies)
            collx = abs(player.rect.x - collision1.rect.x)
            colly = abs(player.rect.y - collision1.rect.y)
            if(collx < 5 or colly <5):
                player.kill()
                running = False
            else:
                continue
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        screen.fill([52,235,186])

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # kills the player object and ends the loop if player hit the bottom of the screen
        if(player.rect.y > SCREEN_HEIGHT):
            player.kill()
            running = False

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()




Jumper()
