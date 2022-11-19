import pygame
from pygame.locals import *
import os

pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT, FPS, ACC, FRIC = 400, 450, 60, 0.5, -0.1

QPOXSIZE = (300, 200)

fpstick = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

qbank = [[['q1.png', 'q1 (1).png', 'q1 (2).png', 'q1 (3).png', 'q1 (4).png'], ['q2.png', 'q2 (1).png', 'q2 (2).png', 'q2 (3).png', 'q2 (4).png'], 
          ['q3.png', 'q3 (1).png', 'q3 (2).png', 'q3 (3).png', 'q3 (4).png'], ['q4.png', 'q4 (1).png', 'q4 (2).png', 'q4 (3).png', 'q4 (4).png'],
          ['q5.png', 'q5 (1).png', 'q5 (2).png', 'q5 (3).png', 'q5 (4).png'], ['q6.png', 'q6 (1).png', 'q6 (2).png', 'q6 (3).png', 'q6 (4).png'],
          ['q7.png', 'q7 (1).png', 'q7 (2).png', 'q7 (3).png', 'q7 (4).png'], ['q8.png', 'q8 (1).png', 'q8 (2).png', 'q8 (3).png', 'q8 (4).png'],
          ['q9.png', 'q9 (1).png', 'q9 (2).png', 'q9 (3).png', 'q9 (4).png']], [['2q1.png'], ['2q2.png'], ['2q3.png'], ['2q4.png'], ['2q5.png']]]
abank = [['c', 'c', 'a', 'd', 'a', 'b', 'c', 'c', 'd'], ['e', 'a', 'a', 'a', 'd']]

class QuestionPopup(pygame.sprite.Sprite):
    def __init__(self, level, qnum):
        super().__init__()
        if level == -1:
            self.image = pygame.transform.scale(loadify(os.path.join('Assets', 'blankquestion.png')), QPOXSIZE)
        else:
            self.image = pygame.transform.scale(loadify(os.path.join('Assets/l' + str(level) + 'questions', qbank[level-1][qnum-1][0])), QPOXSIZE)
        self.level = level
        self.qnum = qnum
        
        self.pos = vec((200, 325))
        self.rect = self.image.get_rect()
    def set_question(self, level, qnum, anum):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets/l' + str(level) + 'questions', qbank[level-1][qnum-1][anum])), QPOXSIZE)
        self.level = level
        self.qnum = qnum
    def clear_question(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "blankquestion.png")), QPOXSIZE)
        self.level = -1
        self.qnum = -1
    def get_answer(self):
        return abank[self.level-1][self.qnum-1]
    def get_question_count(level):
        return len(qbank[level-1])

class Checkmark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "blankquestion.png")), (100,100))
        
        self.pos = vec((200, 275))
        self.rect = self.image.get_rect()
    def appear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "checkmark.png")), (100,100))
    def heartappear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "heart.png")), (100,100))
    def disappear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "blankquestion.png")), (100,100))

class Xmark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "blankquestion.png")), (100,100))
        
        self.pos = vec((200, 275))
        self.rect = self.image.get_rect()
    def appear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "uncheck.png")), (100,100))
    def heartappear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "heartbreak.png")), (100,100))
    def disappear(self):
        self.image = pygame.transform.scale(loadify(os.path.join('Assets', "blankquestion.png")), (100,100))

