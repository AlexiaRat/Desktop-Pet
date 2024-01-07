import turtle
import random

# constants
WIDTH = 500
HEIGHT = 500
FOOD_SIZE = 10
DELAY = 100

# possible directions for movement
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# initialize snake and food
def reset():
    global snake, snake_direction, food_position, pen
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_direction = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    move_snake()

# move the snake
def move_snake():
    global snake_direction

    # calculate the new position of the snake's head
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    # check for collision with its own body
    if new_head in snake[:-1]:
        reset()
    else:
        snake.append(new_head)

        # check for collision with food
        if not food_collision():
            snake.pop(0)

        # check and adjust position in case of screen boundary crossing
        check_boundary()

        # update snake display
        update_snake_display()

        screen.update()

        turtle.ontimer(move_snake, DELAY)

# check for collision with food
def food_collision():
    global food_position
    if get_distance(snake[-1], food_position) < 20:
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

# generate a random position for food
def get_random_food_position():
    x = random.randint(-WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)

# calculate distance between two positions
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

# function called when the "Up" key is pressed
def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

# function called when the "Right" key is pressed
def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

# function called when the "Down" key is pressed
def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

# function called when the "Left" key is pressed
def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

# check and adjust position in case of screen boundary crossing
def check_boundary():
    if snake[-1][0] > WIDTH / 2:
        snake[-1][0] -= WIDTH
    elif snake[-1][0] < -WIDTH / 2:
        snake[-1][0] += WIDTH
    elif snake[-1][1] > HEIGHT / 2:
        snake[-1][1] -= HEIGHT
    elif snake[-1][1] < -HEIGHT / 2:
        snake[-1][1] += HEIGHT

# update snake display
def update_snake_display():
    pen.clearstamps()
    for segment in snake:
        pen.goto(segment[0], segment[1])
        pen.stamp()

# initialize screen
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgcolor("lightblue")
screen.tracer(0)

# initialize pen for snake display
pen = turtle.Turtle("square")
pen.penup()

# initialize food
food = turtle.Turtle()
food.shape("square")
food.color("red")
food.shapesize(FOOD_SIZE / 20)  # size for square
food.stamp()  # display square
food.shape("circle")
food.shapesize(FOOD_SIZE / 10)  # resize circle inside square
food.goto(-1000, -1000)  # move to an initial invisible position

# listen to keyboard input
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

# start the game
reset()
turtle.done()
