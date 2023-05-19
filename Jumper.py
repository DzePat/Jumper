from tkinter import CURRENT
import pygame,random, time

from pygame.locals import (
        RLEACCEL,
        K_SPACE,
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
SCREEN_WIDTH = 500

SCREEN_HEIGHT = 800

#initialize mixer for sounds
pygame.mixer.init()
# Initialize pygame
pygame.init()
pressed_keys = pygame.key.get_pressed()

# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumper")

#font color,style and size
font = pygame.font.SysFont("arialblack",20)
Text_color = (0,0,0)
#renders a text on to the screen 
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

#list of songs
song_list = [
    "song1.mp3",
    "song2.mp3",
    "song3.mp3",
    "song4.mp3"
    ]
Coll_Sound = pygame.mixer.Sound("Collision.mp3")
# list of bird file names
bird_images = ["bird1.png",
               "bird2.png",
               "bird3.png",
               "bird4.png",
               "bird5.png",
               "bird6.png",
               "bird7.png",
               "bird8.png",
               "bird9.png"]

def song(time,player):
    currentsong = ""
    if(time == 1):
        currentsong = song_list[player.song]
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(loops=-1)
    elif(time%61 == 0):
        if(player.song == 3):
            player.song = 0
        else:
            player.song += 1
        currentsong = song_list[player.song]
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(loops=-1)



# Define a player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Catsit.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.jump = 0
        self.center = (self.rect.x + 50/2, self.rect.y + 50/2)
        self.song = 0
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
        self.surf = pygame.transform.scale(self.surf,(40,40))
        self.image_index = 0
        self.rect = self.surf.get_rect(
            center=(
                -20,
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.center = (self.rect.x + 20/2, self.rect.y + 20/2)
        self.speed = random.randint(1, 2)
    def update(self):
        self.image_index += 1
        if self.image_index >= 90:
            self.image_index = 0
        if self.image_index%10 == 0:
            index = int(self.image_index/10)
            self.surf = pygame.image.load(bird_images[index]).convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.surf = pygame.transform.scale(self.surf,(40,40))
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH-50),
                random.randint(0, 1),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, 1)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def Jumper():
    # Create a custom event for adding a new platform, enemy or a cloud
    ADDPLATFORM = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDPLATFORM, 1200)
    ADDENEMIES = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDENEMIES, 2000)
    ADDCLOUD = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDCLOUD, 4000)

    #initiating first platform
    firstplatform = Platform()
    firstplatform.rect.x = 225
    firstplatform.rect.y = 685
    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    player.rect.x = 225
    player.rect.y = 630

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    platforms = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    platforms.add(firstplatform)
    all_sprites.add(firstplatform)
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    previoustime = 0
    # Variable to keep the main loop running
    running = True
    start = time.time()
    while(running):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
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
            # Add a new cloud?
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                #all_sprites.add(new_cloud)

        currenttime = int(time.time()-start)
        if(currenttime != previoustime):
            previoustime = currenttime
            song(currenttime,player)
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # moves all platforms up once depeneding on the speed of the platform
        platforms.update()
        
        enemies.update()
        clouds.update()

        # checks if  the player has colided with the platform sprite     
        if pygame.sprite.spritecollideany(player,platforms):
            collision = pygame.sprite.spritecollideany(player,platforms)
            if(collision.rect[1] < player.rect.y):
                player.jump = 0
                
            elif(collision.rect[1] > player.rect.y):
                player.jump = 40
                player.rect.y = collision.rect[1]-50
                player.rect.move_ip(0,-collision.speed)
        else:
            # adds downward movment on the player so it acts like a gravity
            player.rect.move_ip(0,4)
        
        # checks collision with the birds 
        if pygame.sprite.spritecollideany(player,enemies):
            collision1 = pygame.sprite.spritecollideany(player,enemies)
            collx = abs(player.rect.x - collision1.rect.x)
            colly = abs(player.rect.y - collision1.rect.y)
            if(collx < 3 or colly <3):
                player.kill()
                Coll_Sound.play()
                Coll_Sound.set_volume(0.03)
                running = False
            else:
                continue

                
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        screen.fill([56,215,245])

        for cloud in clouds:
            screen.blit(cloud.surf,cloud.rect)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # kills the player object and ends the loop if player hit the bottom of the screen
        if(player.rect.y > SCREEN_HEIGHT):
            player.kill()
            running = False
        draw_text(str(currenttime),font,Text_color,350,0)
        pygame.display.flip()
        clock.tick(60)
    start = time.time()
    pygame.mixer.music.stop()






def GameMenu():
    Exit = True
    Alive = True
    start = True
    playing = True
    pygame.mixer.music.load("TitleSong.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(loops=-1)
    while Exit:
        screen.fill([0,0,0])
        if(playing == False):
            pygame.mixer.music.load("TitleSong.mp3")
            pygame.mixer.music.set_volume(0.03)
            pygame.mixer.music.play(loops=-1)
            playing == True
        if start == True:
            Title = pygame.image.load("Title.png").convert()
            screen.blit(Title,(50,200))
            Space = pygame.image.load("Space.jpg").convert()
            screen.blit(Space,(100,380))
            Space = pygame.image.load("TitleCat.png").convert()
            screen.blit(Space,(90,600))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Exit = False
                elif event.key == K_SPACE:
                        playing = False
                        pygame.mixer.music.stop()
                        Alive = True
                        start = False
                        Jumper()
                        Alive = False
                
        if Alive == False:
            Game_Over = pygame.image.load("Game_Over.png").convert()
            screen.blit(Game_Over,(200,200))
            draw_text("Press Space to start again",font,(255,0,0),100,250)
        pygame.display.flip()
    pygame.quit()
GameMenu()

