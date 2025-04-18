# # TODO: Check đúng con ma và đúng thuật toán chưa 
import sys
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
from Menu.Menu import Menu
from Leaderboard.LeaderBoard import LeaderBoard
from Music.music import Music

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
        self.music = Music()
        self.player = Player(player_x, player_y, self.screen, player_images, len(boards), len(boards[0]), self.music)
        self.board = Board(boards, self.screen, len(boards), len(boards[0]), self.player, self.font)
        self.ghosts = getGhosts(self.screen, self.player)
        self.algorithms = getAlgorithm()
        self.menu = Menu()
        self.leaderboard = LeaderBoard(self.screen, RANK_FILE, self.player)
        
    def execute(self):
        running = True
        out = True
        while(running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False    
            name_user, ind_level, out = self.menu.execute()
            if out != True:
                break

            if name_user == "":
                name_user = "Anonymous"
            if ind_level == 0:
                level1 = Level1(setup, False)
                out =  level1.execute()
            if ind_level == 1:
                level2 = Level2(setup, False)
                out = level2.execute()
            if ind_level == 2:
                level3 = Level3(setup, False)
                out = level3.execute()
            if ind_level == 3:
                level4 = Level4(setup, False)
                out = level4.execute()
            if ind_level == 4:
                level5 = Level5(setup, False)
                out = level5.execute()
            if ind_level == 5:
                level6 = Level6(setup, True, name_user)
                out = level6.execute()
            if out == False:
                break
            self.leaderboard.save_rank()
            
            if self.leaderboard.show_rank() != True:
                running = False                  
            self.player.lives = NUMBER_LIVES
        pygame.quit()
        sys.exit()




if __name__ == "__main__":
    setup = SetUpGame(boards)
    setup.execute()
    
    