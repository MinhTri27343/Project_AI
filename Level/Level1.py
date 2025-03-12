from utils import *
from Object.Game import Game
from Test.TestMenu import *
class Level1: 
    def __init__(self, setUp, setMoving):
        self.screen = setUp.screen
        self.ghosts = [setUp.ghosts[0]]
        self.algorithms = [setUp.algorithms[0]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms, 5)
    def execute(self):
            #=====================================
            menu_test = TestMenu(self.screen)
            menu_test.execute()
            ind_test = menu_test.ind_test
            pos_ghost, pos_player = FactoryTest.getProperties()["Test" + str(ind_test + 1)].getTest()
            self.game.ghosts[0].x_pos, self.game.ghosts[0].y_pos = pos_ghost
            self.game.player.x, self.game.player.y = pos_player
            #=====================================
            self.game.run()
            

         
        