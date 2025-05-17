# go_game_board_logic.py

from go_game_constants import BOARD_SIZE, EMPTY
from go_game_rules import is_suicide, remove_dead_stones

def create_empty_board():
    """Create and return a fresh empty Go board."""
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def is_valid_position(x, y):
    """Check if the position is within board boundaries."""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def place_stone(board, x, y, player):
    """
    Attempt to place a stone for the player.
    Returns a tuple (success, captured_stones).
    """
    if not is_valid_position(x, y) or board[y][x] != EMPTY:
        return False, []  # Invalid move: out of bounds or already occupied

    if is_suicide(board, x, y, player):
        return False, []  # Invalid move: suicide

    board[y][x] = player
    captured = remove_dead_stones(board, player)
    return True, captured  # Legal move