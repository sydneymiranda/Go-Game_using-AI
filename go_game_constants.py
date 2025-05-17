# go_game_constants.py

# Board configuration
BOARD_SIZE = 7

# Board cell states
EMPTY = 0
BLACK = 1
WHITE = 2

# Player and AI color
PLAYER_COLOR = None   # Will be set by player choice
AI_COLOR = None       # Opposite of PLAYER_COLOR

# Display symbols (optional)
SYMBOLS = {
    EMPTY: '.',
    BLACK: '●',
    WHITE: '○',
}

# GUI constants
CELL_SIZE = 50
BOARD_PADDING = 40
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = BOARD_PADDING * 2 + CELL_SIZE * BOARD_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_PADDING * 2 + CELL_SIZE * BOARD_SIZE

# Colors
BG_COLOR = (245, 222, 179)    # Wooden background
LINE_COLOR = (0, 0, 0)
BLACK_STONE = (0, 0, 0)
WHITE_STONE = (255, 255, 255)
TEXT_COLOR = (10, 10, 10)
TEXT_COLOR_W = (255, 255, 255)
TEXT_COLOR_B = (10, 10, 10)
