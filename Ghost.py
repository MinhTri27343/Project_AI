import pygame
import tracemalloc
import time
from const import *
from board import boards
from Algorithm.IDS import queue_max
from InfoRecord.InfoRecord import InfoRecord
# from utils import utils.convert_coordinates, utils.ghost_status
import utils
# Xem lai eaten dung chua quen roi
class Blinky: 
    def __init__(self): 
        self.x = 320 
        self.y = 240
        self.direction = 0
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_BLINKY
        self.x_inBox = 320 
        self.y_inBox = 250
        
        
class Inky: 
    def __init__(self): 
        self.x = 260
        self.y = 240 
        self.direction = 2
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_INKY
        self.x_inBox = 260
        self.y_inBox = 250
        
class Pinky: 
    def __init__(self): 
        self.x = 250 
        self.y = 305
        self.x_inBox = 250
        self.y_inBox = 270
        self.direction = 0
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
    def __init__(self, j_coord, i_coord, img, direct, id,  screen, player, x_inBox, y_inBox):
        self.x_origin = j_coord
        self.y_origin = i_coord
        self.x_pos = j_coord
        self.y_pos = i_coord
        self.x_inBox = x_inBox
        self.y_inBox = y_inBox
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
        self.isCalculateAlgorithmTime = False
        self.info_record = None
        self.revive = False # Hoi sịnh  add 


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
        ghost1 = ["Đỏ", "Xanh", "Hồng", "Cam"]
        print("info ghost: ", ghost1[self.id], player.power_up, self.dead, self.eaten)
        if (not player.power_up and not self.dead) or (self.revive and player.power_up and not self.dead):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif player.power_up and not self.dead and not self.eaten:
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
        # start_time = time.time()
        # tracemalloc.start()
        path, expand_nodes, nameAlgorithm = self.getPathAndExpandNodes((end_center_x, end_center_y), level, name_algorithm) # Chuyen vao pos nhung lay toa do tai center 
        # current_memory, peak_memory = tracemalloc.get_traced_memory()
        # end_time = time.time()
    
        # if (self.isCalculateAlgorithmTime == False):
            # search_time = end_time - start_time
            # self.info_record = InfoRecord(self.screen, nameAlgorithm, round(search_time, 5), expand_nodes, round(current_memory / 10 ** 6, 5), round(peak_memory / 10 ** 6, 5))
            # self.info_record.showRecord()
            # self.isCalculateAlgorithmTime = True
            # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak_memory / 10**6}MB")
            # print(f"Time to find the path is {self.search_time}")
            # print(f"Expand node is {expand_nodes}")
        heightCell = (HEIGHT - 50) // len(level)
        widthCell = WIDTH // len(level[0])
        if (path and len(path) >= 2):
            if path[0] not in queue_max:
                queue_max.append(path[0])
            next_i, next_j = path[1]
            mark = False
            if next_j > ghost_j_coord and utils.isValidToRight(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                if heightCell // 2 - 2 <= self.center_y %  heightCell <= heightCell // 2 + self.speed + 1: 
                    mark = True
                    self.center_x += self.speed
                    self.direction = RIGHT
            elif next_j < ghost_j_coord and utils.isValidToLeft(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                if heightCell // 2  - 2 <= self.center_y %  heightCell <= heightCell // 2 + self.speed + 1:
                    mark = True
                    self.center_x -= self.speed
                    self.direction = LEFT
            elif next_i > ghost_i_coord and utils.isValidToDown(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + self.speed + 1:
                    mark = True  
                    self.center_y += self.speed
                    self.direction = DOWN
            elif next_i < ghost_i_coord and utils.isValidToUp(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                if widthCell // 2 - 2 <= self.center_x %  widthCell <= widthCell // 2 + self.speed + 1:
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
        elif (self.dead == False and path and len(path) == 1 and not (end_center_x - SPEED_GHOST < self.center_x < end_center_x + SPEED_GHOST and end_center_y - SPEED_GHOST < self.center_y < end_center_y + SPEED_GHOST)):
            if (self.direction == RIGHT) and utils.isValidToRight(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                self.center_x += self.speed
            elif (self.direction == LEFT) and utils.isValidToLeft(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                self.center_x -= self.speed
            elif (self.direction == UP) and utils.isValidToUp(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST):
                self.center_y -= self.speed
            elif (self.direction == DOWN) and utils.isValidToDown(self.center_x, self.center_y, self.speed, VALID_VALUES_GHOST): 
                self.center_y += self.speed
        elif (self.dead == True and path and len(path) == 1):
            print("VO123")
            self.center_x = end_center_x
            self.center_y = end_center_y
            self.dead = False
            self.eaten = False  # add 
            self.revive = True  # add 
            return False
            
        self.x_pos = self.center_x - (HEIGHT - 50) // len(boards) // 2
        self.y_pos = self.center_y - WIDTH // len(boards[0]) // 2
        # print("Ghost pos origin: ", self.x_pos, self.y_pos)
        j_coord, i_coord = utils.convert_coordinates(self.center_x, self.center_y)
        utils.ghost_status[i_coord][j_coord] = 1
        return True
        
       
        
       
