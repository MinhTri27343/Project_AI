from utils import *
from Object.Game import Game
class Level4: 
    def __init__(self, setUp, setMoving):
        self.ghosts = [setUp.ghosts[3]]
        self.algorithms = [setUp.algorithms[3]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        self.game.run()
        