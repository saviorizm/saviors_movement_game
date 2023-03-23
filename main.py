# file by saviorizm
# import libraries
import pygame as pg
from pygame.sprite import Sprite
import os
import random
from random import randint
from time import sleep

from settings import *
from sprites import *


# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# init pygame and create game window
pg.init()

# init sound mixers99
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My last game")
clock = pg.time.Clock() 

# create sprite groups
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
objects = pg.sprite.Group()

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)



# shit drawn
# for i in range
player = Player(WIDTH/2,HEIGHT/2)
obstacle1 = Obstacle(O1WIDTH,O1HEIGHT,randint(0,O1WIDTH),randint(0,WIDTH//3-O1HEIGHT))
obstacle2 = Obstacle(O2WIDTH,O2HEIGHT,randint(0,O2WIDTH),randint(WIDTH//3,WIDTH//3*2-O2HEIGHT))
obstacle3 = Obstacle(O3WIDTH,O3HEIGHT,randint(0,O3WIDTH),randint(WIDTH//3*2,WIDTH-O3HEIGHT))

# for i in range(3):
#     o = Obstacle(randint(0,300),randint(0,300),randint(0,800),randint(0,800))
#     all_sprites.add(o)
#     objects.add(o)

all_sprites.add(player,obstacle1,obstacle2,obstacle3)
objects.add(obstacle1,obstacle2,obstacle3)


# game loopw
while RUNNING:
    # maintains the loop speed
    clock.tick(FPS)
    global current_time
    current_time = pg.time.get_ticks()
    for event in pg.event.get():
        # ends the game if quit
        if event.type == pg.QUIT:
            RUNNING = False

#   update section of game loop
    enemies.update()
    objects.update()
    all_sprites.update()

    
    collided_obstacles = pg.sprite.spritecollide(player, objects, False)

    for obstacle in collided_obstacles:
        keystate = pg.key.get_pressed()
        # Calculate the penetration depth in x and y directions
        delta_x_left = player.rect.right - obstacle.rect.left
        delta_x_right = obstacle.rect.right - player.rect.left
        delta_y_top = player.rect.bottom - obstacle.rect.top
        delta_y_bottom = obstacle.rect.bottom - player.rect.top
        # Check for the smallest penetration depth
        min_delta_x = min(abs(delta_x_left), abs(delta_x_right))
        min_delta_y = min(abs(delta_y_top), abs(delta_y_bottom))
        if min_delta_x < min_delta_y:
            # Player collides on the left side of the obstacle
            if abs(delta_x_left) == min_delta_x:
                player.vel.x = 0
                player.pos.x = obstacle.rect.left - PLAYER_WIDTH/2
                if keystate[pg.K_d]:
                    player.vel.y += -PLAYER_GRAVITY*10
                if keystate[pg.K_w]:
                    player.jump(-50)
            # Player collides on the right side of the obstacle
            else:
                player.vel.x = 0
                player.pos.x = obstacle.rect.right + PLAYER_WIDTH/2
                if keystate[pg.K_a]:
                    player.vel.y += -PLAYER_GRAVITY*10
                if keystate[pg.K_w]:
                    player.jump(-50)
        else:
            # Player collides on the top side of the obstacle
            if abs(delta_y_top) == min_delta_y:
                player.vel.y = 0
                player.pos.y = obstacle.rect.top - PLAYER_WIDTH/2
            # Player collides on the bottom side of the obstacle
            else:
                player.vel.y = 0
                player.pos.y = obstacle.rect.bottom + PLAYER_WIDTH/2

    
        if player.rect.y < 0 + 20:
            print("i am off the top")
            
            WIN = True
            print("win is satsified")
            break
            
            

    screen.fill(RED)
    objects.draw(screen)
    all_sprites.draw(screen)
    # player.draw(screen)

    pg.display.flip()
    
 # ends program when loops evaluates to false


screen.fill(BLACK)
draw_text("You win",30,BLACK ,WIDTH/2,HEIGHT/2,)
pg.display.flip()
# sleep(2)
pg.quit()