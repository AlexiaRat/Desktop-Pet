import tkinter as tk
import random

WIDTH = 600
HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10

class BreakoutGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Breakout")

        # create canvas for the game
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # initialize variables for paddle and ball
        self.paddle_x = (WIDTH - PADDLE_WIDTH) // 2
        self.paddle = self.canvas.create_rectangle(
            self.paddle_x, HEIGHT - PADDLE_HEIGHT, self.paddle_x + PADDLE_WIDTH, HEIGHT, fill="grey"
        )

        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_speed_x = random.choice([-2, 2])
        self.ball_speed_y = 4
        self.ball = self.canvas.create_oval(
            self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS, self.ball_x + BALL_RADIUS, self.ball_y + BALL_RADIUS, fill="white"
        )

        # create bricks
        self.create_bricks()

        # bind keyboard events
        self.master.bind("<Left>", self.move_paddle_left)
        self.master.bind("<Right>", self.move_paddle_right)

        # continuous game update
        self.update_game()

    def create_bricks(self):
        # initialize list for bricks
        self.bricks = []
        brick_width = 50
        brick_height = 20

        # create bricks on the screen
        for i in range(0, WIDTH, brick_width):
            for j in range(50, 150, brick_height):
                brick = self.canvas.create_rectangle(i, j, i + brick_width, j + brick_height, fill="orange")
                self.bricks.append(brick)

    def update_game(self):
        # update ball position
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # check collision with walls
        if self.ball_x <= BALL_RADIUS or self.ball_x >= WIDTH - BALL_RADIUS:
            self.ball_speed_x *= -1

        # check collision with paddle or bricks
        if self.ball_y <= BALL_RADIUS or self.hit_paddle() or self.hit_bricks():
            self.ball_speed_y *= -1

        # move the ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        # check if the ball reached the bottom
        if self.ball_y >= HEIGHT - BALL_RADIUS:
            self.show_game_over()
            return

        # check if all bricks are destroyed
        if not self.bricks:
            self.show_congratulations()
            return

        # continuous game update
        self.master.after(16, self.update_game)

    def move_paddle_left(self, event):
        # move paddle to the left
        self.paddle_x -= 10
        if self.paddle_x < 0:
            self.paddle_x = 0

        # update paddle position
        self.canvas.coords(self.paddle, self.paddle_x, HEIGHT - PADDLE_HEIGHT, self.paddle_x + PADDLE_WIDTH, HEIGHT)

    def move_paddle_right(self, event):
        # move paddle to the right
        self.paddle_x += 10
        if self.paddle_x > WIDTH - PADDLE_WIDTH:
            self.paddle_x = WIDTH - PADDLE_WIDTH

        # update paddle position
        self.canvas.coords(self.paddle, self.paddle_x, HEIGHT - PADDLE_HEIGHT, self.paddle_x + PADDLE_WIDTH, HEIGHT)

    def hit_paddle(self):
        # check collision with paddle
        paddle_coords = self.canvas.coords(self.paddle)
        return (
            paddle_coords[0] <= self.ball_x <= paddle_coords[2] and
            paddle_coords[1] <= self.ball_y + BALL_RADIUS <= paddle_coords[3]
        )

    def hit_bricks(self):
        # check collision with bricks
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if (
                brick_coords[0] <= self.ball_x <= brick_coords[2] and
                brick_coords[1] <= self.ball_y <= brick_coords[3]
            ):
                # delete brick and remove from the list
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                return True
        return False

    def show_game_over(self):
        # display game over message
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", font=("Helvetica", 24), fill="white")

    def show_congratulations(self):
        # display congratulations message
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Congratulations!", font=("Helvetica", 24), fill="white")

def main():
    # initialize the application
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
