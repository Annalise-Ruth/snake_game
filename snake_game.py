from tkinter import *
import random

# Constants
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#9FDDA4"
FOOD_COLOR = "#E0889F"
BACKGROUND_COLOR = "#99DFEC"

# Global variables
game_loop_id = None
is_paused = False
game_started = False
score = 0
direction = 'down'
SPEED = 100  # Default speed (Medium)

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x_axis, y_axis in self.coordinates:
            square = canvas.create_rectangle(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class
class Food:
    def __init__(self):
        x_axis = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y_axis = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x_axis, y_axis]

        canvas.create_oval(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Function to toggle pause/resume
def toggle_pause():
    global is_paused, game_loop_id
    if is_paused:
        is_paused = False
        game_loop_id = window.after(SPEED, next_turn, snake, food)
    else: 
        is_paused = True
        if game_loop_id:
            window.after_cancel(game_loop_id)
        show_resume_popup()

# Show pop up
def show_resume_popup():
    popup = Toplevel(window)
    popup.title("Game Paused")
    popup.geometry("200x100")
    popup.configure(bg="#9FDDA4")

    resume_button = Button(popup, text="Resume", font=('consolas', 20), command=lambda: resume_game(popup))
    resume_button.pack(pady=20)

def start_game():
    global game_started, score, direction, snake, food
    game_started = True
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete("snake")
    canvas.delete("food")
    canvas.delete("gameover")
    snake = Snake()
    food = Food()
    game_loop_id = window.after(SPEED, next_turn, snake, food)

# Function to restart the game
def restart_game():
    global score, direction, is_paused, game_started
    if not game_started:
        start_game()
    else:
        score = 0
        direction = 'down'
        label.config(text="Score:{}".format(score))
        canvas.delete("snake")
        canvas.delete("food")
        canvas.delete("gameover")
        snake = Snake()
        food = Food()
        game_loop_id = window.after(SPEED, next_turn, snake, food)

def resume_game(popup):
    global is_paused, game_loop_id
    is_paused = False
    popup.destroy()
    game_loop_id = window.after(SPEED, next_turn, snake, food)

# Direction and Collisions
def next_turn(snake, food):
    global game_loop_id

    if is_paused:
        return

    x_axis, y_axis = snake.coordinates[0]

    if direction == "up":
        y_axis -= SPACE_SIZE
    elif direction == "down":
        y_axis += SPACE_SIZE  
    elif direction == "left":
        x_axis -= SPACE_SIZE
    elif direction == "right":
        x_axis += SPACE_SIZE

    snake.coordinates.insert(0, (x_axis, y_axis))

    square = canvas.create_rectangle(x_axis, y_axis, x_axis + SPACE_SIZE, y_axis + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x_axis == food.coordinates[0] and y_axis == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    
    else:
        game_loop_id = window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x_axis, y_axis = snake.coordinates[0]
    if x_axis < 0 or x_axis >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y_axis < 0 or y_axis >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    for body_part in snake.coordinates[1:]:
        if x_axis == body_part[0] and y_axis == body_part[1]:
            print ("GAME OVER")
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="#E0889F", tag="gameover")
    show_difficulty_popup()

# Set difficulty levels (Easy, Medium, Hard)
def set_difficulty(level):
    global SPEED
    if level == 'Easy':
        SPEED = 150
    elif level == 'Medium':
        SPEED = 100
    elif level == 'Hard':
        SPEED = 50

    # Close the difficulty pop-up and start the game
    difficulty_popup.destroy()
    open_game_window()

# Open main game window
def open_game_window():
    global window, label, canvas, snake, food

    # Initialize the main game window
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    score = 0
    direction = 'down'
    is_paused = False

    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    # Pause/Resume Button
    pause_button = Button(window, text="Pause or Resume", command=toggle_pause, font=('consolas', 20))
    pause_button.pack(pady=10)

    # Start/Restart Button
    start_button = Button(window, text="Start/Restart", command=restart_game, font=('consolas', 20))
    start_button.pack(pady=10)

    # Game Canvas
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_axis = int((screen_width / 2) - (window_width / 2))
    y_axis = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x_axis}+{y_axis}")

    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    # Start the game Loop
    snake = Snake()
    food = Food()
    next_turn(snake, food)

    window.mainloop()

# Difficulty selection pop-up (This is the first thing that appears)
def show_difficulty_popup():
    global difficulty_popup
    difficulty_popup = Toplevel(window)
    difficulty_popup.title("Select Difficulty")
    difficulty_popup.geometry("400x300")
    difficulty_popup.configure(bg=BACKGROUND_COLOR)

    # Create difficulty selection buttons
    easy_button = Button(difficulty_popup, text="Easy", command=lambda: set_difficulty('Easy'), font=('consolas', 20))
    easy_button.pack(pady=20)

    medium_button = Button(difficulty_popup, text="Medium", command=lambda: set_difficulty('Medium'), font=('consolas', 20))
    medium_button.pack(pady=20)

    hard_button = Button(difficulty_popup, text="Hard", command=lambda: set_difficulty('Hard'), font=('consolas', 20))
    hard_button.pack(pady=20)

    difficulty_popup.mainloop()

# Initialize the difficulty pop-up window
window = Tk()
window.withdraw()  
show_difficulty_popup()
