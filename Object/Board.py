import pygame
import math
from const import *
class Board:
    def __init__(self, level, screen, numberRowMatrix, numberColMatrix, player, font):
        self.level = level
        self.screen = screen
        self.colorLine = "blue"
        self.colorCircle = "white"
        self.PI = math.pi
        self.WIDTH_LINE_BOARD = 2
        self.WIDTH_SMALL_CIRCLE_BOARD = 2
        self.WIDTH_BIG_CIRCLE_BOARD = 6 
        self.num1 = (HEIGHT - 50) // numberRowMatrix
        self.num2 = WIDTH // numberColMatrix
        self.player = player
        self.font = font

    
    def draw(self, flicker):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x, y = j * self.num2, i * self.num1
                cx, cy = x + 0.5 * self.num2, y + 0.5 * self.num1
                if self.level[i][j] == DOT:
                        pygame.draw.circle(self.screen, self.colorCircle, (cx, cy), self.WIDTH_SMALL_CIRCLE_BOARD)
                elif self.level[i][j] == BIG_DOT and not flicker:
                        pygame.draw.circle(self.screen, self.colorCircle, (cx, cy), self.WIDTH_BIG_CIRCLE_BOARD)
                elif self.level[i][j] == VERTICAL_LINE:
                        pygame.draw.line(self.screen, self.colorLine, (cx, y), (cx, y + self.num1), self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == HORIZONTAL_LINE:
                        pygame.draw.line(self.screen, self.colorLine, (x, cy), (x + self.num2, cy), self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == TOP_RIGHT:
                        pygame.draw.arc(self.screen, self.colorLine, [(x - 0.4 * self.num2) - 2, y + 0.5 * self.num1, self.num2, self.num1], 0, self.PI / 2, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == TOP_LEFT:
                        pygame.draw.arc(self.screen, self.colorLine, [(x + 0.5 * self.num2), y + 0.5 * self.num1, self.num2, self.num1], self.PI / 2, self.PI, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == BOT_LEFT:
                        pygame.draw.arc(self.screen, self.colorLine, [(x + 0.5 * self.num2), y - 0.4 * self.num1, self.num2, self.num1], self.PI, 3 * self.PI / 2, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == BOT_RIGHT:
                        pygame.draw.arc(self.screen, self.colorLine, [(x - 0.4 * self.num2) - 2, y - 0.4 * self.num1, self.num2, self.num1], 3 * self.PI / 2, 2 * self.PI, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == GATE:
                        pygame.draw.line(self.screen, self.colorCircle, (x, cy), (x + self.num2, cy), self.WIDTH_LINE_BOARD)
    
    def draw_misc(self, setDisplayDrawMisc):
        if (setDisplayDrawMisc == False): 
                return
        score_text = self.font.render(f'Score: {self.player.score}', True, 'white')
        self.screen.blit(score_text, (10, HEIGHT - 30))
        
        # Hiển thị mạng còn sống của player
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.player.images[0], (25, 25)), (WIDTH - (self.player.lives + 2) * WIDTH_LIVES + (i * WIDTH_LIVES), HEIGHT - WIDTH_LIVES))
