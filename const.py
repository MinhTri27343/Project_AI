# Setup screen
WIDTH: int = 600
HEIGHT: int = 634
FPS: int = 60
FONT_SIZE: int = 30

# DIRECTION - PLAYER
RIGHT: int = 0
LEFT: int = 1
UP: int = 2
DOWN: int = 3
TIME_BLOCK_PLAYER: int = 0


# PLAYER 
SPEED_PLAYER: int = 2
WIDTH_PLAYER: int = 23
HEIGHT_PLAYER: int = 23
NUMBER_LIVES: int = 3
WIDTH_LIVES: int = 40
START_PLAYER_POSITION: tuple = (530, 500)
VALID_VALUES_PLAYER: list = [0, 1, 2]

# SCORE
SCORE_DOT: int = 10
SCORE_BIG_DOT: int = 50
SCORE_GHOST: int = 200

# GHOST 
WIDTH_GHOST: int = 23
HEIGHT_GHOST: int = 23 
SPEED_GHOST: int = 2
ID_BLINKY: int = 0
ID_INKY: int = 1
ID_PINKY: int = 2
ID_CLYDE: int = 3
VALID_VALUES_GHOST: list = [0, 1, 2, 9]

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


# DIRECTION
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# DISTANCE 
DISTANCE_COLLISION: int = 25

#Rank file
RANK_FILE="assets/File/rank.json"
BG_LEADERBOARD="assets/background_images/background_rank.png"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)