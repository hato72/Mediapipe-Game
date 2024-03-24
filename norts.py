import pygame
import random
import time
from draw_image import *
from env import *

class Norts:
    def __init__(self,surface):
        self.surface = surface
        self.norts = []
        self.norts_radius = 20
        self.norts_color = (255,0,0)
        self.new_norts_timer = 0
        self.new_norts_interval = 1000

    def update(self):
        self.new_norts_timer += pygame.time.get_ticks()
        if self.new_norts_timer >= self.new_norts_interval:
            self.new_norts_timer = 0
            self.norts.append(Norts(self.surface))

        for nort in self.norts:
            nort.move()
            nort.draw()

        self.norts = [nort for nort in self.norts if nort.is_on_screen()]

class Nort:
    def __init__(self, surface):
        self.surface = surface
        # screen_width, screen_height = surface.get_size()
        self.x = screen_width
        self.y = screen_height
        self.radius = 20
        self.color = (255, 0, 0)
        self.speed_x = random.randint(-5, -1)
        self.speed_y = random.randint(-5, -1)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(self.surface,self.color,(self.x,self.y),self.radius)

    def is_on_screen(self):
        return 0 <= self.x <= screen_width and 0 <= self.y <= screen_height
    
    def collision(self):
        pass 