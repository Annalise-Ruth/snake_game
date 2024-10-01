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

    if x_axis == food.coordinates[0] and y_axis == food.coordinates[1]:
        
        global score

        score += 1

        score_label.config(text="Score:{}".format(score))

        game_canvas.delete("food")

        food = Food()

    else:
     del snake.coordinates[-1]

     game_canvas.delete(snake.squares[-1])

     del snake.squares[-1]

    if check_collisions(snake):
        game_over()


    else:
        window.after (speed, next_turn, snake, food)
   

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

    if x_axis < 0 or x_axis >= game_width:
        return True
    elif y_axis < 0 or y_axis >= game_height:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x_axis == body_part[0] and y_axis == body_part[1]:
            return True
        
    return False

def game_over():

    game_canvas.delete(ALL)
    game_canvas.create_text(game_canvas.winfo_width()/2, game_canvas.winfo_height()/2, 
                            font=('consolas', 70), text="GAME OVER", fill="#E0889F", tag="gameover")

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

#Key Bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop ()
