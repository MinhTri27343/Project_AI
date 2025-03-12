from utils import *
from Object.Game import Game
from Test.TestMenu import *

class Level3: 
    def __init__(self, setUp, setMoving):
        self.ghosts = [setUp.ghosts[2]]
        self.algorithms = [setUp.algorithms[2]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms, 2)
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
        