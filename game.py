
# SNAKE GAME USING PYGAME

import pygame
import sys
import random

import asyncio

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_SIZE = 20
FOOD_SIZE = 20
SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Load the background image
background_image = pygame.image.load("back.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Snake initial position and direction
snake_x = SCREEN_WIDTH // 2
snake_y = SCREEN_HEIGHT // 2
snake_direction = 'RIGHT'

# Snake body
snake = [{'x': snake_x, 'y': snake_y}]

# Food initial position
food_x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE)
food_y = random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE)

# Score
score = 0

# Load the highest score from a file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Game Over flag
game_over = False

# Create a font for displaying the score
font = pygame.font.Font(None, 36)


def draw_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))


def draw_high_score():
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 50))


# Game Loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the highest score to a file before quitting
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()

        # Detect key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            if event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            if event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            if event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Move the snake
    if snake_direction == 'UP':
        snake_y -= SNAKE_SIZE
    if snake_direction == 'DOWN':
        snake_y += SNAKE_SIZE
    if snake_direction == 'LEFT':
        snake_x -= SNAKE_SIZE
    if snake_direction == 'RIGHT':
        snake_x += SNAKE_SIZE

    # Check for collisions with food
    if snake_x == food_x and snake_y == food_y:
        score += 1
        # Update the highest score if needed
        if score > high_score:
            high_score = score
        food_x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE)
        food_y = random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE)
    else:
        # Remove the tail
        snake.pop()

    # Check for collisions with walls or itself
    if (snake_x < 0 or snake_x >= SCREEN_WIDTH or
        snake_y < 0 or snake_y >= SCREEN_HEIGHT or
        {'x': snake_x, 'y': snake_y} in snake):
        game_over = True

    # Add the new head
    snake.insert(0, {'x': snake_x, 'y': snake_y})

    # Display the background image
    screen.blit(background_image, (0, 0))

    # Draw the snake head as a circle
    snake_head_radius = 2 * SNAKE_SIZE // 6
    pygame.draw.circle(screen, GREEN, (snake_x + snake_head_radius, snake_y + snake_head_radius), snake_head_radius)

    # Draw the snake body except head
    for segment in snake[1:]:
        pygame.draw.rect(screen, GREEN, (segment['x'], segment['y'], SNAKE_SIZE / 2, SNAKE_SIZE / 2))

    # Draw the food
    pygame.draw.rect(screen, WHITE, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))

    # Update the display
    draw_score()
    draw_high_score()
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(SPEED)

pygame.quit()
sys.exit()
