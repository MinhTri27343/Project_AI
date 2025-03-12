from utils import *
from Object.Game import Game
class Level1: 
    def __init__(self, setUp, setMoving):
        self.ghosts = [setUp.ghosts[0]]
        self.algorithms = [setUp.algorithms[0]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        return self.game.run()
        