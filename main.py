import pygame 
import sys
#import os 
from env import *
from menu import Menu
from game import Game
from mole_whack import MoleWhackGame

pygame.init()
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((screen_width,screen_height),0,32)

mainClock = pygame.time.Clock()

fps_font = pygame.font.SysFont("coopbl", 22)

state = "menu"

menu = Menu(screen)
game1 = Game(screen)
game2 = MoleWhackGame(screen)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def update():
    global state
    if state == "menu":
        if menu.update() == "game1":
            game1.reset() # reset the game to start a new game
            state = "game1"
        if menu.update() == "game2":
            game2.reset() # reset the game to start a new game
            state = "game2"
    elif state == "game1":
        if game1.update() == "menu":
            state = "menu"
    elif state == "game2":
        if game2.update() == "menu":
            state = "menu"
    pygame.display.update()
    mainClock.tick(FPS)

while True:
    events()

    update()

    # if DRAW_FPS:
    #     fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
    #     screen.blit(fps_label, (5,5))

