import pygame



from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
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


def Jumper():

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Variable to keep the main loop running
    running = True

    while(running):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        player.rect.move_ip(0,1)
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

         # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        screen.fill([0,0,0])

        screen.blit(player.surf, player.rect)
        pygame.display.flip()

    pygame.quit()

Jumper()
