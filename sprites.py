import pygame as pg
from pygame.sprite import Sprite
import os
import random
import time
from settings import *
# from main import *
# from main import *
vec = pg.math.Vector2
last_call_time = 0

class Player(Sprite):
    def __init__(self,X,Y):
        Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH/2, HEIGHT/2)
        self.pos = vec(X,Y)
        # self.color = color
        self.start = (X,Y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.fragment = vec((self.rect.x + PLAYER_WIDTH - WIDTH), (self.pos.y + HEIGHT) - HEIGHT)
    
    def jump(self,JUMPFORCE = -100):
        keystate = pg.key.get_pressed()
        global last_call_time
        # todo
        # jump cooldown
        # jump limit
        if keystate[pg.K_w]:
            if self.vel.y == 0:
                print(f"last jump call time is {last_call_time}")
                if pg.time.get_ticks() - int(last_call_time) > JUMP_COOLDOWN:
                    self.vel.y = JUMP_FORCE
                    last_call_time = pg.time.get_ticks()
                    print(f"last jump call time is {last_call_time}")

        

    def input(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
            
        if keystate[pg.K_w]:
            self.jump()
            
        if keystate[pg.K_s]:
            self.acc.y = PLAYER_ACC
            
        if keystate[pg.K_c]:
            self.pos = self.start

    def gravity(self):
        self.vel.y += PLAYER_GRAVITY



    def inbounds(self):
        
        if self.rect.x >= WIDTH - PLAYER_WIDTH:
            # self.vel.x = -1
            print("i am off the right side")
            self.vel.x = 0
            self.pos.x = WIDTH - PLAYER_WIDTH/2

        if self.rect.x <= 0:
            # self.vel.x = 1
            print("i am off the left")
            self.vel.x = 0
            self.pos.x = PLAYER_WIDTH/2



        if self.rect.y >= HEIGHT - PLAYER_HEIGHT:
            print("I am off the bottom")
            self.vel.y = 0
            self.pos.y = HEIGHT-PLAYER_HEIGHT/2


    def update(self):
        self.inbounds()
        self.acc = self.vel * PLAYER_FRICTION
        self.input()
        self.gravity()
        self.jump()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

class Obstacle(Sprite):
    def __init__(self,width,height,xpos,ypos):
        Sprite.__init__(self)
        self.image = pg.Surface((width,height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (xpos, ypos)
        self.pos = vec(0,0)