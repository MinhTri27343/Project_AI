from utils import *
from Object.Game import Game
class Level5: 
    def __init__(self, setUp, setMoving):
        self.ghosts = setUp.ghosts
        self.algorithms = setUp.algorithms
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        self.game.run()
        