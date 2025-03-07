# Setup screen
WIDTH: int = 600
HEIGHT: int = 634
FPS: int = 60

# DIRECTION - PLAYER
RIGHT: int = 0
LEFT: int = 1
UP: int = 2
DOWN: int = 3



# PLAYER 
SPEED_PLAYER: int = 2
WIDTH_PLAYER: int = 28
HEIGHT_PLAYER: int = 28
NUMBER_LIVES: int = 3
WIDTH_LIVES: int = 40


# GHOST 
WIDTH_GHOST: int = 28
HEIGHT_GHOST: int = 28
SPEED_GHOST: int = 2
ID_BLINKY: int = 0
ID_INKY: int = 1
ID_PINKY: int = 2
ID_CLYDE: int = 3
DIRECTIONS = [(SPEED_GHOST, 0), (-SPEED_GHOST, 0), (0, SPEED_GHOST), (0, -SPEED_GHOST)]

# POWER_UP
TIME_POWER_UP: int = 10

# MATRIX
EMPTY_BLACK_RECTANGLE: int = 0
DOT: int = 1
BIG_DOT: int = 2
VERTICAL_LINE: int = 3
HORIZONTAL_LINE: int = 4
TOP_RIGHT: int = 5
TOP_LEFT: int = 6
BOT_LEFT: int = 7
BOT_RIGHT: int = 8
GATE: int = 9


# RECTANGE: ((230, 245), (340, 285))  : (x, y)