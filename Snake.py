import pygame
import time
import random
import os

pygame.init()

# Colors
WHITE, DARK_GRAY, BLACK, RED, GREEN, BLUE = (255, 255, 255), (50, 50, 50), (30, 30, 30), (165, 42, 42), (0, 255, 0), (50, 153, 213)

# Display settings
DIS_WIDTH, DIS_HEIGHT = 510, 510
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake')

# Clock
CLOCK = pygame.time.Clock()

# Snake settings
SNAKE_BLOCK_SIZE = 30
SNAKE_SPEED = 7

# Font
FONT_STYLE = pygame.font.SysFont("System", 30)

# Colors
BLACK = (30, 30, 30)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

def draw_grid():
    for x in range(0, DIS_WIDTH, SNAKE_BLOCK_SIZE):
        for y in range(0, DIS_HEIGHT, SNAKE_BLOCK_SIZE):
            color = BLACK if (x // SNAKE_BLOCK_SIZE + y // SNAKE_BLOCK_SIZE) % 2 == 0 else DARK_GRAY
            pygame.draw.rect(DIS, color, [x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

def draw_rect(color, x, y, width, height, radius=0):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(DIS, color, rect, border_radius=radius)

def draw_snake(snake_list):
    for i, (x, y) in enumerate(snake_list):
        # Draw white rectangle (border) only for the head
        if i == len(snake_list) - 1:
            draw_rect(WHITE, x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE, radius=8)
            # Draw blue rectangle (snake head)
            draw_rect(BLUE, x + 2, y + 2, SNAKE_BLOCK_SIZE - 4, SNAKE_BLOCK_SIZE - 4, radius=8)
        else:
            # Draw blue rectangle (snake body)
            draw_rect(BLUE, x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE, radius=8)



def draw_food(food_list, color):
    for food in food_list:
        x, y = food
        draw_rect(color, x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE, radius=4)

def display_text(text, font, color, x, y):
    value = font.render(text, True, color)
    DIS.blit(value, [x, y])

def draw_overlay(alpha):
    overlay = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
    overlay.set_alpha(alpha)
    overlay.fill(BLACK)
    DIS.blit(overlay, (0, 0))

def game_over_screen(score):
    my_font = pygame.font.SysFont('System', 50)

    high_score = get_high_score()
    score_color = GREEN if score > high_score else RED

    game_over_surface = my_font.render('Your Score is: ' + str(score), True, score_color)
    game_rect = game_over_surface.get_rect(midtop=(DIS_WIDTH / 2, DIS_HEIGHT / 4))

    high_score_surface = my_font.render('High Score is: ' + str(high_score), True, WHITE)
    high_score_rect = high_score_surface.get_rect(midtop=(DIS_WIDTH / 2, DIS_HEIGHT / 2))

    draw_overlay(150)
    DIS.blit(game_over_surface, game_rect)
    DIS.blit(high_score_surface, high_score_rect)

    try_again()

    pygame.display.flip()

def try_again():
    my_font = pygame.font.SysFont('System', 30)
    
    try_again_surface = my_font.render('Press ENTER to try again / Press ESC to exit', True, WHITE)
    try_again_rect = try_again_surface.get_rect(midtop=(DIS_WIDTH / 2, DIS_HEIGHT * 3 / 4))
    DIS.blit(try_again_surface, try_again_rect)

    pygame.display.flip()

def get_high_score():
    high_score = 0
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    return high_score

def update_high_score(score):
    high_score = get_high_score()
    
    if score > high_score:
        with open("highscore.txt", "w") as file:
            file.write(str(score))

def restart_game():
    global SNAKE_SPEED, score
    SNAKE_SPEED, score = 7, 0
    return True

def game_loop():
    global SNAKE_SPEED, score

    while True:
        game_over, restart_game_flag = False, False
        score = 0

        x1, y1 = round((DIS_WIDTH - SNAKE_BLOCK_SIZE) / (2 * SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE, round(
            (DIS_HEIGHT - SNAKE_BLOCK_SIZE) / (2 * SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE
        x1_change, y1_change = SNAKE_BLOCK_SIZE, 0
        last_direction = "RIGHT"  # Track the last direction of the snake
        key_pressed = False  # Track whether a key is already pressed

        snake_list, length_of_snake = [], 1

        food_x, food_y = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE, round(
            random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

        green_food_list, num_green_food = [[food_x, food_y]], 1
        red_food_list, num_red_food = [], 0

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if not key_pressed:  # Process key press only if a key is not already pressed
                        if event.key == pygame.K_LEFT and last_direction != "RIGHT":
                            x1_change, y1_change = -SNAKE_BLOCK_SIZE, 0
                            last_direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and last_direction != "LEFT":
                            x1_change, y1_change = SNAKE_BLOCK_SIZE, 0
                            last_direction = "RIGHT"
                        elif event.key == pygame.K_UP and last_direction != "DOWN":
                            y1_change, x1_change = -SNAKE_BLOCK_SIZE, 0
                            last_direction = "UP"
                        elif event.key == pygame.K_DOWN and last_direction != "UP":
                            y1_change, x1_change = SNAKE_BLOCK_SIZE, 0
                            last_direction = "DOWN"
                        elif event.key == pygame.K_RETURN and game_over:
                            restart_game_flag = True
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                        key_pressed = True  # Mark that a key is pressed
                elif event.type == pygame.KEYUP:
                    key_pressed = False  # Mark that a key is released

            if restart_game_flag:
                if restart_game():
                    return True

            x1, y1 = x1 + x1_change, y1 + y1_change

            if x1 < 0 or x1 >= DIS_WIDTH or y1 < 0 or y1 >= DIS_HEIGHT:
                game_over = True

            if x1 >= DIS_WIDTH:
                x1 = DIS_WIDTH - SNAKE_BLOCK_SIZE
            elif x1 < 0:
                x1 = 0

            if y1 >= DIS_HEIGHT:
                y1 = DIS_HEIGHT - SNAKE_BLOCK_SIZE
            elif y1 < 0:
                y1 = 0

            DIS.fill(BLACK)
            draw_grid()

            for red_food in red_food_list:
                draw_food([red_food], RED)

            for green_food in green_food_list:
                draw_food([green_food], GREEN)

            snake_head = pygame.Rect(x1, y1, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)
            snake_list.append([x1, y1])
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x, y in snake_list[:-1]:
                if x == x1 and y == y1:
                    game_over = True

            draw_snake(snake_list)
            display_text("Your Score: " + str(score), FONT_STYLE, WHITE, 0, 0)

            pygame.display.update()

            for red_food in red_food_list:
                if snake_head.colliderect(pygame.Rect(red_food[0], red_food[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)):
                    red_food_list.remove(red_food)
                    score -= 5
                    if length_of_snake < 1:
                        length_of_snake = 1

            for green_food in green_food_list:
                if snake_head.colliderect(pygame.Rect(green_food[0], green_food[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)):
                    green_food_list.remove(green_food)
                    score += 1
                    length_of_snake += 1

                    if len(green_food_list) < 1:
                        green_food_x, green_food_y = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE, round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                        green_food_list.append([green_food_x, green_food_y])

                    if score >= 15 and score % 10 == 0:
                        num_red_food += 1
                        for _ in range(num_red_food):
                            red_food_x, red_food_y = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE, round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                            red_food_list.append([red_food_x, red_food_y])
                    elif score % 5 == 0:
                        red_food_x, red_food_y = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE, round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                        red_food_list.append([red_food_x, red_food_y])

            CLOCK.tick(SNAKE_SPEED)

        update_high_score(score)
        game_over_screen(score)

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if restart_game():
                            return True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

if __name__ == "__main__":
    while game_loop():
        pass
    pygame.quit()
    quit()
