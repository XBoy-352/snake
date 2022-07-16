import pygame
import random
import os

pygame.init()
pygame.display.set_caption("Snake !!")
clock = pygame.time.Clock()

# welcome screen function
def main():
    game_exit = False
    while game_exit == False:
        # welcome screen
        screen.window.fill(colors.black)
        text_screen(welcome_text)
        text_screen(press_space_text)
        
        # exit or start game logic
        for event in pygame.event.get():
            game_exit = new_or_quit(event, game_exit)

        pygame.display.update()
        clock.tick(screen.fps)

# main game function
def run_game():

    # check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    # read current hiscore
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
    hiscore = int(hiscore)

    # net score in game
    score = 0

    # create snake
    snake = snake_object(3, 15, screen.w / 2, screen.h / 2, [], 10, colors.white)
    # vecocity of snake
    x_vel = 0
    y_vel = 0

    # create food
    food = create_food()

    # game specific variables
    game_exit = False
    game_over = False
    pygame.display.update()

    # creating a gameloop
    while not game_exit:
        if game_over:
            # saving hiscore
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            # exit or continue when game over
            game_exit = game_over_fun(game_exit)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True

                # snake direction
                if event.type == pygame.KEYDOWN:
                    (x_vel, y_vel) = snake_dir(x_vel, y_vel, snake, event)

            # move the snake
            snake.x += x_vel
            snake.y += y_vel

            # fill screen colors.black
            screen.window.fill(colors.black)

            # eat food
            if abs(food.x - snake.x) < food.size and abs(food.y - snake.y) < food.size:
                (score, snake, food) = eat_food(score, snake, food)
                # manage high score
                hiscore = max(score, hiscore)

            # draw food
            pygame.draw.rect(screen.window, colors.green, [food.x, food.y, food.size, food.size])

            # show scores on screen
            show_score(score, hiscore)

            # draw snake
            head = (snake.x, snake.y)
            snake = draw_snake(snake, head)

            # if snake bit itself game over
            if(self_bit(head, snake)):
                game_over = True
        
            # make snake reappear from opposite side if it crosses boundary from one side
            snake = boundry_check(snake)

        pygame.display.update()
        clock.tick(screen.fps)
    # end gameloop

    pygame.quit()
    quit()

# helper functions
def text_screen(obj):
    # setting text style, size and color
    font = pygame.font.SysFont(None, obj.size)
    screen_text = font.render(obj.text, True, obj.color)
    # draw the text on screen
    screen.window.blit(screen_text, [obj.x, obj.y])

def plot_snake(snake):
    # draw rectangles for the points in snake
    for x, y in snake.points:
        pygame.draw.rect(screen.window, colors.white, [x, y, snake.size, snake.size])

def new_or_quit(event, game_exit):
    if event.type == pygame.QUIT:
        game_exit = True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        run_game()
    return (game_exit)

def show_score(score, hiscore):
    score_text.text = "Score: " + str(score)
    text_screen(score_text)
    hiscore_text.text = "Hiscore: " + str(hiscore)
    text_screen(hiscore_text)

def snake_dir(x_vel, y_vel, snake, event):
    # not move in directly opposite direction
    if event.key == pygame.K_RIGHT and not x_vel:
        x_vel = snake.vel
        y_vel = 0
    elif event.key == pygame.K_LEFT and not x_vel:
        x_vel = -snake.vel
        y_vel = 0
    elif event.key == pygame.K_UP and not y_vel:
        y_vel = -snake.vel
        x_vel = 0
    elif event.key == pygame.K_DOWN and not y_vel:
        y_vel = snake.vel
        x_vel = 0
    return (x_vel, y_vel)

def eat_food(score, snake, food):
    # increase score and snake length
    score += 10
    snake.length += 50
    # new food
    food = create_food()
    if score % 50 == 0:
        snake.vel += 1
    return (score, snake, food)

def draw_snake(snake, head):
    snake.points.append(head)
    # remove extra points
    if len(snake.points) > snake.length:
        del snake.points[0]
    plot_snake(snake)
    return snake

def self_bit(head, snake):
    # if head in points means self bitten
    if(head in snake.points[:-1] and len(snake.points) > 10):
        return True
    return False

def boundry_check(snake):
    # send to opposite side when sides crossed
    if snake.x < 0:
        snake.x = screen.w
    elif snake.x > screen.w:
        snake.x = 0
    elif snake.y < 0:
        snake.y = screen.h
    elif snake.y > screen.h:
        snake.y = 0
    return snake

def game_over_fun(game_exit):
    # draw game over text
    text_screen(game_over_text)
    text_screen(press_space_text)

    # new game or quit game
    for event in pygame.event.get():
        game_exit = new_or_quit(event, game_exit)
    return game_exit

def create_food():
    food = food_object(random.randint(10, screen.w - 10), random.randint(10, screen.h - 10))
    return food
# helper functions end

# classes
# game window object
class screen_object():
    def __init__(self, w, h, fps):
        self.w = w
        self.h = h
        self.fps = fps
        self.window = pygame.display.set_mode((w, h))

# creating game window
screen = screen_object(800, 600, 60)

# colors
class colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

class snake_object:
    def __init__(self, vel, size, x, y, points, length, color):
        self.vel = vel
        self.size = size
        self.x = x
        self.y = y
        self.points = points
        self.length = length
        self.color = color

class food_object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12

# text on screen class
class text_object:
    def __init__(self, text, color, size, x, y):
        self.text = text
        self.color = color
        self.size = size
        self.x = x
        self.y = y
# classes end

# text type and specifications
score_text = text_object("", colors.white, 30, 5, 5)
hiscore_text = text_object("", colors.white, 30, 150, 5)
game_over_text = text_object("Game Over :(", colors.red, 40, 315, 240)
welcome_text = text_object("Welcome :D", colors.white, 40, 325, 240)
press_space_text = text_object("Press Spacebar to continue", colors.red, 30, 275, 300)

# main function call.
main()
