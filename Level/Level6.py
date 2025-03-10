from utils import *
from Object.Game import Game
class Level6: 
    def __init__(self, setUp, setMoving, name):
        self.ghosts = setUp.ghosts
        self.algorithms = setUp.algorithms
        self.moving = setMoving
        setUp.player.name = name
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        return self.game.run()
        