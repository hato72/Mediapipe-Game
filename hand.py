import pygame 
from draw_image import * 
import draw_image
from env import *
#from hand_tracking import Hand_tracking

class Hand:
    def __init__(self):
        self.orig_image = draw_image.load("img/click.png",size=(hand_size,hand_size))
        self.image = self.orig_image.copy()
        #self.image_smaller = image.load
        self.rect = pygame.Rect(screen_width//2,screen_height//2,hand_hitbox[0],hand_hitbox[1])
        self.left_click = False

    def follow_mouse(self): # change the hand pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()

    def follow_hand_tracking(self,x,y):
        self.rect.center = (x,y)

    def draw_hitbox(self,surface):
        pygame.draw.rect(surface,(200,60,0),self.rect)

    def draw(self,surface):
        draw_image.draw(surface,self.image,self.rect.center,pos_mode="center")

        if hitbox:
            self.draw_hitbox(surface)


    def on_animator(self, animators): # return a list with all animations that collide with the hand hitbox
        return [animator for animator in animators if self.rect.colliderect(animator.rect)]


    def kill_animators(self, animators, score): # will kill the animators that collide with the hand when the left mouse button is pressed
        if self.left_click: # if left click
            for animator in self.on_animator(animators):
                animator_score = animator.kill(animators)
                score += animator_score
                # sounds["slap"].play()
                # if animator_score < 0:
                #     sounds["screaming"].play()
        else:
            self.left_click = False
        return score
    
    def kill_norts(self, norts):
        score = 0
        if self.left_click:
            for nort in norts[:]:  # リストのコピーを使用して反復
                if self.rect.colliderect(nort.rect):
                    norts.remove(nort)
                    score += 1
        return score

    