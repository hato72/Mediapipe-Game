import pygame
import sys
from env import *
from draw_image import *
from background import Background

class Menu:
    def __init__(self,surface):
        self.surface = surface
        self.background = Background()
        
    def draw(self):
        self.background.draw(self.surface)
        draw_text(self.surface,TITLE,(screen_width//2,120),COLORS["title"],font=FONT["medium"],shadow = True,shadow_color = (255,255,255), pos_mode="center")

    def update(self):
        self.draw()
        
        if button(self.surface,300,"Start_mole"):
            return "game1"
        if button(self.surface, 320+button_size[1]*1.5, "Quit"):
            pygame.quit()
            sys.exit()
        
        # if button(self.surface,200,"Start_mole"):
        #     return "game1"
        
        # if button(self.surface,350,"Start_norts"):
        #     return "game2"
        
        # if button(self.surface, 360+button_size[1]*1.5, "Quit"):
        #     pygame.quit()
        #     sys.exit()