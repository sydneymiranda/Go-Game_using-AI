import pygame
import sys
import time
from go_game_constants import (BOARD_SIZE, BLACK, WHITE, EMPTY, PLAYER_COLOR, AI_COLOR, CELL_SIZE, BOARD_PADDING,
                               SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, LINE_COLOR, BLACK_STONE,
                               WHITE_STONE, TEXT_COLOR, TEXT_COLOR_B, TEXT_COLOR_W)
from go_game_board_logic import create_empty_board, place_stone
from go_game_ai import GoAI  # Import AI logic
from go_game_rules import check_end_game, calculate_score, is_ko, update_pass_history
from go_game_end_display import show_end_game_result

# Initialize pygame and font
pygame.init()
font = pygame.font.SysFont("Arial", 20)

# Define pass_history globally
pass_history = []

# Set a fixed time limit (10 minutes = 600 seconds)
TIME_LIMIT = 600  # 10 minutes for the player
PASS_BONUS_TIME = 30  # seconds added on pass

# Function to format time for display
def format_time(seconds):
    if seconds <= 0:
        return "Time's up!"  # Or any custom message you prefer
    minutes = int(seconds) // 60  # Convert seconds to minutes
    seconds = int(seconds) % 60  # Convert remaining seconds
    return f"{minutes}:{seconds:02d}"

def draw_board(screen, board):
    # Fill background
    screen.fill(BG_COLOR)

    # Draw vertical and horizontal grid lines
    for i in range(BOARD_SIZE):
        start_x = BOARD_PADDING + i * CELL_SIZE
        start_y = BOARD_PADDING
        end_y = BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (start_x, end_y))

        start_x = BOARD_PADDING
        start_y = BOARD_PADDING + i * CELL_SIZE
        end_x = BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, start_y))

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            stone = board[y][x]
            if stone != EMPTY:
                center_x = BOARD_PADDING + x * CELL_SIZE
                center_y = BOARD_PADDING + y * CELL_SIZE
                color = BLACK_STONE if stone == BLACK else WHITE_STONE
                pygame.draw.circle(screen, color, (center_x, center_y), CELL_SIZE // 2 - 2)


def draw_sidebar(screen, current_player, black_score=0, white_score=0, player_time_left=0, ai_time_left=0):
    sidebar_x = BOARD_PADDING * 2 + CELL_SIZE * BOARD_SIZE
    pygame.draw.rect(screen, (230, 230, 230), (sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))

    info_lines = [
        f"Turn: {'Black' if current_player == BLACK else 'White'}",
        f"Black Score: {black_score}",
        f"White Score: {white_score}",
        f"Player Time Left: {format_time(player_time_left)}",  # Updated to show player's time left
    ]

    for i, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (sidebar_x + 10, 50 + i * 40))

    # Draw Pass button
    pass_button = pygame.Rect(sidebar_x + 10, 300, 100, 40)
    pygame.draw.rect(screen, (180, 180, 180), pass_button)
    text_pass = font.render("Pass", True, (0, 0, 0))
    screen.blit(text_pass, (pass_button.x + 20, pass_button.y + 10))

    return pass_button


def color_selection_screen(screen):
    # Add UI elements for player to choose color
    screen.fill(BG_COLOR)

    text = font.render("Choose your color:", True, TEXT_COLOR)
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 100))

    black_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 200, 200, 50)
    white_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50)

    pygame.draw.rect(screen, BLACK_STONE, black_button)
    pygame.draw.rect(screen, WHITE_STONE, white_button)

    text_black = font.render("Black", True, TEXT_COLOR_W)
    text_white = font.render("White", True, TEXT_COLOR_B)

    screen.blit(text_black, (WINDOW_WIDTH // 2 - text_black.get_width() // 2, 215))
    screen.blit(text_white, (WINDOW_WIDTH // 2 - text_white.get_width() // 2, 315))

    pygame.display.flip()

    # Event loop to handle color selection
    selected_color = None
    while selected_color is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if black_button.collidepoint(mouse_x, mouse_y):
                    selected_color = BLACK
                elif white_button.collidepoint(mouse_x, mouse_y):
                    selected_color = WHITE

    return selected_color


def main():
    global pass_history  # Declare pass_history as global to modify it inside this function

    # Initialize pass_history as an empty list at the start
    pass_history = []

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Go Game (9x9)")

    # Color selection screen
    PLAYER_COLOR = color_selection_screen(screen)
    AI_COLOR = WHITE if PLAYER_COLOR == BLACK else BLACK

    ai = GoAI(board_size=BOARD_SIZE, simulations=100)

    board = create_empty_board()
    previous_board = create_empty_board()  # Initialize as an empty board
    current_player = BLACK  # Black always starts
    clock = pygame.time.Clock()

    # Initialize game time
    player_time_left = TIME_LIMIT
    ai_time_left = TIME_LIMIT
    last_move_time = time.time()  # Track the time when last move was made
    running = True

    while running:
        # Check for time depletion
        elapsed_time = time.time() - last_move_time
        if current_player == PLAYER_COLOR:
            player_time_left -= elapsed_time
        else:
            ai_time_left -= elapsed_time

        last_move_time = time.time()  # Reset the timer for next player move

        if player_time_left <= 0 or ai_time_left <= 0:
            winner = 'B' if black_score > white_score else 'W' if white_score > black_score else 'Draw'
            show_end_game_result(winner)
            running = False
            continue  # Skip further rendering this frame

        # Draw everything first (before event handling)
        draw_board(screen, board)
        black_score, white_score = calculate_score(board, komi=6.5)
        pass_button = draw_sidebar(screen, current_player, black_score, white_score, player_time_left, ai_time_left)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if pass button is clicked
                if pass_button.collidepoint(mouse_x, mouse_y) and current_player == PLAYER_COLOR:
                    print("Player passed.")
                    pass_history.append(True)
                    current_player = AI_COLOR
                    player_time_left += PASS_BONUS_TIME  # Add bonus time for pass
                    continue  # Skip stone placement

                # Check if a board position is clicked
                grid_x = (mouse_x - BOARD_PADDING + CELL_SIZE // 2) // CELL_SIZE
                grid_y = (mouse_y - BOARD_PADDING + CELL_SIZE // 2) // CELL_SIZE

                if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE and current_player == PLAYER_COLOR:
                    valid, captured = place_stone(board, grid_x, grid_y, current_player)
                    if valid:
                        if previous_board and is_ko(previous_board, board):
                            board[grid_y][grid_x] = EMPTY
                            continue
                        previous_board = [row[:] for row in board]
                        pass_history.append(False)
                        current_player = AI_COLOR  # Switch to AI

        # AI Turn
        if current_player == AI_COLOR:
            ai_move_position = ai.get_move(board, AI_COLOR)
            if ai_move_position:
                x, y = ai_move_position
                valid, captured = place_stone(board, x, y, AI_COLOR)
                if valid:
                    pass_history.append(False)
                    current_player = PLAYER_COLOR
            else:
                print("AI passed.")
                pass_history.append(True)
                current_player = PLAYER_COLOR

        # End Game Check
        if check_end_game(pass_history):
            black_score, white_score = calculate_score(board, komi=6.5)
            if black_score > white_score:
                if PLAYER_COLOR == BLACK:
                    winner = 'BP'
                else:
                    winner = 'BA'
            elif white_score > black_score:
                if PLAYER_COLOR == WHITE:
                    winner = 'WP'
                else:
                    winner = 'WA'
            else:
                winner = 'Draw'
            show_end_game_result(winner)
            running = False
            continue

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
