import pygame
from const import *
from board import boards 
import utils
import math
from Algorithm.BFS import BFS
from Music.music import Music
import time
class Player: 
    def __init__(self, x, y, screen, images, numberRowMatrix, numberColMatrix, music):
        self.x = x
        self.y = y
        self.direction = 0
        self.direction_command = 0
        self.counter = 0
        self.speed = SPEED_PLAYER
        self.score = 0
        self.screen = screen
        self.images = images
        self.width = WIDTH_PLAYER
        self.height = HEIGHT_PLAYER
        self.numberRowMatrix = numberRowMatrix 
        self.numberColMatrix = numberColMatrix
        self.turns_allowed = [False, False, False, False]
        self.level = boards
        self.power_up = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.lives = NUMBER_LIVES
        self.moving = False
        self.startup_counter = 0
        self.circle = pygame.draw.circle(self.screen, "red", (self.x + self.width // 2, self.y + self.height // 2), 1, 1)
        self.gameOver = False
        self.name = "Anonymous"
        self.music = music
        self.checkFirstPowerup = False
    def resetIntoDefault(self):
        self.startup_counter = 0
        self.power_counter = 0
        self.x, self.y = START_PLAYER_POSITION
        self.direction = RIGHT
        self.direction_command = RIGHT
        self.counter = 0
        self.power_up = False
        self.eaten_ghost = [False, False, False, False]
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == RIGHT:
           self.screen.blit(self.images[self.counter // 5], (self.x, self.y))
        elif self.direction == LEFT:
           self.screen.blit(pygame.transform.flip(self.images[self.counter // 5], True, False), (self.x, self.y))
        elif self.direction == UP:
           self.screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 90), (self.x, self.y))
        elif self.direction == DOWN:
            self.screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 270), (self.x, self.y))
    
    
    def check_collision(self):
        num1 = (HEIGHT - 50) // (len(boards))
        num2 = WIDTH // (len(boards[0]))
        center_x, center_y = utils.getCenter(self.x, self.y, boards)
        if 0 < self.x < WIDTH - 30:
            # Nếu ăn thức ăn thường thì score + 10
            player_j_coordinate, player_i_coordinate = utils.convert_coordinates(center_x, center_y)
            if self.checkFirstPowerup == True:
                self.checkFirstPowerup = False
                self.music.musicPowerUp()
            if self.level[player_i_coordinate][player_j_coordinate] == 1:
                if self.power_up == False:
                    self.music.stopMusicThread()
                    self.music.musicPacmanChomp()
                self.level[player_i_coordinate][player_j_coordinate] = 0
                self.score += SCORE_DOT
            
            # Nếu ăn power-up score + 50 và bật trạng thái power_up
            if self.level[player_i_coordinate][player_j_coordinate] == 2:
                self.level[player_i_coordinate][player_j_coordinate] = 0
                self.score += SCORE_BIG_DOT
                self.power_up = True
                self.power_counter = 0
                self.eaten_ghost = [False, False, False, False]
                self.checkFirstPowerup = True

    def check_position(self, level):
        center_x, center_y = utils.getCenter(self.x, self.y, level)
        pygame.draw.circle(self.screen, "red", (center_x, center_y), 3)
        turns = [False, False, False, False]
        num1 = (HEIGHT - 50) // self.numberRowMatrix
        num2 = WIDTH // self.numberColMatrix
        num3 = min(num1, num2) // 2
        if center_x // self.numberColMatrix < self.numberColMatrix - 1:
            if self.direction == RIGHT and level[center_y // num1][(center_x - num3) // num2] in VALID_VALUES_PLAYER:
                turns[LEFT] = True
            if self.direction == LEFT and level[center_y // num1][(center_x + num3) // num2] in VALID_VALUES_PLAYER:
                turns[RIGHT] = True
            if self.direction == UP and level[(center_y + num3) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                turns[DOWN] = True
            if self.direction == DOWN and level[(center_y - num3) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                turns[UP] = True
            
            if self.direction in [UP, DOWN]:
                if level[(center_y + num3) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                    turns[DOWN] = True
                if level[(center_y - num3) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                    turns[UP] = True
                if level[center_y // num1][(center_x - num2) // num2] in VALID_VALUES_PLAYER:
                    turns[LEFT] = True
                if level[center_y // num1][(center_x + num2) // num2] in VALID_VALUES_PLAYER:
                    turns[RIGHT] = True
            if self.direction in [RIGHT, LEFT]:
                if level[(center_y + num1) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                    turns[DOWN] = True
                if level[(center_y - num1) // num1][center_x // num2] in VALID_VALUES_PLAYER:
                    turns[UP] = True
                if level[center_y // num1][(center_x - num3) // num2] in VALID_VALUES_PLAYER:
                    turns[LEFT] = True
                if level[center_y // num1][(center_x + num3) // num2] in VALID_VALUES_PLAYER:
                    turns[RIGHT] = True
        else:
            turns[RIGHT] = True
            turns[LEFT] = True

        return turns
    
    def move_player(self):
        # r, l, u, d
        if self.direction == RIGHT and self.turns_allowed[RIGHT]:
            self.x += self.speed
        elif self.direction == LEFT and self.turns_allowed[LEFT]:
            self.x -= self.speed
        elif self.direction == UP and self.turns_allowed[UP]:
            self.y -= self.speed
        elif self.direction == DOWN and self.turns_allowed[DOWN]:
            self.y += self.speed
            
    def check_collision_no_power_up(self, ghosts): 
       if not self.power_up:
            center_x, center_y = utils.getCenter(self.x, self.y, boards)
            for ghost in ghosts:
                distance = math.sqrt((center_x - ghost.center_x) ** 2 + (center_y - ghost.center_y) ** 2)
                if distance < DISTANCE_COLLISION and not ghost.dead:  
                    if self.lives > 0:
                        self.lives -= 1
                        self.music.musicPacmanDeath()
                        time.sleep(2)
                        self.resetIntoDefault()
                        for ghost in ghosts:
                            ghost.resetIntoDefault()
                    else:
                        self.gameOver = True
                        self.moving = False
                        self.startup_counter = 0
                    break
    def eat_ghost(self, ghosts):
        center_x, center_y = utils.getCenter(self.x, self.y, boards)
        if self.power_up:
            for ghost in ghosts:
                distance = math.sqrt((center_x - ghost.center_x) ** 2 + (center_y - ghost.center_y) ** 2)
                if distance < DISTANCE_COLLISION and not ghost.dead and not ghost.eaten:  
                    ghost.eaten = True
                    self.score += SCORE_GHOST
                    ghost.dead = True
                    self.music.musicPacmanEatGhost()

    
    def isGameOver(self):
        if (self.lives == 0):
            return True
        else: 
            return False