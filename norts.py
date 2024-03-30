import pygame
import random
import time
import draw_image
from env import *

class Norts:
    def __init__(self,surface):
        self.surface = surface
        self.norts = []
        self.norts_radius = 20
        self.norts_color = (255,0,0)
        self.new_norts_timer = 0
        self.new_norts_interval = 1000

        # self.x = screen_width
        # self.y = screen_height
        # self.speed_x = random.randint(-5, -1)
        # self.speed_y = random.randint(-5, -1)

    def update(self):
        print("norts update")
        self.new_norts_timer += pygame.time.get_ticks()
        if self.new_norts_timer >= self.new_norts_interval:
            self.new_norts_timer = 0
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            self.norts.append(Nort(self.surface,x,y))

        # for nort in self.norts:
        #     nort.move()
        #     nort.draw()

        self.norts = [nort for nort in self.norts if nort.is_on_screen()]

class Nort:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (255, 0, 0)
        self.speed_x = random.randint(-5, -1)
        self.speed_y = random.randint(-5, -1)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(self.surface,self.color,(self.x,self.y),self.radius)
        # if hitbox:
        #     self.draw_hitbox(surface)

    def is_on_screen(self):
        return 0 <= self.x <= screen_width and 0 <= self.y <= screen_height
    
    def collision(self,hand_rect):
        hand_center_x,hand_center_y = hand_rect.center
        x = self.x - hand_center_x
        y = self.y - hand_center_y
        distance = (x ** 2 + y ** 2) ** 0.5
        if distance <= self.radius + hand_rect.width // 2:
            return True
        else:
            return False
        #pass 