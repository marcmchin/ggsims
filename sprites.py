import pygame
from pygame.locals import *
import random
import os

pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT, FPS, ACC, FRIC = 400, 450, 60, 0.5, -0.1

fpstick = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

LEVELHEIGHT = [413.75, 311.25, 198.75, 86.25, 0]
LEVELWIDTH = [56.25, 14.0625, 14.0625, 14.0625, 14.0625]


PLAYERSPRITE = pygame.transform.scale(loadify(os.path.join('Assets', 'adultFront.png')), (40,100))
QBOXSPRITE = pygame.transform.scale(loadify(os.path.join('Assets', 'qboxsprite.jpg')), (30,30))
FLOORSPRITES = ['lvl1floor.jpg', 'lvl1floor.jpg', 'lvl1floor.jpg', 'lvl1floor.jpg', 'lvl1floor.jpg']

BACKDROPSPRITES = ['school.jpg', 'date.jpg']

DATINGSPRITES = ['emilio.png', 'valo.png', 'nya.png', 'bunnies.jpg']


class Player(pygame.sprite.Sprite):
    def __init__(self, facingright, level):
        super().__init__() 
        self.image = PLAYERSPRITE
        self.rect = self.image.get_rect()
        
        self.pos = vec(200, LEVELHEIGHT[level-1])
        self.vel = vec((0,0))
        self.acc = vec((0,0))
        self.facingright = facingright
    def change_level(self, level):
        self.pos = vec(200, LEVELHEIGHT[level-1])
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        
class QuestionBox(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = QBOXSPRITE
        self.rect = self.image.get_rect()
        
        self.pos = vec((random.randint(0, 150) + 250 * random.randint(0,1), (LEVELHEIGHT[level-1] + 30+LEVELHEIGHT[level]+LEVELWIDTH[level])/2))
    def vanish(self):
        self.pos = vec(-100, -100)
    def appear(self, level):
        self.pos = vec((random.randint(0, 150) + 250 * random.randint(0,1), (LEVELHEIGHT[level-1] + 30+LEVELHEIGHT[level]+LEVELWIDTH[level])/2))

class Floor(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', FLOORSPRITES[level-1])), (400,LEVELWIDTH[level-1]))
        self.rect = self.image.get_rect()
        
        self.pos = vec((200, LEVELHEIGHT[level-1]+LEVELWIDTH[level-1]))
        
class Backdrop(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', BACKDROPSPRITES[level-1])), (400, LEVELHEIGHT[level-1]-LEVELHEIGHT[level]-LEVELWIDTH[level]))
        self.rect = self.image.get_rect()
        
        self.pos = vec((200, LEVELHEIGHT[level-1]))
        
class Love(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', 'blankquestion.png')), (100, 100))
        self.rect = self.image.get_rect()
        
        self.pos = vec((50, 100))
    def set_image(self, option):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', DATINGSPRITES[option-1])), (100, 100))