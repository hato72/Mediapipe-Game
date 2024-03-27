import pygame

screen_width = 800
screen_height = 600

button_size = (240,90)
hand_size = 200
hand_hitbox = (50,80)

norts_size = (50,40)

hitbox = False

FPS = 90

anim_speed = 3
dulation = 60

TITLE = "Hand_Tracking_Game"

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39), "timer": (38, 61, 39),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "shadow": (46, 54, 163)}}

# fonts
pygame.font.init()
FONT = {}
FONT["small"] = pygame.font.Font(None, 30)
FONT["medium"] = pygame.font.Font(None, 40)
FONT["big"] = pygame.font.Font(None, 60)