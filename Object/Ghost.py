import pygame
import tracemalloc
import time
from const import *
from board import boards
from Algorithm.IDS import queue_max
from InfoRecord.InfoRecord import InfoRecord

import utils
# Xem lai eaten dung chua quen roi
class Blinky: 
    def __init__(self): 
        self.x = 358 - (WIDTH) // len(boards[0]) // 2
        self.y = 258 - (HEIGHT - 50) // len(boards) // 2
        self.direction = RIGHT
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_BLINKY
        self.x_inBox = 320 
        self.y_inBox = 250
        
        
class Inky: 
    def __init__(self): 
        self.x = 260
        self.y = 240 
        self.direction = RIGHT
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_INKY
        self.x_inBox = 260
        self.y_inBox = 250
        
class Pinky: 
    def __init__(self): 
        self.x = 220 
        self.y = 305
        self.x_inBox = 250
        self.y_inBox = 270
        self.direction = LEFT
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_PINKY

class Clyde: 
    def __init__(self): 
        self.x = 200 
        self.y = 220
        self.x_inBox = 320
        self.y_inBox = 270
        self.direction = 3
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.id = ID_CLYDE

class Ghost:
    def __init__(self, j_coord, i_coord, img, direct, id,  screen, player, x_inBox, y_inBox, board):
        self.x_origin = j_coord
        self.y_origin = i_coord
        self.x_pos = j_coord
        self.y_pos = i_coord
        self.x_inBox = x_inBox
        self.y_inBox = y_inBox
        self.center_x, self.center_y = utils.getCenter(self.x_pos, self.y_pos, boards)
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
        self.isCalculateAlgorithmTime = False
        self.revive = False # Hoi sịnh  add 
        self.player = player
        self.board = board


    def setNewPosition(self, position):
        pos_x, pos_y = position
        self.x_pos = pos_x
        self.y_pos = pos_y
        self.x_origin = pos_x
        self.y_origin = pos_y
        self.center_x, self.center_y = utils.getCenter(self.x_pos, self.y_pos, boards)
    def resetIntoDefault(self):
        self.x_pos = self.x_origin
        self.y_pos = self.y_origin
        self.center_x, self.center_y = utils.getCenter(self.x_pos, self.y_pos, boards)
        self.dead = False
        utils.ghost_status = [[0] * len(boards[0]) for _ in range(len(boards))]
    def draw(self, player):
        if (not player.power_up and not self.dead) or (self.revive and player.power_up and not self.dead and not self.eaten):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif player.power_up and not self.dead and self.eaten:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def getPath(self, end , level, name_algorithm):
        center_x, center_y = end
        player_j_coord, player_i_coord = utils.convert_coordinates(center_x, center_y)
        ghost_j_coord, ghost_i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        
        path = name_algorithm(level,  (ghost_i_coord, ghost_j_coord), (player_i_coord, player_j_coord))
        return path; 
    def getPathAndExpandNodes(self, end , level, name_algorithm):
        center_x, center_y = end
        player_j_coord, player_i_coord = utils.convert_coordinates(center_x, center_y)
        ghost_j_coord, ghost_i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        
        path, expand_nodes, self.nameAlgorithm  = name_algorithm(level,  (ghost_i_coord, ghost_j_coord), (player_i_coord, player_j_coord))
        return path, expand_nodes, self.nameAlgorithm; 
    def move_towards_end_pos(self, end_center, level, name_algorithm, player):
        end_center_x, end_center_y = end_center
        ghost_j_coord, ghost_i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[ghost_i_coord][ghost_j_coord] = 0
        path, expand_nodes, nameAlgorithm = self.getPathAndExpandNodes((end_center_x, end_center_y), level, name_algorithm) # Chuyen vao pos nhung lay toa do tai center 
        heightCell = (HEIGHT - 50) // len(level)
        widthCell = WIDTH // len(level[0])
        if (path and len(path) >= 2):
            if path[0] not in queue_max:
                queue_max.append(path[0])
            next_i, next_j = path[1]
            if next_j > ghost_j_coord and utils.isValidToRight(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_y %  heightCell < heightCell // 2 - 2:
                    self.center_y += SLOW_SPEED_GHOST
                elif self.center_y %  heightCell > heightCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_y -= SLOW_SPEED_GHOST 
                if heightCell // 2 - 2 <= self.center_y %  heightCell <= heightCell // 2 + SLOW_SPEED_GHOST + 1: 
                    self.center_x += SLOW_SPEED_GHOST
                    self.direction = RIGHT
            elif next_j < ghost_j_coord and utils.isValidToLeft(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                # print(ghosts[self.id], "Xet: ", heightCell // 2 - 2, self.center_y %  heightCell, heightCell // 2 + self.speed + 1)
                if self.center_y %  heightCell < heightCell // 2 - 2:
                    self.center_y += SLOW_SPEED_GHOST
                elif self.center_y %  heightCell > heightCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_y -= SLOW_SPEED_GHOST 
                if heightCell // 2  - 2 <= self.center_y %  heightCell <= heightCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_x -= SLOW_SPEED_GHOST
                    self.direction = LEFT
            elif next_i > ghost_i_coord and utils.isValidToDown(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_x %  widthCell < widthCell // 2 - 2:
                    self.center_x += SLOW_SPEED_GHOST 
                elif self.center_x %  widthCell > widthCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_x -= SLOW_SPEED_GHOST
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_y += SLOW_SPEED_GHOST
                    self.direction = DOWN
                
            elif next_i < ghost_i_coord and utils.isValidToUp(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_x %  widthCell < widthCell // 2 - 2:
                    self.center_x += SLOW_SPEED_GHOST
                elif self.center_x %  widthCell > widthCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_x -= SLOW_SPEED_GHOST
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + SLOW_SPEED_GHOST + 1:
                    self.center_y -= SLOW_SPEED_GHOST
                    self.direction = UP
        elif (self.dead == False and path and len(path) == 1 and not (end_center_x - SLOW_SPEED_GHOST < self.center_x < end_center_x + SLOW_SPEED_GHOST and end_center_y - SLOW_SPEED_GHOST < self.center_y < end_center_y + SLOW_SPEED_GHOST)):
            if (self.direction == RIGHT) and utils.isValidToRight(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_x += SLOW_SPEED_GHOST
            elif (self.direction == LEFT) and utils.isValidToLeft(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_x -= SLOW_SPEED_GHOST
            elif (self.direction == UP) and utils.isValidToUp(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_y -= SLOW_SPEED_GHOST
            elif (self.direction == DOWN) and utils.isValidToDown(self.center_x, self.center_y, SLOW_SPEED_GHOST, VALID_VALUES_GHOST): 
                self.center_y += SLOW_SPEED_GHOST
        elif (self.dead == True and path and len(path) == 1):
            self.center_x = end_center_x
            self.center_y = end_center_y
            self.dead = False
            self.eaten = False  # add 
            self.revive = True  # add 
            return False
            
        self.x_pos = self.center_x - (HEIGHT - 50) // len(boards) // 2
        self.y_pos = self.center_y - WIDTH // len(boards[0]) // 2
        j_coord, i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[i_coord][j_coord] = 1
        return True
    
    def move_towards_end_pos_search_first_time(self, end_center, level, path, indexCurrentPath):
        end_center_x, end_center_y = end_center
        ghost_j_coord, ghost_i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[ghost_i_coord][ghost_j_coord] = 0
        heightCell = (HEIGHT - 50) // len(level)
        widthCell = WIDTH // len(level[0])
        if (path and len(path) >= 2):
            if path[0] not in queue_max:
                queue_max.append(path[0])
            next_i, next_j = path[indexCurrentPath[0]]
            # print("next:" , next_i, next_j)
            # print("ghost: ", ghost_i_coord, ghost_j_coord, [indexCurrentPath[0]])
            if (next_i == ghost_i_coord and next_j == ghost_j_coord and indexCurrentPath[0] <= len(path) - 2): 
                indexCurrentPath[0] += 1
                 
            if next_j > ghost_j_coord and utils.isValidToRight(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_y %  heightCell < heightCell // 2 - 2:
                    self.center_y += FAST_SPEED_GHOST
                elif self.center_y %  heightCell > heightCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_y -= FAST_SPEED_GHOST 
                if heightCell // 2 - 2 <= self.center_y %  heightCell <= heightCell // 2 + FAST_SPEED_GHOST + 1: 
                    self.center_x += FAST_SPEED_GHOST
                    self.direction = RIGHT
            elif next_j < ghost_j_coord and utils.isValidToLeft(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                # print(ghosts[self.id], "Xet: ", heightCell // 2 - 2, self.center_y %  heightCell, heightCell // 2 + FAST_SPEED_GHOST + 1)
                if self.center_y %  heightCell < heightCell // 2 - 2:
                    self.center_y += FAST_SPEED_GHOST
                elif self.center_y %  heightCell > heightCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_y -= FAST_SPEED_GHOST 
                if heightCell // 2  - 2 <= self.center_y %  heightCell <= heightCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_x -= FAST_SPEED_GHOST
                    self.direction = LEFT
            elif next_i > ghost_i_coord and utils.isValidToDown(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_x %  widthCell < widthCell // 2 - 2:
                    self.center_x += FAST_SPEED_GHOST 
                elif self.center_x %  widthCell > widthCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_x -= FAST_SPEED_GHOST
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_y += FAST_SPEED_GHOST
                    self.direction = DOWN
            elif next_i < ghost_i_coord and utils.isValidToUp(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                if self.center_x %  widthCell < widthCell // 2 - 2:
                    self.center_x += FAST_SPEED_GHOST
                elif self.center_x %  widthCell > widthCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_x -= FAST_SPEED_GHOST
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + FAST_SPEED_GHOST + 1:
                    self.center_y -= FAST_SPEED_GHOST
                    self.direction = UP
        elif (self.dead == False and path and len(path) == 1 and not (end_center_x - FAST_SPEED_GHOST < self.center_x < end_center_x + FAST_SPEED_GHOST and end_center_y - FAST_SPEED_GHOST < self.center_y < end_center_y + FAST_SPEED_GHOST)):
            if (self.direction == RIGHT) and utils.isValidToRight(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_x += FAST_SPEED_GHOST
            elif (self.direction == LEFT) and utils.isValidToLeft(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_x -= FAST_SPEED_GHOST
            elif (self.direction == UP) and utils.isValidToUp(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST):
                self.center_y -= FAST_SPEED_GHOST
            elif (self.direction == DOWN) and utils.isValidToDown(self.center_x, self.center_y, FAST_SPEED_GHOST, VALID_VALUES_GHOST): 
                self.center_y += FAST_SPEED_GHOST
        elif (self.dead == True and path and len(path) == 1):
            self.center_x = end_center_x
            self.center_y = end_center_y
            self.dead = False
            self.eaten = False  # add 
            self.revive = True  # add 
            return False
            
        self.x_pos = self.center_x - (HEIGHT - 50) // len(boards) // 2
        self.y_pos = self.center_y - WIDTH // len(boards[0]) // 2
        j_coord, i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[i_coord][j_coord] = 1
        return True
        
       
        
       
