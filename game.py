import cv2 
from norts import *

class Game:
    def __init__(self,surface):
        self.surface = surface
        self.norts = Norts(surface)

        #self.cap = cv2.VideoCapture(0)

    def reset(self):
        #self.hand_tracking = Hand_tracking()
        #self.hand = Hand()
        pass
        

    def update(self):
        #norts
        self.norts.update()
        
        #handtracking
