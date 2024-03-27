import cv2 
from norts import Norts
import pygame
import time
import random
import sys
from hand import Hand
from hand_tracking import Hand_tracking
from background import Background
from env import *
import draw_image


class Game:
    def __init__(self,surface):
        self.surface = surface
        self.background = Background()

        #self.norts = Norts(surface)

        self.cap = cv2.VideoCapture(0)
        

    def reset(self):
        #print("game reset")
        self.hand_tracking = Hand_tracking()
        self.hand = Hand()
        self.animators = []
        self.animators_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()
        #pass

    def spawn_animator(self):
        t = time.time()
        if t > self.animators_spawn_timer:
            self.insects_spawn_timer = t + spawn_time

            # increase the probability that the animation will be a angel or a zombie over time
            #nb = (dulation-self.time_left)/dulation * 100  /50  # increase from 0 to 50 during all  the game (linear)
            if self.time_left < dulation/2:
                self.animators.append(Norts())

    def load_camera(self):
        _,self.frame = self.cap.read()
        

    def set_hand_position(self):
        self.frame = self.hand_tracking.hand_tracking(self.frame)
        (x,y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x,y)

    def draw(self):
        self.background.draw(self.surface)

        for animator in self.animators:
            animator.draw(self.surface)

        self.hand.draw(self.surface)

        draw_image.draw_text(self.surface, f"Score : {self.score}", (5, 5), COLORS["score"], font=FONT["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        draw_image.draw_text(self.surface, f"Time left : {self.time_left}", (screen_width//2, 5),  timer_text_color, font=FONT["medium"],
                    shadow=True, shadow_color=(255,255,255))
        
    def game_time_update(self):
        self.time_left = max(round(dulation - (time.time() - self.game_start_time), 1), 0)


    def update(self):
        #handtracking
        self.load_camera()
        self.set_hand_position()
        self.game_time_update()
        #norts
        #self.norts.update()

        self.draw()

        if self.time_left > 0:
            self.spawn_animator()
            (x, y) = self.hand_tracking.get_hand_center()
            self.hand.rect.center = (x, y)
            self.hand.left_click = self.hand_tracking.hand_close
            if self.hand.left_click:
                print("hand close")
            self.hand.image = self.hand.orig_image.copy()
            self.score = self.hand.kill_animators(self.animators, self.score)
            for animator in self.animators:
                animator.move()

        else: # when the game is over
            if draw_image.button(self.surface, 320, "Continue"):
                return "menu"
            if draw_image.button(self.surface, 320+button_size[1]*1.5, "Quit"):
                pygame.quit()
                sys.exit()

        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)