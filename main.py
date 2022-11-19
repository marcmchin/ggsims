import pygame, sprites, qanda, os, sys, time, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT, FPS, ACC, FRIC = 400, 450, 60, 0.5, -0.1

fpstick = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

MENUBG = pygame.transform.scale(loadify(os.path.join('Assets', 'menubg.jpg')), (400,450))

CORRECTSFX = pygame.mixer.Sound(os.path.join('Assets', 'correct.mp3'))

WRONGSFX = pygame.mixer.Sound(os.path.join('Assets', 'wrong.mp3'))

spritegroup = pygame.sprite.Group()

L1F = sprites.Floor(1)
spritegroup.add(L1F)

L1BD = sprites.Backdrop(1)
spritegroup.add(L1BD)

L2F = sprites.Floor(2)
spritegroup.add(L2F)

L2BD = sprites.Backdrop(2)
spritegroup.add(L2BD)

L3F = sprites.Floor(3)
spritegroup.add(L3F)

L4F = sprites.Floor(4)
spritegroup.add(L4F)

ROOF = sprites.Floor(5)
spritegroup.add(ROOF)

QB1 = sprites.QuestionBox(1)
spritegroup.add(QB1)

P1 = sprites.Player(True, 1)
spritegroup.add(P1)

QP = qanda.QuestionPopup(-1, 1)
spritegroup.add(QP)

DT = sprites.Love()
spritegroup.add(DT)

CHCK = qanda.Checkmark()
spritegroup.add(CHCK)

UNCHCK = qanda.Xmark()
spritegroup.add(UNCHCK)

def convert_mcq_to_num(letter):
    if letter == 'a':
        return 1
    if letter == 'b':
        return 2
    if letter == 'c':
        return 3
    if letter == 'd':
        return 4

class Background():
    def __init__(self, bgimg, scrollspeed):
        self.bgimage = bgimg
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width

        self.scrollspeed = scrollspeed
        
    def update(self):
        self.bgX1 -= self.scrollspeed
        self.bgX2 -= self.scrollspeed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX1, self.bgY1))
        displaysurface.blit(pygame.transform.flip(self.bgimage, True, False), (self.bgX2, self.bgY2))
        
mainmenubg = Background(MENUBG, 0.75)


def player_movement(self):
    self.acc = vec(0,0)
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
        self.acc.x = -ACC
        if self.facingright:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facingright = False
            
        
    if pressed_keys[K_RIGHT]:
        self.acc.x = ACC
        if not self.facingright:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facingright = True
        
    self.acc.x += self.vel.x * FRIC
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc
    if self.pos.x > WIDTH:
        self.pos.x = 0
    if self.pos.x < 0:
        self.pos.x = WIDTH
    

def main_menu():
    pygame.display.set_caption("Project GGSIM - In menu")
    ticking = 0

    while True:
        mainmenubg.update()
        mainmenubg.render()
        
        MENU_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 40).render("GG SIM", True, (255,255,255))
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 50))
        pygame.draw.rect(displaysurface, (0,0,0), MENU_RECT, 0, 3)
        displaysurface.blit(MENU_TEXT, MENU_RECT)
        
        SUBTITLE_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 12).render("made by gg", True, (255,255,255))
        SUBTITLE_RECT = SUBTITLE_TEXT.get_rect(center=(200, 90))
        pygame.draw.rect(displaysurface, (0,0,0), SUBTITLE_RECT, 0, 3)
        displaysurface.blit(SUBTITLE_TEXT, SUBTITLE_RECT)
        
        START_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 20).render("press enter", True, (255,255,255))
        START_RECT = START_TEXT.get_rect(center=(200, 410))
        
        ticking = ticking + 1
        if ticking <= 60:
            displaysurface.blit(START_TEXT, START_RECT)
        elif ticking >= 120:
            ticking = 0
        
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play()
                if event.key == pygame.K_ESCAPE:
                    leave_confirmation()
        
        pygame.display.update()
        fpstick.tick(FPS)
    

def play():
    displaysurface.fill((0,0,0))

    
    pygame.display.set_caption("Project GGSIM - In game")
    
    movement = True
    
    level = 1
    time_limit = 120
    start_time = time.time()
    P1.change_level(1)
    QP.clear_question()
    CHCK.disappear()
    UNCHCK.disappear()
    
    level1q_ans = 0
    while level == 1:
        elapsed_time = time.time()-start_time
        displaysurface.fill((0,0,0))
        if movement:
            player_movement(P1)
            
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_elapsed = elapsed_time
                    pause()
                    pygame.display.set_caption("Project GGSIM - In game")
                    start_time = time.time()-paused_elapsed
                if not movement:
                    if event.key == pygame.key.key_code(str(QP.get_answer())):
                        CHCK.appear()
                        QP.set_question(1, QP.qnum, convert_mcq_to_num(str(QP.get_answer())))
                        for entity in spritegroup:
                            displaysurface.blit(entity.image, entity.rect)
                            entity.rect.midbottom = entity.pos
                        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
                        pygame.display.update()
                        fpstick.tick(FPS)
                        level1q_ans = level1q_ans + 1
                        pygame.mixer.Sound.play(CORRECTSFX)
                        
                        time.sleep(1)                
                        movement = True
                        QP.clear_question()
                        
                        if (level1q_ans >= 4):
                            level = 2
                        else:
                            P1.change_level(1)
                            CHCK.disappear()
                            QB1.appear(1)
                        
                            
                    elif event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d:
                        UNCHCK.appear()
                        QP.set_question(1, QP.qnum, convert_mcq_to_num(pygame.key.name(event.key)))
                        for entity in spritegroup:
                            displaysurface.blit(entity.image, entity.rect)
                            entity.rect.midbottom = entity.pos
                        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
                        pygame.display.update()
                        fpstick.tick(FPS)
                        if level1q_ans > 0:
                            level1q_ans = level1q_ans-1 #temporary - replace with sound effect and symbol
                        pygame.mixer.Sound.play(WRONGSFX)
                        
                        time.sleep(1)
                        movement = True
                        QP.clear_question()
                        P1.change_level(1)
                        QB1.appear(1)
                        UNCHCK.disappear()

                
                        
                        

        for entity in spritegroup:
            displaysurface.blit(entity.image, entity.rect)
            entity.rect.midbottom = entity.pos
            
        if P1.rect.colliderect(QB1.rect):
            movement = False
            QB1.vanish()
            QP.set_question(1, random.randint(1, qanda.QuestionPopup.get_question_count(1)), 0)
            
        COUNT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 31).render(str(time_limit-math.floor(elapsed_time)), True, (255,255,255))
        COUNT_RECT = COUNT_TEXT.get_rect(center=(200, 431))
        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
    
        pygame.display.update()
        fpstick.tick(FPS)
        
        if elapsed_time > time_limit:
            game_over()
    
    level = 2
    time_limit = 120
    start_time = time.time()
    P1.change_level(2)
    QP.clear_question()
    CHCK.disappear()
    UNCHCK.disappear()
    selectedpart = False
    QP.set_question(2, 1, 0)
    
    level2q_ans = 0
    while level == 2:
        displaysurface.fill((0,0,0))
        elapsed_time = time.time()-start_time
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_elapsed = elapsed_time
                    pause()
                    pygame.display.set_caption("Project GGSIM - In game")
                    start_time = time.time()-paused_elapsed
                if not selectedpart:
                    if event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d:
                        heroine = convert_mcq_to_num(pygame.key.name(event.key))
                        DT.set_image(heroine)
                        
                        QP.set_question(2, random.randint(2, qanda.QuestionPopup.get_question_count(2)), 0)
                        selectedpart = True
                        
                        
                elif selectedpart:
                    if event.key == pygame.key.key_code(str(QP.get_answer())):
                        CHCK.appear()
                        for entity in spritegroup:
                            displaysurface.blit(entity.image, entity.rect)
                            entity.rect.midbottom = entity.pos
                        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
                        pygame.display.update()
                        fpstick.tick(FPS)
                        level2q_ans = level2q_ans + 1
                        pygame.mixer.Sound.play(CORRECTSFX)
                        
                        time.sleep(1)
                        if (level2q_ans >= 3):
                            level = 3
                        else:
                            CHCK.disappear()
                            QP.set_question(2, random.randint(2, qanda.QuestionPopup.get_question_count(2)), 0)
                    elif event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d:
                        UNCHCK.appear()
                        for entity in spritegroup:
                            displaysurface.blit(entity.image, entity.rect)
                            entity.rect.midbottom = entity.pos
                        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
                        pygame.display.update()
                        fpstick.tick(FPS)
                        if level2q_ans > 0:
                            level2q_ans = level2q_ans - 1
                        pygame.mixer.Sound.play(WRONGSFX)
                        
                        time.sleep(1)
                        UNCHCK.disappear()
                        QP.set_question(2, random.randint(1, qanda.QuestionPopup.get_question_count(2)), 0)
                        
                    

        for entity in spritegroup:
            displaysurface.blit(entity.image, entity.rect)
            entity.rect.midbottom = entity.pos
            
        COUNT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 31).render(str(time_limit-math.floor(elapsed_time)), True, (255,255,255))
        COUNT_RECT = COUNT_TEXT.get_rect(center=(200, 431))
        displaysurface.blit(COUNT_TEXT, COUNT_RECT)
    
        pygame.display.update()
        fpstick.tick(FPS)
        
        if elapsed_time > time_limit:
            game_over()
    
    # level = 3
    # time_limit = 120
    # start_time = time.time()
    # P1.change_level(3)
    # QP.clear_question()
    # CHCK.disappear()
    # UNCHCK.disappear()
    # while level == 3:
    #     displaysurface.fill((0,0,0))
    #     player_movement(P1)
    
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 pause()
    #                 pygame.display.set_caption("Project GGSIM - In game")

    #     for entity in spritegroup:
    #         displaysurface.blit(entity.image, entity.rect)
    #         entity.rect.midbottom = entity.pos
    
    #     pygame.display.update()
    #     fpstick.tick(FPS)
        
    # level = 4
    # time_limit = 120
    # start_time = time.time()
    # P1.change_level(4)
    # QP.clear_question()
    # CHCK.disappear()
    # UNCHCK.disappear()
    # while level == 4:
    #     displaysurface.fill((0,0,0))
    #     player_movement(P1)
    
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 pause()
    #                 pygame.display.set_caption("Project GGSIM - In game")

    #     for entity in spritegroup:
    #         displaysurface.blit(entity.image, entity.rect)
    #         entity.rect.midbottom = entity.pos
    
    #     pygame.display.update()
    #     fpstick.tick(FPS)
    

def pause():
    pygame.display.set_caption("Project GGSIM - Paused")

    
    displaysurface.blit(MENUBG, (0,0))
    paused = True
    while paused:
        displaysurface.blit(MENUBG, (0,0))
        
        PAUSED_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 50).render("PAUSED", True, (255,255,255))
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(200, 225))
        pygame.draw.rect(displaysurface, (0,0,0), PAUSED_RECT, 0, 3)
        displaysurface.blit(PAUSED_TEXT, PAUSED_RECT)
        
        QUIT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 20).render("press enter to quit", True, (255,255,255))
        QUIT_RECT = QUIT_TEXT.get_rect(center=(200, 400))
        pygame.draw.rect(displaysurface, (0,0,0), QUIT_RECT, 0, 3)
        displaysurface.blit(QUIT_TEXT, QUIT_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_RETURN:
                    pause_confirmation()
        pygame.display.update()
        fpstick.tick(FPS)
    
def pause_confirmation():
    paused2 = True
    ticking = 0
    while paused2:
        displaysurface.blit(MENUBG, (0,0))
        
        PAUSED_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 50).render("PAUSED", True, (255,255,255))
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(200, 225))
        pygame.draw.rect(displaysurface, (0,0,0), PAUSED_RECT, 0, 3)
        displaysurface.blit(PAUSED_TEXT, PAUSED_RECT)
        
        QUIT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 20).render("are you sure you want to quit? (press enter)", True, (255,255,255))
        QUIT_RECT = QUIT_TEXT.get_rect(center=(200, 400))
        pygame.draw.rect(displaysurface, (0,0,0), QUIT_RECT, 0, 3)
        ticking = ticking + 1
        if ticking <= 60:
            displaysurface.blit(QUIT_TEXT, QUIT_RECT)
        elif ticking >= 120:
            ticking = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused2 = False
                if event.key == pygame.K_RETURN:
                    main_menu()
        pygame.display.update()
        fpstick.tick(FPS)
        
def leave_confirmation():
    paused2 = True
    ticking = 0
    while paused2:
        mainmenubg.update()
        mainmenubg.render()
        
        PAUSED_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 50).render("QUIT", True, (255,255,255))
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(200, 225))
        pygame.draw.rect(displaysurface, (0,0,0), PAUSED_RECT, 0, 3)
        displaysurface.blit(PAUSED_TEXT, PAUSED_RECT)
        
        QUIT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 20).render("quit the game? (press enter)", True, (255,255,255))
        QUIT_RECT = QUIT_TEXT.get_rect(center=(200, 400))
        pygame.draw.rect(displaysurface, (0,0,0), QUIT_RECT, 0, 3)
        ticking = ticking + 1
        if ticking <= 60:
            displaysurface.blit(QUIT_TEXT, QUIT_RECT)
        elif ticking >= 120:
            ticking = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused2 = False
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        fpstick.tick(FPS)
        
def game_over():
    while True:
        mainmenubg.update()
        mainmenubg.render()
        
        PAUSED_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 50).render("GAME OVER", True, (255,255,255))
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(200, 225))
        pygame.draw.rect(displaysurface, (0,0,0), PAUSED_RECT, 0, 3)
        displaysurface.blit(PAUSED_TEXT, PAUSED_RECT)
        
        QUIT_TEXT = pygame.font.Font("Assets/Aller_Bd.ttf", 20).render("continue?", True, (255,255,255))
        QUIT_RECT = QUIT_TEXT.get_rect(center=(200, 400))
        pygame.draw.rect(displaysurface, (0,0,0), QUIT_RECT, 0, 3)
        displaysurface.blit(QUIT_TEXT, QUIT_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    main_menu()
                    
        pygame.display.update()
        fpstick.tick(FPS)
    
main_menu()