import pygame

def Jumper():
    from pygame.locals import(
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT
        )


    pygame.init()
    screen = pygame.display.set_mode([800,800])
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill([255,255,255])

        pygame.draw.circle(screen,(0,0,255),(400,400),25)

        pygame.display.flip();
    pygame.quit();

Jumper()