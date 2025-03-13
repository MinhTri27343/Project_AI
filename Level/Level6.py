from utils import *
import utils
from Object.Game import Game
class Level6: 
    def __init__(self, setUp, setMoving, name):
        self.ghosts = setUp.ghosts
        self.algorithms = setUp.algorithms
        self.moving = setMoving
        setUp.player.name = name
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms, 5)
    def execute(self):
        if utils.info_record != None:
            utils.info_record =None
        self.game.run()
        