from utils import *
from Object.Game import Game
class Level3: 
    def __init__(self, setUp, setMoving):
        self.ghosts = [setUp.ghosts[2]]
        self.algorithms = [setUp.algorithms[2]]
        self.moving = setMoving
        self.game = Game(setUp, setMoving, self.ghosts, self.algorithms)
    def execute(self):
        return self.game.run()
        