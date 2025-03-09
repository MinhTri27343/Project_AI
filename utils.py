from const import *
from board import boards 
from Object.Ghost import Ghost
from Object.Ghost import Blinky, Inky, Pinky, Clyde
from Algorithm.BFS import BFS
from Algorithm.AStar import AStar
from const import *
def getCenter(x, y, matrix):
    x = x + (WIDTH) // len(matrix[0]) // 2
    y = y + (HEIGHT - 50) // len(matrix) // 2
    return (x, y)

def convert_coordinates(center_x, center_y):
    num1 = (HEIGHT - 50) // 33 
    num2 = WIDTH // 30
    x_coordinate = center_x // num2
    y_coordinate = center_y // num1
    return x_coordinate, y_coordinate

def getGhosts(screen, player): 
    blinkyInformation = Blinky()
    inkyInformation = Inky()
    pinkyInformation = Pinky()
    clydeInformation = Clyde()
    blinky = Ghost(blinkyInformation.x, blinkyInformation.y, blinkyInformation.image, blinkyInformation.direction, blinkyInformation.id, screen, player)
    inky = Ghost(inkyInformation.x, inkyInformation.y, inkyInformation.image, inkyInformation.direction, inkyInformation.id, screen, player)
    pinky = Ghost(pinkyInformation.x, pinkyInformation.y, pinkyInformation.image, pinkyInformation.direction, pinkyInformation.id, screen, player)
    clyde = Ghost(clydeInformation.x, clydeInformation.y, clydeInformation.image, clydeInformation.direction, clydeInformation.id, screen, player)
    return [blinky, inky, pinky, clyde]

def getAlgorithm():
    return [BFS, BFS, AStar, AStar]


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

ghost_status = [[0] * len(boards[0]) for _ in range(len(boards))]