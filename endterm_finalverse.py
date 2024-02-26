import pygame
import random

pygame.init()

# начальные настройки
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 by Zhagalbay E. (SE-2333)")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# colors
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}

# variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

# sound
pop = pygame.mixer.Sound("pop.mp3")
pops = pygame.mixer.Sound("pops.mp3")
popso = pygame.mixer.Sound("popso.mp3")
popsoc = pygame.mixer.Sound("popsoc.mp3")

# draw game over and restart
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# take your turn based direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] \
                            and not merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

    return board

# spawn new pieces randomly
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2

    if count < 1:
        full = True
    return board, full

# background
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

# items
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Function to get player's nickname
def get_player_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key in (pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
                                   pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n,
                                   pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u,
                                   pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z):
                    name += event.unicode

        screen.fill('gray')
        draw_board()
        draw_pieces(board_values)
        name_text = font.render("Enter Your Nickname: " + name, True, 'black')
        screen.blit(name_text, (10, 470))
        pygame.display.flip()

    return name

# Function to draw leaderboard
def draw_leaderboard(leaderboard):
    screen.fill('gray')
    leaderboard_text1 = font.render('Leaderboard', True, 'black')
    screen.blit(leaderboard_text1, (150, 50))
    y_offset = 100
    for entry in leaderboard:
        entry_text = font.render(f'{entry[0]}: {entry[1]}', True, 'black')
        screen.blit(entry_text, (150, y_offset))
        y_offset += 30

# Function to save leaderboard to a file
def save_leaderboard(leaderboard):
    with open('leaderboard.txt', 'w') as file:
        for entry in leaderboard:
            file.write(f'{entry[0]}:{entry[1]}\n')

# Function to load leaderboard from a file
def load_leaderboard():
    try:
        with open('leaderboard.txt', 'r') as file:
            lines = file.readlines()
            leaderboard = [tuple(line.strip().split(':')) for line in lines]
            leaderboard = [(name, int(score)) for name, score in leaderboard]
            return leaderboard
    except FileNotFoundError:
        return []

# ... (your existing code)

# Main loop
run = True
leaderboard = load_leaderboard()

while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            save_leaderboard(leaderboard)
            file = open('high_score.txt', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
                pop.play()
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
                pops.play()
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
                popso.play()
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
                popsoc.play()

            if game_over:
                if event.key == pygame.K_RETURN:
                    player_name = get_player_name()
                    leaderboard.append((player_name, score))
                    leaderboard.sort(key=lambda x: x[1], reverse=True)
                    draw_leaderboard(leaderboard)
                    pygame.display.flip()
                    pygame.time.wait(5000)  # Wait for 5 seconds before closing the game

                    # Your existing code for resetting the game
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()