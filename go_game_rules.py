from go_game_constants import BOARD_SIZE, EMPTY, BLACK, WHITE


def get_opponent(player):
    """Return the opponent color."""
    return BLACK if player == WHITE else WHITE


def is_on_board(x, y):
    """Check if the coordinates (x, y) are on the board."""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def get_neighbors(x, y):
    """Get the neighboring coordinates of (x, y) on the board."""
    return [(nx, ny) for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if is_on_board(nx, ny)]


def has_liberties(board, x, y):
    """Check if a stone at (x, y) has liberties."""
    stack = [(x, y)]
    visited = set()
    color = board[y][x]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        for nx, ny in get_neighbors(cx, cy):
            if board[ny][nx] == EMPTY:
                return True
            if board[ny][nx] == color and (nx, ny) not in visited:
                stack.append((nx, ny))
    return False


def remove_dead_stones(board, player):
    """Remove dead stones of the opponent."""
    opponent = get_opponent(player)
    captured = []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == opponent and not has_liberties(board, x, y):
                board[y][x] = EMPTY
                captured.append((x, y))
    return captured


def is_suicide(board, x, y, player):
    """Check if placing a stone at (x, y) is a suicide move."""
    board[y][x] = player  # Temporarily place the stone
    captured = remove_dead_stones(board, player)

    is_suicide_move = not has_liberties(board, x, y)

    # Restore the captured stones (undo the move)
    for cx, cy in captured:
        board[cy][cx] = get_opponent(player)  # Reset opponent's stones

    # Restore the position of the placed stone to empty
    board[y][x] = EMPTY

    return is_suicide_move


def is_ko(previous_board, current_board):
    """Check if the current board state is the same as the previous one (Ko rule)."""
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if previous_board[y][x] != current_board[y][x]:
                return False
    return True


def count_captured_stones(board, player):
    """Count the number of captured stones for a player."""
    captured = 0
    for row in board:
        captured += row.count(player)
    return captured


def count_territory(board, player):
    """Count the territory (empty points surrounded by the player's stones)."""
    territory = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == EMPTY and is_surrounded_by(board, player, x, y):
                territory += 1
    return territory


def is_surrounded_by(board, player, x, y):
    """Checks if an empty space at (x, y) is surrounded by the player's stones."""
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[ny][nx] != player and board[ny][nx] != EMPTY:
                return False
    return True


def calculate_score(board, komi=6.5):
    """
    Calculate the score based on territory, captured stones, and komi.

    :param board: The current game board
    :param komi: The komi value for white player, default is 6.5
    :return: A tuple (black_score, white_score)
    """
    black_score = 0
    white_score = komi  # White gets komi

    # Count captured stones
    black_captured = count_captured_stones(board, BLACK)
    white_captured = count_captured_stones(board, WHITE)
    black_score += black_captured
    white_score += white_captured

    # Count territory (surrounded empty spaces)
    black_territory = count_territory(board, BLACK)
    white_territory = count_territory(board, WHITE)

    black_score += black_territory
    white_score += white_territory

    return black_score, white_score

# In go_game_rules.py
def check_end_game(pass_history):
    """Return True if the last two moves were passes"""
    return len(pass_history) >= 2 and pass_history[-1] and pass_history[-2]

# In go_game_rules.py
def update_pass_history(pass_history, player_passed):
    if pass_history is None:
        pass_history = []  # Reinitialize it if somehow None
    pass_history.append(player_passed)
    return pass_history

