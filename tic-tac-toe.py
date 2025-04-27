import pygame
import sys
import math

pygame.init()

# ألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
RED = (255, 0, 0)

# أبعاد
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# رسم النافذة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('X-O VS AI ')

# إعداد اللوحة
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# رسم خطوط الشبكة
def draw_lines():
    # خطوط أفقية
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # خطوط رأسية
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# رسم الرموز X و O
def draw_marks():
    font = pygame.font.SysFont(None, 100)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                text = font.render('X', True, RED)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2))
                screen.blit(text, text_rect)
            elif board[row][col] == 'O':
                text = font.render('O', True, BLACK)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2))
                screen.blit(text, text_rect)

# التحقق من الفوز
def check_winner(player):
    for i in range(BOARD_ROWS):
        if all(board[i][j] == player for j in range(BOARD_COLS)) or all(board[j][i] == player for j in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_ROWS-i-1] == player for i in range(BOARD_ROWS)):
        return True
    return False

# تحقق من التعادل
def is_draw():
    return all(board[row][col] != '' for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

# Minimax Algorithm
def minimax(depth, is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(depth + 1, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(depth + 1, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

# حركة الكمبيوتر
def computer_move():
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(0, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = 'O'

# عرض النتيجة
def display_winner(text):
    font = pygame.font.SysFont(None, 60)
    result_text = font.render(text, True, RED)
    text_rect = result_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(result_text, text_rect)

# إعادة تعيين اللعبة
def restart_game():
    global board, player_turn, game_over, winner_text
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player_turn = True
    game_over = False
    winner_text = ""

# المين لوب
player_turn = True
game_over = False
winner_text = ""

while True:
    screen.fill(WHITE)
    draw_lines()
    draw_marks()

    if game_over:
        display_winner(winner_text)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over and player_turn:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if board[mouseY][mouseX] == '':
                    board[mouseY][mouseX] = 'X'
                    player_turn = False

            elif game_over:
                restart_game()

    if not player_turn and not game_over:
        pygame.time.delay(300)  # تأخير بسيط ليظهر وكأن الكمبيوتر يفكر
        computer_move()
        player_turn = True

    if check_winner('X'):
        winner_text = "You Win!!"
        game_over = True
    elif check_winner('O'):
        winner_text = "AI Wins!!"
        game_over = True
    elif is_draw():
        winner_text = "Draw!"
        game_over = True

    pygame.display.update()
