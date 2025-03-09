import pygame
from const import *
from board import boards
from utils import *
from Object.Player import Player
from Object.Board import Board
from Level.Level1 import Level1
from Level.Level2 import Level2
from Level.Level3 import Level3
from Level.Level4 import Level4
from Level.Level5 import Level5
from Level.Level6 import Level6

class SetUpGame: 
    def __init__(self, boards):
        pygame.init()
        self.timer = pygame.time.Clock()
        player_x, player_y = START_PLAYER_POSITION
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        player_images = []
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (WIDTH_PLAYER, HEIGHT_PLAYER)))
            
        self.player = Player(player_x, player_y, self.screen, player_images, len(boards), len(boards[0]))
        self.board = Board(boards, self.screen, len(boards), len(boards[0]), self.player, self.font)
        self.ghosts = getGhosts(self.screen, self.player)
        self.algorithms = getAlgorithm()
    

if __name__ == "__main__":
    setUp = SetUpGame(boards)
    level1 = Level1(setUp, False)
    level2 = Level2(setUp, False)
    level3 = Level3(setUp, True)
    level4 = Level4(setUp, False)
    level5 = Level5(setUp, False)
    level6 = Level6(setUp, True)
    level6.execute()
    
    
    # Cao: 17, Rong: 20
    # CAO = 

