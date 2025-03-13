from utils import *
import utils
from Object.Game import Game
class Level5: 
    def __init__(self, setUp, setMoving):
        self.ghosts = setUp.ghosts
        self.algorithms = setUp.algorithms
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms, 4)
    def execute(self):
        if utils.info_record != None:
            utils.info_record =None
        self.game.run()
        