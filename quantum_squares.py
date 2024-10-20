import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 900
FONT = pygame.font.SysFont("Arial", 28)
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)
INPUT_FONT = pygame.font.SysFont("Arial", 32)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
BLUE = (80, 80, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (220, 240, 255)
DARK_BLUE = (0, 0, 139)
YELLOW = (255, 255, 0)

# Game Variables
grid = None
control = None
points = {'R': 0, 'B': 0}
player_turn = 'R'
ai_opponent = False
player1_name = ""
player2_name = ""
max_score = 10
ai_difficulty = 0
GRID_SIZE = 5
SQUARE_SIZE = 90
MARGIN = (WIDTH - GRID_SIZE * SQUARE_SIZE) // 2
TOP_MARGIN = 150

# Create the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Squares")

def draw_particles(x, y, count, color):
    radius = 8
    spacing = 20
    if count == 1:
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), radius)
    elif count == 2:
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2 - spacing//2, y + SQUARE_SIZE//2), radius)
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2 + spacing//2, y + SQUARE_SIZE//2), radius)
    elif count == 3:
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2 - spacing//2), radius)
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2 - spacing//2, y + SQUARE_SIZE//2 + spacing//2), radius)
        pygame.draw.circle(WIN, color, (x + SQUARE_SIZE//2 + spacing//2, y + SQUARE_SIZE//2 + spacing//2), radius)

def draw_grid():
    global MARGIN, TOP_MARGIN
    WIN.fill(LIGHT_BLUE)
    
    # Draw game title
    title_text = TITLE_FONT.render("Quantum Squares", True, DARK_BLUE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
    
    # Draw player info
    p1_text = FONT.render(f"{player1_name} (Red)", True, RED)
    p2_text = FONT.render(f"{player2_name} (Blue)", True, BLUE)
    WIN.blit(p1_text, (20, 90))
    WIN.blit(p2_text, (WIDTH - 20 - p2_text.get_width(), 90))
    
    # Recalculate MARGIN and TOP_MARGIN based on GRID_SIZE
    SQUARE_SIZE = min(90, (WIDTH - 40) // GRID_SIZE)
    MARGIN = (WIDTH - GRID_SIZE * SQUARE_SIZE) // 2
    TOP_MARGIN = 150
    
    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = MARGIN + col * SQUARE_SIZE
            y = TOP_MARGIN + row * SQUARE_SIZE
            
            # Draw cell background with slight gradient based on control
            if control[row][col] == 'R':
                pygame.draw.rect(WIN, (255, 240, 240), (x, y, SQUARE_SIZE, SQUARE_SIZE))
            elif control[row][col] == 'B':
                pygame.draw.rect(WIN, (240, 240, 255), (x, y, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(WIN, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            pygame.draw.rect(WIN, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)
            
            particles = grid[row][col]
            if particles > 0:
                color = RED if control[row][col] == 'R' else BLUE if control[row][col] == 'B' else BLACK
                draw_particles(x, y, particles, color)
    
    # Display scores
    score_box_width = 150
    score_box_height = 60
    
    # Red player score box
    pygame.draw.rect(WIN, (255, 240, 240), (20, HEIGHT - 80, score_box_width, score_box_height))
    pygame.draw.rect(WIN, RED, (20, HEIGHT - 80, score_box_width, score_box_height), 2)
    score_text = FONT.render(f"Score: {points['R']}", True, RED)
    WIN.blit(score_text, (30, HEIGHT - 60))
    
    # Blue player score box
    pygame.draw.rect(WIN, (240, 240, 255), (WIDTH - 170, HEIGHT - 80, score_box_width, score_box_height))
    pygame.draw.rect(WIN, BLUE, (WIDTH - 170, HEIGHT - 80, score_box_width, score_box_height), 2)
    score_text = FONT.render(f"Score: {points['B']}", True, BLUE)
    WIN.blit(score_text, (WIDTH - 160, HEIGHT - 60))
    
    # Current turn indicator
    turn_color = RED if player_turn == 'R' else BLUE
    turn_name = player1_name if player_turn == 'R' else player2_name
    turn_text = FONT.render(f"{turn_name}'s Turn", True, turn_color)
    text_width = turn_text.get_width()
    
    # Draw turn indicator box
    box_padding = 20
    pygame.draw.rect(WIN, WHITE, 
                    (WIDTH//2 - text_width//2 - box_padding, 
                     HEIGHT - 80, 
                     text_width + 2*box_padding, 
                     score_box_height))
    pygame.draw.rect(WIN, turn_color,
                    (WIDTH//2 - text_width//2 - box_padding, 
                     HEIGHT - 80, 
                     text_width + 2*box_padding, 
                     score_box_height), 2)
    WIN.blit(turn_text, (WIDTH//2 - text_width//2, HEIGHT - 60))
    
    pygame.display.update()

def get_player_names():
    global player2_name
    p1_input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3, 200, 50)
    p2_input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    
    p1_text = ""
    p2_text = ""
    active_box = None
    cursor_visible = True
    last_cursor_toggle = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        
        # Toggle cursor visibility every 500 milliseconds
        if current_time - last_cursor_toggle > 500:
            cursor_visible = not cursor_visible
            last_cursor_toggle = current_time
        
        WIN.fill(LIGHT_BLUE)
        
        # Draw title
        title_text = TITLE_FONT.render("Enter Player Name(s)", True, DARK_BLUE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        
        # Draw input labels
        p1_label = FONT.render("P1 (Red):", True, RED)
        WIN.blit(p1_label, (p1_input_box.x - 170, p1_input_box.y + 10))
        
        # Draw input boxes
        pygame.draw.rect(WIN, WHITE, p1_input_box)
        pygame.draw.rect(WIN, RED if active_box == 1 else GRAY, p1_input_box, 2)
        
        # Handle player 1 text
        if active_box == 1:
            display_text = p1_text + ('|' if cursor_visible else '')
        else:
            display_text = p1_text
        p1_surface = INPUT_FONT.render(display_text, True, BLACK)
        WIN.blit(p1_surface, (p1_input_box.x + 5, p1_input_box.y + 10))
        
        if not ai_opponent:
            p2_label = FONT.render("P2 (Blue):", True, BLUE)
            WIN.blit(p2_label, (p2_input_box.x - 170, p2_input_box.y + 10))
            pygame.draw.rect(WIN, WHITE, p2_input_box)
            pygame.draw.rect(WIN, BLUE if active_box == 2 else GRAY, p2_input_box, 2)
            
            # Handle player 2 text
            if active_box == 2:
                display_text = p2_text + ('|' if cursor_visible else '')
            else:
                display_text = p2_text
            p2_surface = INPUT_FONT.render(display_text, True, BLACK)
            WIN.blit(p2_surface, (p2_input_box.x + 5, p2_input_box.y + 10))
        
        # Draw start button if name(s) are entered
        if p1_text and (ai_opponent or p2_text):
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT * 2 // 3, 200, 50)
            pygame.draw.rect(WIN, WHITE, button_rect)
            pygame.draw.rect(WIN, DARK_BLUE, button_rect, 2)
            start_text = FONT.render("Start Game", True, DARK_BLUE)
            WIN.blit(start_text, (button_rect.centerx - start_text.get_width() // 2,
                                  button_rect.centery - start_text.get_height() // 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            
            # Handle mouse clicks for input boxes and button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if p1_input_box.collidepoint(event.pos):
                    active_box = 1
                elif not ai_opponent and p2_input_box.collidepoint(event.pos):
                    active_box = 2
                elif p1_text and (ai_opponent or p2_text):
                    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT * 2 // 3, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        if ai_opponent:
                            player2_name = "AI"
                            return p1_text, "AI"
                        return p1_text, p2_text
                else:
                    active_box = None
            
            # Handle key inputs
            if event.type == pygame.KEYDOWN:
                if active_box == 1:
                    if event.key == pygame.K_RETURN:
                        if not ai_opponent:
                            active_box = 2
                        elif p1_text:
                            player2_name = "AI"
                            return p1_text, "AI"
                    elif event.key == pygame.K_BACKSPACE:
                        p1_text = p1_text[:-1]
                    else:
                        if len(p1_text) < 15:  # Limit name length
                            p1_text += event.unicode
                elif active_box == 2 and not ai_opponent:
                    if event.key == pygame.K_RETURN and p1_text and p2_text:
                        return p1_text, p2_text
                    elif event.key == pygame.K_BACKSPACE:
                        p2_text = p2_text[:-1]
                    else:
                        if len(p2_text) < 15:  # Limit name length
                            p2_text += event.unicode

def select_ai_difficulty():
    WIN.fill(LIGHT_BLUE)
    title_text = TITLE_FONT.render("Select AI Difficulty", True, DARK_BLUE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    options = ["Easy", "Hard"]
    button_height = 60
    button_width = 200
    button_margin = 30
    start_y = HEIGHT // 2

    while True:
        WIN.fill(LIGHT_BLUE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        for i, option in enumerate(options):
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                    start_y + i * (button_height + button_margin),
                                    button_width, button_height)
            pygame.draw.rect(WIN, WHITE, button_rect)
            pygame.draw.rect(WIN, DARK_BLUE, button_rect, 2)
            text = FONT.render(option, True, DARK_BLUE)
            WIN.blit(text, (button_rect.centerx - text.get_width() // 2,
                          button_rect.centery - text.get_height() // 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                            start_y + i * (button_height + button_margin),
                                            button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        return i  # 0 for Easy, 1 for Hard

def select_max_score():
    WIN.fill(LIGHT_BLUE)
    title_text = TITLE_FONT.render("Select Max Score", True, DARK_BLUE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    options = [5, 10, 15, 20]
    button_height = 60
    button_width = 200
    button_margin = 30
    start_y = HEIGHT // 2

    while True:
        WIN.fill(LIGHT_BLUE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        for i, score in enumerate(options):
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                    start_y + i * (button_height + button_margin),
                                    button_width, button_height)
            pygame.draw.rect(WIN, WHITE, button_rect)
            pygame.draw.rect(WIN, DARK_BLUE, button_rect, 2)
            text = FONT.render(str(score), True, DARK_BLUE)
            WIN.blit(text, (button_rect.centerx - text.get_width() // 2,
                          button_rect.centery - text.get_height() // 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, score in enumerate(options):
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                            start_y + i * (button_height + button_margin),
                                            button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        return score

def select_grid_size():
    WIN.fill(LIGHT_BLUE)
    title_text = TITLE_FONT.render("Select Grid Size", True, DARK_BLUE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    options = [3, 4, 5, 6, 7]
    button_height = 60
    button_width = 200
    button_margin = 30
    start_y = HEIGHT // 2

    while True:
        WIN.fill(LIGHT_BLUE)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        for i, size in enumerate(options):
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                    start_y + i * (button_height + button_margin),
                                    button_width, button_height)
            pygame.draw.rect(WIN, WHITE, button_rect)
            pygame.draw.rect(WIN, DARK_BLUE, button_rect, 2)
            text = FONT.render(f"{size}x{size}", True, DARK_BLUE)
            WIN.blit(text, (button_rect.centerx - text.get_width() // 2,
                          button_rect.centery - text.get_height() // 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, size in enumerate(options):
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                            start_y + i * (button_height + button_margin),
                                            button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        return size

def show_winner(winner_text):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((255, 255, 255))
    WIN.blit(overlay, (0, 0))
    
    winner_surface = TITLE_FONT.render(winner_text, True, DARK_BLUE)
    WIN.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 3))
    
    button_width = 200
    button_height = 50
    button_margin = 20
    
    play_again_rect = pygame.Rect(WIDTH // 2 - button_width - button_margin, 
                                HEIGHT // 2, button_width, button_height)
    menu_rect = pygame.Rect(WIDTH // 2 + button_margin, 
                          HEIGHT // 2, button_width, button_height)
    
    pygame.draw.rect(WIN, WHITE, play_again_rect)
    pygame.draw.rect(WIN, DARK_BLUE, play_again_rect, 2)
    pygame.draw.rect(WIN, WHITE, menu_rect)
    pygame.draw.rect(WIN, DARK_BLUE, menu_rect, 2)
    
    play_text = FONT.render("Play Again", True, DARK_BLUE)
    menu_text = FONT.render("Main Menu", True, DARK_BLUE)
    
    WIN.blit(play_text, (play_again_rect.centerx - play_text.get_width() // 2,
                        play_again_rect.centery - play_text.get_height() // 2))
    WIN.blit(menu_text, (menu_rect.centerx - menu_text.get_width() // 2,
                        menu_rect.centery - menu_text.get_height() // 2))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return "play_again"
                if menu_rect.collidepoint(event.pos):
                    return "menu"

def show_menu():
    WIN.fill(LIGHT_BLUE)
    title_text = TITLE_FONT.render("Quantum Squares", True, DARK_BLUE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    options = ["Play Against Human", "Play Against AI", "Quit"]
    button_height = 60
    button_width = 300
    button_margin = 30
    start_y = HEIGHT // 2

    for i, option in enumerate(options):
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, 
                                start_y + i * (button_height + button_margin),
                                button_width, button_height)
        pygame.draw.rect(WIN, WHITE, button_rect)
        pygame.draw.rect(WIN, DARK_BLUE, button_rect, 2)
        text = FONT.render(option, True, DARK_BLUE)
        WIN.blit(text, (button_rect.centerx - text.get_width() // 2, 
                       button_rect.centery - text.get_height() // 2))

    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, 
                                           start_y + i * (button_height + button_margin),
                                           button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        if i == 0:  # Play Against Human
                            return True, False
                        elif i == 1:  # Play Against AI
                            return True, True
                        else:  # Quit
                            return False, False

def add_particle(row, col, player):
    global player_turn, points
    if grid[row][col] < 4:
        grid[row][col] += 1
        if control[row][col] is None:
            control[row][col] = player
        if grid[row][col] == 4:
            collapse(row, col)
    player_turn = 'B' if player_turn == 'R' else 'R'

def collapse(row, col):
    global points
    collapsing_player = control[row][col]
    points[collapsing_player] += 1
    grid[row][col] = 0
    control[row][col] = None
    
    for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_row, adj_col = row + d_row, col + d_col
        if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
            grid[adj_row][adj_col] += 1
            if control[adj_row][adj_col] is None:
                control[adj_row][adj_col] = collapsing_player
            if grid[adj_row][adj_col] == 4:
                collapse(adj_row, adj_col)

def check_game_over():
    if points['R'] >= max_score:
        return f"{player1_name} wins!"
    if points['B'] >= max_score:
        return f"{player2_name} wins!"
    if np.all(grid == 3):
        return "Draw! No more moves possible."
    return None

def ai_move(difficulty):
    valid_moves = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) 
                   if grid[r][c] < 4 and (control[r][c] is None or control[r][c] == 'B')]
    
    if not valid_moves:
        return None, None
        
    if difficulty == 0:  # Easy mode - completely random
        return random.choice(valid_moves)
        
    # Hard mode - strategic
    # Prioritize moves that will lead to a collapse
    collapse_moves = [move for move in valid_moves if grid[move[0]][move[1]] == 3]
    if collapse_moves:
        return random.choice(collapse_moves)
    
    # Look for moves that can claim empty squares
    empty_moves = [move for move in valid_moves if control[move[0]][move[1]] is None]
    if empty_moves:
        return random.choice(empty_moves)
    
    # Avoid moves that give advantage to the opponent
    safe_moves = [move for move in valid_moves if not (grid[move[0]][move[1]] == 2 and control[move[0]][move[1]] == 'R')]
    if safe_moves:
        return random.choice(safe_moves)
    
    return random.choice(valid_moves)

def main():
    global player_turn, grid, control, points, ai_opponent, player1_name, player2_name, max_score, GRID_SIZE, ai_difficulty

    while True:
        play_game, ai_opponent = show_menu()
        if not play_game:
            break

        if ai_opponent:
            player1_name, _ = get_player_names()
            if player1_name is None:
                break
            player2_name = "AI"
            ai_difficulty = select_ai_difficulty()
        else:
            player1_name, player2_name = get_player_names()
            if player1_name is None or player2_name is None:
                break

        max_score = select_max_score()
        if max_score is None:
            break

        GRID_SIZE = select_grid_size()
        if GRID_SIZE is None:
            break

        while True:
            grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
            control = np.full((GRID_SIZE, GRID_SIZE), None)
            points = {'R': 0, 'B': 0}
            player_turn = 'R'
            
            run = True
            while run:
                draw_grid()
                
                if ai_opponent and player_turn == 'B':
                    pygame.time.wait(500)  # Add slight delay for AI moves
                    row, col = ai_move(ai_difficulty)
                    if row is not None and col is not None:
                        add_particle(row, col, 'B')
                        winner = check_game_over()
                        if winner:
                            draw_grid()
                            result = show_winner(winner)
                            if result == "quit":
                                return
                            elif result == "play_again":
                                break
                            else:  # result == "menu"
                                run = False
                                break
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and (player_turn == 'R' or not ai_opponent):
                        x, y = pygame.mouse.get_pos()
                        if MARGIN <= x < WIDTH - MARGIN and TOP_MARGIN <= y < HEIGHT - TOP_MARGIN:
                            col = (x - MARGIN) // SQUARE_SIZE
                            row = (y - TOP_MARGIN) // SQUARE_SIZE
                            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                                if grid[row][col] < 4 and (control[row][col] is None or control[row][col] == player_turn):
                                    add_particle(row, col, player_turn)
                                    winner = check_game_over()
                                    if winner:
                                        draw_grid()
                                        result = show_winner(winner)
                                        if result == "quit":
                                            return
                                        elif result == "play_again":
                                            run = False
                                            break
                                        else:  # result == "menu"
                                            run = False
                                            break
            
            if not run:  # If we broke out of the game loop
                if result == "menu":
                    break  # Break out of the replay loop to go back to menu

    pygame.quit()

if __name__ == "__main__":
    main()