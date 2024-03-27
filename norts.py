import pygame
import random
import time
import draw_image
from env import *

class Norts:
    def __init__(self):
        #self.surface = surface
        self.norts = []
        self.norts_radius = 20
        self.norts_color = (255,0,0)
        self.new_norts_timer = 0
        self.new_norts_interval = 1000

        self.x = screen_width
        self.y = screen_height
        self.speed_x = random.randint(-5, -1)
        self.speed_y = random.randint(-5, -1)

    def update(self):
        print("norts update")
        self.new_norts_timer += pygame.time.get_ticks()
        if self.new_norts_timer >= self.new_norts_interval:
            self.new_norts_timer = 0
            self.norts.append(Norts())

        for nort in self.norts:
            nort.move()
            nort.draw()

        self.norts = [nort for nort in self.norts if nort.is_on_screen()]


    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(self.norts_color,(self.x,self.y),self.norts_radius)
        # if hitbox:
        #     self.draw_hitbox(surface)

    def is_on_screen(self):
        return 0 <= self.x <= screen_width and 0 <= self.y <= screen_height
    
    def collision(self):
        pass 