from utils import *
from Object.Game import Game
from Test.TestMenu import *
from board import boards
import utils
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
            if menu_test.execute() == False:
                return
            ind_test = menu_test.ind_test
            pos_ghost, pos_player = FactoryTest.getProperties()["Test" + str(ind_test + 1)].getTest()
            self.ghosts[0].setNewPosition(pos_ghost)
            self.game.player.setNewPosition(pos_player)
            #=====================================
            return self.game.run()
            break
                
            

         
        