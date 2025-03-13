import pygame
from const import *
from Test.Test import FactoryTest
import sys
class TestMenu:
    def __init__(self, screen):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.screen = screen
        self.color_bg = (255, 224, 217)
        self.ind_test = 0
        self.number_of_test = len(FactoryTest.getProperties())
        self.box_bg = pygame.Rect(50,50,400,100)
        self.box_opt =[]
        self.WIDTH_OPT = 50
        self.HEIGHT_OPT = 30
        self.Pos_opt = (60,110)
        self.color_opt = (131, 102, 255)
        self.text = "Which case do you want?"
        self.box_exit = pygame.Rect(360,110,50,30)
        self.color_exit = (193, 36, 36)
    def execute(self):
        running = True
        self.screen.fill("black")
        pygame.draw.rect(self.screen, self.color_bg, self.box_bg,0, 10)
        text = self.font.render(self.text, True, BLACK)  # Chữ trắng
        text_rect = text.get_rect(center = self.box_bg.center)
        self.screen.blit(text, text_rect)

        text = self.font.render("EXIT", True, WHITE)  # Chữ trắng
        text_rect = text.get_rect(center = self.box_exit.center)
        pygame.draw.rect(self.screen, self.color_exit, self.box_exit,0, 10)
        self.screen.blit(text, text_rect)

        self.createBoxOption()
        for i in range(0, self.number_of_test):
            text = self.font.render(str(i+1), True, WHITE)  # Chữ trắng
            text_rect = text.get_rect(center = self.box_opt[i].center)
            pygame.draw.rect(self.screen, self.color_opt, self.box_opt[i], 0, 10)
            self.screen.blit(text, text_rect)
        pygame.display.flip()  # Cập nhật màn hình
        while(running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, box in enumerate(self.box_opt):
                        if box.collidepoint(event.pos):
                            self.ind_test = index
                            running = False
                            break
                    if self.box_exit.collidepoint(event.pos):
                        self.ind_test = -1
                        running = False


    def createBoxOption(self):
        for i in range(0, self.number_of_test):
            self.box_opt.append(pygame.Rect(self.Pos_opt[0]*(i+1)  ,self.Pos_opt[1], self.WIDTH_OPT, self.HEIGHT_OPT))
