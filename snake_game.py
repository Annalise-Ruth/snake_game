from tkinter import * 
import random

#Constants/Game Settings
game_width = 700
game_height = 700
speed = 100
space_size = 50
body_parts = 3
snake_color = "#9FDDA4"
food_color = "#E0889F"
background_color = "#99DFEC"

#Classes Snake and Food
class Snake:
    
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0])

        for x_axis, y_axis in self.coordinates:
            square = game_canvas.create_rectangle(x_axis, y_axis, x_axis + space_size, y_axis + space_size, fill=snake_color, tags="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
     x_axis = random.randint(0, (game_width/space_size)-1) * space_size
     y_axis = random.randint(0, (game_height/space_size)-1) * space_size 

     self.coordinates = [x_axis, y_axis]

     game_canvas.create_oval(x_axis, y_axis, x_axis + space_size, y_axis + space_size, fill=food_color, tag="food")
    
#Directions and Collisions
def next_turn(snake, food):
    
    x_axis, y_axis = snake.coordinates[0]

    if direction == "up":
        y_axis -= space_size
    elif direction == "down":
        y_axis += space_size
    elif direction == "left":
        x_axis -= space_size
    elif direction == "right":
        x_axis += space_size

    snake.coordinates.insert(0, (x_axis, y_axis))
    square = game_canvas.create_rectangle(x_axis, y_axis, x_axis + space_size, y_axis + space_size, fill=snake_color)

    snake.squares.insert(0, square)

    window.after (speed, next_turn, snake, food)

    
def change_direction(new_direction):
    pass

def check_collisions():
    pass

def game_over():
    pass

#Window Settings
window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0 
direction = 'down'

score_label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
score_label.pack()

game_canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
game_canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_axis = int((screen_width/2) - (window_width/2))
y_axis = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x_axis}+{y_axis}")

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop ()
