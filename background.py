import pygame
import draw_image
from env import *

class Background:
    def __init__(self):
        self.image = draw_image.load("img/background.jpeg", size=(screen_width, screen_height),
                                convert="default")


    def draw(self, surface):
        draw_image.draw(surface, self.image, (screen_width//2, screen_height//2), pos_mode="center")