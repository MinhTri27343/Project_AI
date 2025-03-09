from utils import *
from Object.Game import Game
class Level2: 
    def __init__(self, setUp, setMoving):
        self.ghosts = [setUp.ghosts[1]]
        self.algorithms = [setUp.algorithms[1]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        self.game.run()
        