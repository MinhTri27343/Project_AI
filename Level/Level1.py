from utils import *
import sys
from Object.Game import Game
from Test.TestMenu import *
class Level1: 
    def __init__(self, setUp, setMoving):
        self.screen = setUp.screen
        self.ghosts = [setUp.ghosts[0]]
        self.algorithms = [setUp.algorithms[0]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms, 0)
        
    def execute(self):
        running = True
        while running:
            #=====================================
            menu_test = TestMenu(self.screen)
            menu_test.execute()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            ind_test = menu_test.ind_test
            if ind_test == -1:
                running = False
                break
            
            pos_ghost, pos_player = FactoryTest.getProperties()["Test" + str(ind_test + 1)].getTest()
            self.ghosts[0].setNewPosition(pos_ghost)
            self.game.player.setNewPosition(pos_player)
            self.ghosts[0].isCalculateAlgorithmTime = False
            #=====================================
            self.game.run()
                
                
            

         
        