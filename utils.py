from const import *
from board import boards 
from Object.Ghost import Ghost
from Object.Ghost import Blinky, Inky, Pinky, Clyde
from Algorithm.BFS import BFS
from Algorithm.AStar import AStar
from Algorithm.UCS import UCS
from Algorithm.IDS import IDS

from const import *
def getCenter(x, y, matrix):
    x = x + (WIDTH) // len(matrix[0]) // 2
    y = y + (HEIGHT - 50) // len(matrix) // 2
    return (x, y)

def convert_coordinates(center_x, center_y):
    num1 = (HEIGHT - 50) // len(boards) 
    num2 = WIDTH // len(boards[0])
    x_coordinate = center_x // num2
    y_coordinate = center_y // num1
    return x_coordinate, y_coordinate

def getGhosts(screen, player): 
    blinkyInformation = Blinky()
    inkyInformation = Inky()
    pinkyInformation = Pinky()
    clydeInformation = Clyde()
    blinky = Ghost(blinkyInformation.x, blinkyInformation.y, blinkyInformation.image, blinkyInformation.direction, blinkyInformation.id, screen, player, blinkyInformation.x_inBox, blinkyInformation.y_inBox)
    inky = Ghost(inkyInformation.x, inkyInformation.y, inkyInformation.image, inkyInformation.direction, inkyInformation.id, screen, player, inkyInformation.x_inBox, inkyInformation.y_inBox)
    pinky = Ghost(pinkyInformation.x, pinkyInformation.y, pinkyInformation.image, pinkyInformation.direction, pinkyInformation.id, screen, player, pinkyInformation.x_inBox, pinkyInformation.y_inBox)
    clyde = Ghost(clydeInformation.x, clydeInformation.y, clydeInformation.image, clydeInformation.direction, clydeInformation.id, screen, player, clydeInformation.x_inBox, clydeInformation.y_inBox)
    return [blinky, inky, pinky, clyde]

def getAlgorithm():
    # return [BFS, IDS, UCS, AStar]
    return [BFS, IDS, AStar, UCS]


def isValidToRight(center_x, center_y, domain, validValues): 
    j_coordinate, i_coordinate = convert_coordinates(center_x + domain, center_y)
    if (j_coordinate < len(boards[0]) and boards[i_coordinate][j_coordinate] in validValues):
        return True
    else: 
        return False
    
def isValidToLeft(center_x, center_y, domain, validValues): 
    j_coordinate, i_coordinate = convert_coordinates(center_x - domain, center_y)
    if (j_coordinate >= 0 and boards[i_coordinate][j_coordinate] in validValues):
        return True
    else: 
        return False
    
def isValidToUp(center_x, center_y, domain, validValues):
    j_coordinate, i_coordinate = convert_coordinates(center_x, center_y - domain)
    if (i_coordinate >= 0 and boards[i_coordinate][j_coordinate] in validValues):
        return True
    else: 
        return False

def isValidToDown(center_x, center_y, domain, validValues):
    j_coordinate, i_coordinate = convert_coordinates(center_x, center_y + domain)
    if (i_coordinate < len(boards) and boards[i_coordinate][j_coordinate] in validValues):
        return True
    else: 
        return False 
    
def resetAllGhosts(ghosts): 
    for ghost in ghosts:
        ghost.reset()
        
def isWinGame(boards): 
    for i in range(len(boards)):
        for j in range(len(boards[0])):
            if (boards[i][j] == 1):
                return False
    return True

ghost_status = [[0] * len(boards[0]) for _ in range(len(boards))]
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 128)]