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
    pass

class Food:
    pass

def next_turn():
    pass

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


window.mainloop ()
