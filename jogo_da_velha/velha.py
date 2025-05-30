import pygame
import sys
import random
import os

# Inicializando o pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
GRAY = (200, 200, 200)
WIN_COLOR = (0, 200, 0)

# Tamanho da janela
WIDTH = 300
HEIGHT = 400
LINE_WIDTH = 5

# Dimensões da grade
CELL_SIZE = WIDTH // 3
HEADER_HEIGHT = 100  # Espaço para cabeçalho/mensagem

# Criando a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")

# Fonte para texto
font = pygame.font.SysFont(None, 72)
menu_font = pygame.font.SysFont(None, 40)

# Sons (use sons padrão do pygame)
pygame.mixer.init()
try:
    SOUND_CLICK = pygame.mixer.Sound(pygame.mixer.get_init() and pygame.mixer.Sound(pygame.mixer.Sound(os.path.join(pygame.__path__[0], "examples", "data", "secosmic_lo.wav"))))
except Exception:
    SOUND_CLICK = None
try:
    SOUND_WIN = pygame.mixer.Sound(pygame.mixer.get_init() and pygame.mixer.Sound(pygame.mixer.Sound(os.path.join(pygame.__path__[0], "examples", "data", "boom.wav"))))
except Exception:
    SOUND_WIN = None

# Matriz do jogo
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
mode = None  # 'pvp' ou 'cpu'
win_line = None  # Para efeito visual

def draw_board(win_line=None):
    screen.fill(WHITE)
    # Desenha as linhas verticais
    for i in range(1, 3):
        pygame.draw.line(
            screen, LINE_COLOR,
            (CELL_SIZE * i, HEADER_HEIGHT),
            (CELL_SIZE * i, HEADER_HEIGHT + CELL_SIZE * 3),
            LINE_WIDTH
        )
    # Desenha as linhas horizontais
    for i in range(1, 3):
        pygame.draw.line(
            screen, LINE_COLOR,
            (0, HEADER_HEIGHT + CELL_SIZE * i),
            (WIDTH, HEADER_HEIGHT + CELL_SIZE * i),
            LINE_WIDTH
        )
    # Borda externa do tabuleiro
    pygame.draw.rect(
        screen, LINE_COLOR,
        (0, HEADER_HEIGHT, WIDTH, CELL_SIZE * 3),
        LINE_WIDTH
    )
    # Efeito visual: linha de vitória
    if win_line:
        pygame.draw.line(
            screen, WIN_COLOR,
            win_line[0], win_line[1], 8
        )

def draw_symbols():
    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol != "":
                color = X_COLOR if symbol == "X" else O_COLOR
                text = font.render(symbol, True, color)
                text_rect = text.get_rect(center=(
                    col * CELL_SIZE + CELL_SIZE // 2,
                    HEADER_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2
                ))
                screen.blit(text, text_rect)

def draw_buttons():
    """Desenha os botões de Reset e Voltar ao Menu."""
    reset_rect = pygame.Rect(20, 20, 110, 40)
    menu_rect = pygame.Rect(WIDTH - 130, 20, 110, 40)
    pygame.draw.rect(screen, GRAY, reset_rect, border_radius=8)
    pygame.draw.rect(screen, GRAY, menu_rect, border_radius=8)
    reset_text = menu_font.render("Reset", True, BLACK)
    menu_text = menu_font.render("Menu", True, BLACK)
    screen.blit(reset_text, reset_text.get_rect(center=reset_rect.center))
    screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))
    return reset_rect, menu_rect

def show_winner(winner):
    """Exibe o vencedor na tela, centralizado no tabuleiro."""
    if winner == "Empate":
        text = font.render("Empate!", True, WIN_COLOR)
    else:
        text = font.render(f"{winner} venceu!", True, WIN_COLOR)
    # Centraliza no meio do tabuleiro, não no cabeçalho
    text_rect = text.get_rect(center=(WIDTH // 2, HEADER_HEIGHT + (CELL_SIZE * 3) // 2))
    screen.blit(text, text_rect)
    

def check_winner_for_minimax(board_state):
    # Checa linhas e colunas
    for i in range(3):
        if board_state[i][0] == board_state[i][1] == board_state[i][2] != "":
            return board_state[i][0]
        if board_state[0][i] == board_state[1][i] == board_state[2][i] != "":
            return board_state[0][i]
    # Checa diagonais
    if board_state[0][0] == board_state[1][1] == board_state[2][2] != "":
        return board_state[0][0]
    if board_state[0][2] == board_state[1][1] == board_state[2][0] != "":
        return board_state[0][2]
    # Checa empate
    if all(board_state[row][col] != "" for row in range(3) for col in range(3)):
        return "Empate"
    return None

def minimax(board_state, depth, is_maximizing):
    winner = check_winner_for_minimax(board_state)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Empate":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = "O"
                    score = minimax(board_state, depth + 1, False)
                    board_state[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = "X"
                    score = minimax(board_state, depth + 1, True)
                    board_state[r][c] = ""
                    best_score = min(score, best_score)
        return best_score

def computer_move():
    """Faz a jogada do computador usando Minimax (invencível)."""
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                score = minimax(board, 0, False)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"
        if SOUND_CLICK:
            SOUND_CLICK.play()

def draw_menu():
    """Desenha o menu de seleção de modo de jogo centralizado."""
    screen.fill(WHITE)
    title = menu_font.render("Modo de jogo:", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 60))
    pvp_btn = menu_font.render("1.Contra amigo", True, BLACK)
    cpu_btn = menu_font.render("2.Contra máquina", True, BLACK)

    # Botões centralizados
    pvp_rect = pygame.Rect(WIDTH // 2 - 110, 120, 220, 50)
    cpu_rect = pygame.Rect(WIDTH // 2 - 110, 200, 220, 50)

    pygame.draw.rect(screen, GRAY, pvp_rect, border_radius=8)
    pygame.draw.rect(screen, GRAY, cpu_rect, border_radius=8)

    screen.blit(title, title_rect)
    screen.blit(pvp_btn, pvp_btn.get_rect(center=pvp_rect.center))
    screen.blit(cpu_btn, cpu_btn.get_rect(center=cpu_rect.center))
    pygame.display.update()

def reset_game():
    global board, current_player, game_over, win_line
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    win_line = None

def check_winner():
    global game_over, win_line
    # Checa linhas e colunas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            game_over = True
            win_line = (
                (0, HEADER_HEIGHT + CELL_SIZE // 2 + i * CELL_SIZE),
                (WIDTH, HEADER_HEIGHT + CELL_SIZE // 2 + i * CELL_SIZE)
            )
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            game_over = True
            win_line = (
                (CELL_SIZE // 2 + i * CELL_SIZE, HEADER_HEIGHT),
                (CELL_SIZE // 2 + i * CELL_SIZE, HEADER_HEIGHT + CELL_SIZE * 3)
            )
            return board[0][i]
    # Checa diagonais
    if board[0][0] == board[1][1] == board[2][2] != "":
        game_over = True
        win_line = (
            (0, HEADER_HEIGHT),
            (WIDTH, HEADER_HEIGHT + CELL_SIZE * 3)
        )
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        game_over = True
        win_line = (
            (WIDTH, HEADER_HEIGHT),
            (0, HEADER_HEIGHT + CELL_SIZE * 3)
        )
        return board[0][2]
    # Checa empate
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        game_over = True
        win_line = None
        return "Empate"
    return None

def play_win_sound():
    if SOUND_WIN:
        SOUND_WIN.play()

def menu_loop():
    global mode
    while mode is None:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 110 <= x <= WIDTH // 2 + 110:
                    if 120 <= y <= 170:
                        mode = 'pvp'
                    elif 200 <= y <= 250:
                        mode = 'cpu'
                if mode is not None:
                    reset_game()

menu_loop()

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            reset_rect, menu_rect = draw_buttons()
            if reset_rect.collidepoint(x, y):
                reset_game()
                continue
            if menu_rect.collidepoint(x, y):
                mode = None
                reset_game()
                menu_loop()
                break

            if not game_over:
                if y < HEADER_HEIGHT:
                    continue  # ignorar cliques no cabeçalho
                row = (y - HEADER_HEIGHT) // CELL_SIZE
                col = x // CELL_SIZE
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                    board[row][col] = current_player
                    if SOUND_CLICK:
                        SOUND_CLICK.play()
                    winner = check_winner()
                    if game_over and winner != "Empate":
                        play_win_sound()
                    if not game_over:
                        current_player = "O" if current_player == "X" else "X"

    if not game_over and mode == "cpu" and current_player == "O":
        pygame.time.wait(500)  # pequena pausa para parecer "pensamento"
        computer_move()
        winner = check_winner()
        if game_over and winner != "Empate":
            play_win_sound()
        if not game_over:
            current_player = "X"

    draw_board(win_line)
    draw_symbols()
    reset_rect, menu_rect = draw_buttons()

    if game_over:
        show_winner(check_winner())

    pygame.display.update()