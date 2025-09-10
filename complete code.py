import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
TEAL = (85, 173, 191)
CYAN = (62, 163, 219)
BLUE = (0, 0, 255)
MAGENTA = (255, 0,255)
VIOLET = (75, 0 ,135)

# Sizes and proportions
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')

# Initialize the board
def initialize_board():
    return np.zeros((BOARD_ROWS, BOARD_COLS))

# Drawing the grid lines
def draw_lines(color=TEAL):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, start_pos=(0, SQUARE_SIZE * i), end_pos=(WIDTH, SQUARE_SIZE * i), width=LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, color, start_pos=(SQUARE_SIZE * i, 0), end_pos=(SQUARE_SIZE * i, HEIGHT), width=LINE_WIDTH)

# Drawing figures (X and O)
def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CYAN, center=(int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   radius=CIRCLE_RADIUS, width=CIRCLE_WIDTH)
            if board[row][col] == 2:
                pygame.draw.line(screen, RED,
                                 start_pos=(col * SQUARE_SIZE + SQUARE_SIZE // 4,
                                            row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                                          row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), width=CROSS_WIDTH)
                pygame.draw.line(screen, RED,
                                 start_pos=(col * SQUARE_SIZE + SQUARE_SIZE // 4,
                                            row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                                          row * SQUARE_SIZE + SQUARE_SIZE // 4), width=CROSS_WIDTH)

# Marking a square
def mark_square(board, row, col, player):
    board[row][col] = player

# Checking if a square is available
def available_square(board, row, col):
    return board[row][col] == 0

# Checking if the board is full
def is_board_full(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Checking if the player has won
def check_win(board, player):
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    if all(board[i][i] == player for i in range(min(BOARD_ROWS, BOARD_COLS))):
        return True
    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(min(BOARD_ROWS, BOARD_COLS))):
        return True
    return False

# Minimax algorithm to find the best move
def minimax(minimax_board, depth, is_maximizing):
    if check_win(minimax_board, 2):
        return float('inf')
    elif check_win(minimax_board, 1):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# AI's best move
def best_move(board):
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(board, move[0], move[1], player=2)
        return True
    return False

# Restart the game
def restart_game():
    return initialize_board()

# Show the start screen
def show_start_screen():
    font = pygame.font.Font(None, 74)
    screen.fill(BLACK)
    text = font.render('Press 1 to Start First', True, WHITE)
    screen.blit(text, (50, 150))
    text = font.render('Press 2 to Let AI Start', True, WHITE)
    screen.blit(text, (50, 250))
    pygame.display.update()

    # Wait for the player to choose
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    screen.fill(BLACK)#Clear the screen after selection
                    pygame.display.update()
                    return 1
                elif event.key == pygame.K_2:
                    screen.fill(BLACK)  # Clear the screen after selection
                    pygame.display.update()
                    return 2

# Main game loop
def game_loop():
    board = initialize_board()
    draw_lines()
    player = show_start_screen()
    game_over = False

    if player == 2:
        best_move(board)
        player = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE
                if available_square(board, mouseY, mouseX):
                    mark_square(board, mouseY, mouseX, player)
                    if check_win(board, player):
                        game_over = True
                    player = 3 - player  # Switch player between 1 and 2

                if not game_over and player == 2:
                    if best_move(board):
                        if check_win(board, 2):
                            game_over = True
                        player = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = restart_game()
                    game_over = False
                    player = show_start_screen()
                    if player == 2:
                        best_move(board)
                        player = 1

        draw_lines()
        draw_figures(board)

        if game_over:
            if check_win(board, 1):
                draw_figures(board)
                draw_lines(GREEN)
            elif check_win(board, 2):
                draw_figures(board)
                draw_lines(RED)
            else:
                draw_figures(board)
                draw_lines(GRAY)

        pygame.display.update()

game_loop()
