import pygame
from const import *
from board import boards
# from utils import utils.convert_coordinates, utils.ghost_status
import utils
class Blinky: 
    def __init__(self): 
        self.x = 320 
        self.y = 250
        self.direction = 0
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_BLINKY
        
        
class Inky: 
    def __init__(self): 
        self.x = 260
        self.y = 250 
        self.direction = 2
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_INKY
        
class Pinky: 
    def __init__(self): 
        self.x = 250 
        self.y = 305
        
        self.direction = 0
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_PINKY

class Clyde: 
    def __init__(self): 
        self.x = 200 
        self.y = 220
        self.direction = 3
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.id = ID_CLYDE

class Ghost:
    def __init__(self, j_coord, i_coord, img, direct, id,  screen, player):
        self.x_origin = j_coord
        self.y_origin = i_coord
        self.x_pos = j_coord
        self.y_pos = i_coord
        self.center_x, self.center_y = utils.getCenter(self.x_pos, self.y_pos, boards)
        self.speed = SPEED_GHOST
        self.img = img
        self.direction = direct
        self.dead = False
        self.in_box = False
        self.id = id
        self.screen = screen 
        self.eaten = False
        self.dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.rect = self.draw(player)
        
    def resetGhost(self):
        self.x_pos = self.x_origin
        self.y_pos = self.y_origin
        self.center_x, self.center_y = utils.getCenter(self.x_pos, self.y_pos, boards)
        self.dead = False
        
    def draw(self, player):
        if (not player.power_up and not self.dead) or (self.eaten and player.power_up and not self.dead):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif player.power_up and not self.dead and not self.eaten:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def getPath(self, player, level, name_algorithm):
        center_player_x, center_player_y = utils.getCenter(player.x, player.y, boards)
        player_j_coord, player_i_coord = utils.convert_coordinates(center_player_x, center_player_y)
        ghost_j_coord, ghost_i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        
        path = name_algorithm(level,  (ghost_i_coord, ghost_j_coord), (player_i_coord, player_j_coord))
        return path; 
    
    def move_towards_player(self, player, level, name_algorithm):
        ghost_x_coord, ghost_y_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[ghost_y_coord][ghost_x_coord] = 0
        path = self.getPath(player, level, name_algorithm)
        heightCell = (HEIGHT - 50) // len(level)
        widthCell = WIDTH // len(level[0])
        # Tra ve trang thai cua bang truoc do
        if (path and len(path) >= 2):
            next_i, next_j = path[1]
            ##cap nhat trang thai cua bang luc sau
            # Ghost nay in nguoc
            mark = False
            if next_j > ghost_x_coord:
                
                if heightCell // 2 <= self.center_y %  heightCell <= heightCell // 2 + self.speed + 1: 
                    mark = True
                    self.center_x += self.speed
                    self.direction = RIGHT
            elif next_j < ghost_x_coord:
                if heightCell // 2 <= self.center_y %  heightCell <= heightCell // 2 + self.speed + 1:
                    mark = True
                    self.center_x -= self.speed
                    self.direction = LEFT
            elif next_i > ghost_y_coord:
                if widthCell // 2 <= self.center_x %  widthCell <= widthCell // 2 + self.speed + 1:
                    mark = True  
                    self.center_y += self.speed
                    self.direction = DOWN
            elif next_i < ghost_y_coord:
                if widthCell // 2 <= self.center_x %  widthCell <= widthCell // 2 + self.speed + 1:
                    mark = True
                    self.center_y -= self.speed
                    self.direction = UP
            if mark == False: 
                if (self.direction == RIGHT) and utils.isValidToRight(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                    self.center_x += self.speed
                elif (self.direction == LEFT ) and utils.isValidToLeft(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                    self.center_x -= self.speed 
                elif (self.direction == UP) and  utils.isValidToUp(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                    self.center_y -= self.speed 
                elif (self.direction == DOWN ) and utils.isValidToDown(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):  
                    self.center_y += self.speed
        elif (path and len(path) == 1 and not (player.x - SPEED_PLAYER < self.center_x < player.x + SPEED_PLAYER) and (player.y - SPEED_PLAYER < self.center_y < player.y + SPEED_PLAYER)):
            
            if (self.direction == RIGHT):
                self.center_x += self.speed
            elif (self.direction == LEFT):
                self.center_y -= self.speed
            elif (self.direction == UP):
                self.center_y -= self.speed
            else: 
                self.center_y += self.speed
        self.x_pos = self.center_x - WIDTH_GHOST // 2
        self.y_pos = self.center_y - HEIGHT_GHOST // 2
        x_coord, y_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[y_coord][x_coord] = 1
        
        # TEST
       
        
       