import pygame
import sys

# Constants
WIDTH, HEIGHT = 400, 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def show_end_game_result(winner):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Over")

    font = pygame.font.SysFont("arial", 36)
    if winner == 'BP':
        message = "Black (PLAYER) Wins!"
    elif winner == 'WP':
        message = "White (PLAYER) Wins!"
    elif winner == 'BA':
        message = "Black (AI) Wins!"
    elif winner == 'WA':
        message = "White (AI) Wins!"
    else:
        message = "It's a Draw!"

    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill(WHITE)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for user to close window
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
