import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_GAP = 10

# Ball dimensions
BALL_RADIUS = 10

# Game speed
FPS = 60
clock = pygame.time.Clock()

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# Function to draw the paddle
def draw_paddle(paddle_x):
    pygame.draw.rect(window, WHITE, (paddle_x, WINDOW_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw a brick
def draw_brick(brick_x, brick_y):
    pygame.draw.rect(window, RED, (brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Function to draw the ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(window, BLUE, (ball_x, ball_y), BALL_RADIUS)

# Function to update the game window
def update_window(paddle_x, ball_x, ball_y, bricks):
    window.fill(BLACK)
    draw_paddle(paddle_x)
    draw_ball(ball_x, ball_y)
    for brick in bricks:
        draw_brick(brick[0], brick[1])
    pygame.display.update()

# Function to start the game
def game():
    paddle_x = WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2
    ball_x = WINDOW_WIDTH // 2
    ball_y = WINDOW_HEIGHT // 2
    ball_dx = 5
    ball_dy = -5
    bricks = []

    # Create bricks
    for row in range(5):
        for col in range(WINDOW_WIDTH // (BRICK_WIDTH + BRICK_GAP)):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP)
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + 50
            bricks.append((brick_x, brick_y))

    # Track key presses
    keys = set()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                keys.add(event.key)
            if event.type == KEYUP:
                if event.key in keys:
                    keys.remove(event.key)

        # Update paddle position based on key presses
        if K_LEFT in keys:
            paddle_x -= 15
        if K_RIGHT in keys:
            paddle_x += 15

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with paddle
        if ball_y + BALL_RADIUS >= WINDOW_HEIGHT - PADDLE_HEIGHT and ball_x + BALL_RADIUS >= paddle_x and ball_x - BALL_RADIUS <= paddle_x + PADDLE_WIDTH:
            ball_dy = -ball_dy

        # Ball collision with walls
        if ball_x + BALL_RADIUS >= WINDOW_WIDTH or ball_x - BALL_RADIUS <= 0:
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS <= 0:
            ball_dy = -ball_dy

        # Ball collision with bricks
        for brick in bricks:
            brick_x, brick_y = brick
            if ball_x + BALL_RADIUS >= brick_x and ball_x - BALL_RADIUS <= brick_x + BRICK_WIDTH and ball_y + BALL_RADIUS >= brick_y and ball_y - BALL_RADIUS <= brick_y + BRICK_HEIGHT:
                ball_dy = -ball_dy
                bricks.remove(brick)
                break

        # Game over condition
        if ball_y + BALL_RADIUS >= WINDOW_HEIGHT:
            pygame.quit()
            return

        # Update the game window
        update_window(paddle_x, ball_x, ball_y, bricks)
        clock.tick(FPS)

# Start the game
game()
