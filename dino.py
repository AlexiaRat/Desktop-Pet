import datetime
import os
import random
import pygame

pygame.init()

# Display settings
HEIGHT = 600
WIDTH = 1100
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

RUNNING = [
	pygame.image.load(os.path.join("dino_imgs/Dino", "DinoRun1.png")),
	pygame.image.load(os.path.join("dino_imgs/Dino", "DinoRun2.png")),
]

JUMPING = pygame.image.load(os.path.join("dino_imgs/Dino", "DinoJump.png"))

DUCKING = [
	pygame.image.load(os.path.join("dino_imgs/Dino", "DinoDuck1.png")),
	pygame.image.load(os.path.join("dino_imgs/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
	pygame.image.load(os.path.join("dino_imgs/Cactus", "SmallCactus1.png")),
	pygame.image.load(os.path.join("dino_imgs/Cactus", "SmallCactus2.png")),
	pygame.image.load(os.path.join("dino_imgs/Cactus", "SmallCactus3.png")),
]

LARGE_CACTUS = [
	pygame.image.load(os.path.join("dino_imgs/Cactus", "LargeCactus1.png")),
	pygame.image.load(os.path.join("dino_imgs/Cactus", "LargeCactus2.png")),
	pygame.image.load(os.path.join("dino_imgs/Cactus", "LargeCactus3.png")),
]

BIRD = [
	pygame.image.load(os.path.join("dino_imgs/Bird", "Bird1.png")),
	pygame.image.load(os.path.join("dino_imgs/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("dino_imgs/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("dino_imgs/Other", "Track.png"))

FONT_COLOR=(0,0,0)

class Dinosaur:
    def __init__(self):
        self.x = 80
        self.y = 310
        self.y_duck = 340
        self.jmp = 8.5

        # Load dinosaur images
        self.img = {
            "duck": DUCKING,
            "run": RUNNING,
            "jump": JUMPING
        }

        # Current action and status
        self.action = {
            "duck": False,
            "run": True,
            "jump": False
        }

        self.step_index = 0
        self.jmp_speed = self.jmp
        self.image = self.img["run"][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, user_input):
        # Update dinosaur based on user input
        if self.action["duck"]:
            self.duck()
        if self.action["run"]:
            self.run()
        if self.action["jump"]:
            self.jump()

        # Update step index for animation
        if self.step_index >= 10:
            self.step_index = 0

        # Handle jump, duck, and run actions
        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.action["jump"]:
            self.action = {
                "duck": False,
                "run": False,
                "jump": True
            }
        elif user_input[pygame.K_DOWN] and not self.action["jump"]:
            self.action = {
                "duck": True,
                "run": False,
                "jump": False
            }
        elif not (self.action["jump"] or user_input[pygame.K_DOWN]):
            self.action = {
                "duck": False,
                "run": True,
                "jump": False
            }

    def update_image_and_rect(self):
        # Update image and rectangle based on current action
        if self.action["duck"]:
            current_action = "duck"
        else:
            current_action = "run"
        self.image = self.img[current_action][self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y_duck if current_action == "duck" else self.y
        self.step_index += 1

    def duck(self):
        self.update_image_and_rect()

    def run(self):
        self.update_image_and_rect()

    def jump(self):
        self.image = self.img["jump"]
        if self.action["jump"]:
            self.rect.y -= self.jmp_speed * 4
            self.jmp_speed -= 0.8
        if self.jmp_speed < -self.jmp:
            self.action["jump"] = False
            self.jmp_speed = self.jmp

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(800, 1200)
        self.y = random.randint(50, 150)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        # Update cloud position
        self.x -= game_speed
        if self.x < -self.width:
            self.reset_position()

    def reset_position(self):
        # Reset cloud position when off-screen
        self.x = WIDTH + random.randint(2000, 3000)
        self.y = random.randint(50, 150)

    def draw(self, screen):
        # Draw cloud on the screen
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, images, obstacle_type):
        # Initialize obstacle
        self.images = images
        self.type = obstacle_type
        self.rect = self.images[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self):
        # Update obstacle position
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        # Draw obstacle on the screen
        screen.blit(self.images[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, images):
        # Initialize small cactus obstacle
        obstacle_type = random.randint(0, 2)
        super().__init__(images, obstacle_type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, images):
        # Initialize large cactus obstacle
        obstacle_type = random.randint(0, 2)
        super().__init__(images, obstacle_type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, images):
        # Initialize bird obstacle
        super().__init__(images, 0)
        self.rect.y = random.choice([250, 290, 320])
        self.index = 0

    def draw(self, screen):
        # Draw bird on the screen
        if self.index >= 9:
            self.index = 0
        screen.blit(self.images[self.index // 5], self.rect)
        self.index += 1


def main():
    # Global variables to track game state
    global game_speed, x_bg, y_bg, points, obstacles, SCREEN, WIDTH, HEIGHT, FONT_COLOR

    # Initialize Pygame
    pygame.init()

    # Set up the game window
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Runner")

    # Initialize game variables
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_bg = 0
    y_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    def score():
        # Update player's score and adjust game speed
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        # Display the score on the screen
        text = font.render("Points: " + str(points), True, FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (900, 40)
        SCREEN.blit(text, text_rect)

    def background():
        # Scroll the background to create a continuous effect
        global x_bg, y_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_bg, y_bg))
        SCREEN.blit(BG, (image_width + x_bg, y_bg))
        if x_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_bg, y_bg))
            x_bg = 0
        x_bg -= game_speed

    def unpause():
        # Unpause the game
        global pause, run
        pause = False
        run = True

    def paused():
        # Display pause message and wait for unpause command
        global pause
        pause = True
        font_paused = pygame.font.Font("freesansbold.ttf", 30)
        text_paused = font_paused.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        text_rect_paused = text_paused.get_rect()
        text_rect_paused.center = (WIDTH // 2, HEIGHT // 3)
        SCREEN.blit(text_paused, text_rect_paused)
        pygame.display.update()

        while pause:
            for event_paused in pygame.event.get():
                if event_paused.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event_paused.type == pygame.KEYDOWN and event_paused.key == pygame.K_u:
                    unpause()

    while run:
        for event_main in pygame.event.get():
            if event_main.type == pygame.QUIT:
                run = False
            if event_main.type == pygame.KEYDOWN and event_main.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour

        # Adjust background color based on current time
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))  # Daytime background
        else:
            SCREEN.fill((0, 0, 0))  # Nighttime background

        # Get user input
        user_input = pygame.key.get_pressed()

        # Update and draw player
        player.draw(SCREEN)
        player.update(user_input)

        # Generate obstacles if none exist
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        # Update and draw obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            # Check for collision with player
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        # Scroll background
        background()

        # Update and draw clouds
        cloud.draw(SCREEN)
        cloud.update()

        # Display player's score
        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    # Display the main menu
    global points, FONT_COLOR, SCREEN, WIDTH, HEIGHT, RUNNING
    run_menu = True

    while run_menu:
        current_time = datetime.datetime.now().hour

        # Adjust menu background color based on current time
        if 7 < current_time < 19:
            FONT_COLOR = (0, 0, 0)
            SCREEN.fill((255, 255, 255))  # Daytime menu background
        else:
            FONT_COLOR = (255, 255, 255)
            SCREEN.fill((128, 128, 128))  # Nighttime menu background

        font_menu = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text_menu = font_menu.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text_menu = font_menu.render("Press any Key to Restart", True, FONT_COLOR)
            score_menu = font_menu.render("Your Score: " + str(points), True, FONT_COLOR)
            score_rect_menu = score_menu.get_rect()
            score_rect_menu.center = (WIDTH // 2, HEIGHT // 2 + 50)
            SCREEN.blit(score_menu, score_rect_menu)

        text_rect_menu = text_menu.get_rect()
        text_rect_menu.center = (WIDTH // 2, HEIGHT // 2)
        SCREEN.blit(text_menu, text_rect_menu)
        SCREEN.blit(RUNNING[0], (WIDTH // 2 - 20, HEIGHT // 2 - 140))
        pygame.display.update()

        for event_menu in pygame.event.get():
            if event_menu.type == pygame.QUIT:
                run_menu = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event_menu.type == pygame.KEYDOWN:
                main()

# Start the game by calling the main function
menu(0)