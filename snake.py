import random
import sys
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME - Professional")
clock = pygame.time.Clock()

# Professional Color Palette
BG_DARK = (10, 10, 20)
BG_MAIN = (20, 20, 35)
HEADER_BG = (25, 35, 60)
ACCENT = (0, 255, 150)
ACCENT_LIGHT = (100, 255, 200)
GREEN = (50, 255, 100)
GREEN_DARK = (30, 180, 80)
RED = (255, 70, 70)
ORANGE = (255, 150, 40)
YELLOW = (255, 255, 100)
WHITE = (240, 240, 245)
BLACK = (0, 0, 0)

snake_size = 20
snake_speed = 11
high_score = 0

title_font = pygame.font.SysFont("arial", 90, bold=True)
header_font = pygame.font.SysFont("arial", 50, bold=True)
large_font = pygame.font.SysFont("arial", 55, bold=True)
font = pygame.font.SysFont("arial", 42, bold=True)
medium_font = pygame.font.SysFont("arial", 35, bold=True)
small_font = pygame.font.SysFont("arial", 26)

def show_text(msg, color, x, y, f=font):
    text = f.render(msg, True, color)
    screen.blit(text, (x, y))

def draw_button(text, x, y, w, h, color, text_color, hovered=False):
    if hovered:
        c = tuple(min(c + 70, 255) for c in color)
        pygame.draw.rect(screen, c, (x, y, w, h))
        pygame.draw.rect(screen, ACCENT_LIGHT, (x, y, w, h), 5)
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.draw.rect(screen, ACCENT, (x, y, w, h), 3)
    
    t = font.render(text, True, text_color)
    tr = t.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(t, tr)

def button_check(x, y, w, h, pos):
    return x <= pos[0] <= x + w and y <= pos[1] <= y + h

def new_food():
    fx = random.randint(0, (WIDTH - snake_size) // snake_size) * snake_size
    fy = random.randint(0, (HEIGHT - 130 - snake_size) // snake_size) * snake_size + 130
    return fx, fy

def draw_header(score, high):
    pygame.draw.rect(screen, HEADER_BG, (0, 0, WIDTH, 130))
    pygame.draw.line(screen, ACCENT, (0, 130), (WIDTH, 130), 4)
    
    show_text("SCORE", ACCENT, 40, 15, medium_font)
    show_text(f"{score}", YELLOW, 40, 50, header_font)
    
    show_text("SNAKE GAME", ACCENT_LIGHT, WIDTH // 2 - 200, 30, header_font)
    
    show_text("HIGH SCORE", ORANGE, WIDTH - 320, 15, medium_font)
    show_text(f"{high}", RED, WIDTH - 300, 50, header_font)

def game_loop():
    global high_score
    
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = dy = 0
    body = []
    length = 1
    score = 0
    fx, fy = new_food()
    over = False

    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -snake_size, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = snake_size, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -snake_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, snake_size

        x += dx
        y += dy

        if x < 0 or x >= WIDTH or y < 130 or y >= HEIGHT:
            if score > high_score:
                high_score = score
            over = True
            break

        body.append([x, y])
        if len(body) > length:
            body.pop(0)

        for seg in body[:-1]:
            if seg == [x, y]:
                if score > high_score:
                    high_score = score
                over = True
                break

        if x == fx and y == fy:
            length += 1
            score += 10
            fx, fy = new_food()

        screen.fill(BG_DARK)
        pygame.draw.rect(screen, BG_MAIN, (0, 130, WIDTH, HEIGHT - 130))
        pygame.draw.rect(screen, ACCENT, (0, 130, WIDTH, HEIGHT - 130), 3)
        
        draw_header(score, high_score)

        for i, s in enumerate(body):
            if i == len(body) - 1:
                pygame.draw.rect(screen, GREEN, (s[0], s[1], snake_size, snake_size))
                pygame.draw.rect(screen, WHITE, (s[0], s[1], snake_size, snake_size), 2)
                pygame.draw.circle(screen, BLACK, (s[0] + 6, s[1] + 6), 3)
                pygame.draw.circle(screen, BLACK, (s[0] + 14, s[1] + 6), 3)
            else:
                pygame.draw.rect(screen, GREEN, (s[0], s[1], snake_size, snake_size))
                pygame.draw.rect(screen, GREEN_DARK, (s[0], s[1], snake_size, snake_size), 1)

        pygame.draw.rect(screen, RED, (fx, fy, snake_size, snake_size))
        pygame.draw.rect(screen, ORANGE, (fx + 2, fy + 2, snake_size - 4, snake_size - 4))
        pygame.draw.circle(screen, YELLOW, (fx + snake_size // 2, fy + snake_size // 2), 5)

        pygame.display.update()
        clock.tick(snake_speed)

    while True:
        screen.fill(BG_DARK)
        pygame.draw.rect(screen, HEADER_BG, (0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(screen, ACCENT, (30, 30, WIDTH - 60, HEIGHT - 60), 6)
        
        show_text("GAME OVER", RED, WIDTH // 2 - 280, 80, title_font)
        show_text(f"Score: {score}", YELLOW, WIDTH // 2 - 220, 250, large_font)
        show_text(f"High Score: {high_score}", ORANGE, WIDTH // 2 - 300, 350, large_font)

        rb = (WIDTH // 2 - 240, 470, 480, 100)
        mb = (WIDTH // 2 - 240, 590, 480, 100)
        m = pygame.mouse.get_pos()

        draw_button("RESTART [R]", rb[0], rb[1], rb[2], rb[3], GREEN, BLACK, button_check(*rb, m))
        draw_button("MENU [M]", mb[0], mb[1], mb[2], mb[3], RED, WHITE, button_check(*mb, m))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    return
                if event.key == pygame.K_m:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_check(*rb, m):
                    game_loop()
                    return
                if button_check(*mb, m):
                    return

def main_menu():
    global high_score
    while True:
        screen.fill(BG_DARK)
        pygame.draw.rect(screen, BG_MAIN, (0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(screen, ACCENT, (40, 40, WIDTH - 80, HEIGHT - 80), 6)
        pygame.draw.line(screen, ACCENT_LIGHT, (80, 180), (WIDTH - 80, 180), 3)
        
        show_text("SNAKE GAME", ACCENT_LIGHT, WIDTH // 2 - 280, 60, title_font)

        pb = (WIDTH // 2 - 240, 280, 480, 110)
        eb = (WIDTH // 2 - 240, 420, 480, 110)
        m = pygame.mouse.get_pos()

        draw_button("PLAY [SPACE]", pb[0], pb[1], pb[2], pb[3], GREEN, BLACK, button_check(*pb, m))
        draw_button("EXIT [ESC]", eb[0], eb[1], eb[2], eb[3], RED, WHITE, button_check(*eb, m))

        show_text("Use Arrow Keys to Control", WHITE, WIDTH // 2 - 280, 200, small_font)
        show_text(f"Best Score: {high_score}", YELLOW, WIDTH // 2 - 220, 600, large_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_check(*pb, m):
                    game_loop()
                if button_check(*eb, m):
                    pygame.quit()
                    sys.exit()

main_menu()