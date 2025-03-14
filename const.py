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
SPEED_PLAYER: int = 1 
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
FAST_SPEED_GHOST: int = 5
SLOW_SPEED_GHOST: int = 1
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
DISTANCE_COLLISION: int = 18

#Rank file
RANK_FILE="assets/File/rank.json"
BG_LEADERBOARD="assets/background_images/background_rank.png"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# GAME 
# TIMER_START_GAME: int = 4 # fix into 3 seconds to test games
TIMER_START_GAME: int = 5 # fix into 3 seconds to test games
TIMER_PACMAN_DEATH: int = 1

# Depth of IDS
SMALL_DEPTH_IDS: int = 1
#TODO: Sửa chỗ này 100 thành 10
LARGE_DEPTH_IDS: int = 10
DEPTH_LIMIT: int = 40