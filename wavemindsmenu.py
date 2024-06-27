import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk


def open_color_picker():
    color = colorchooser.askcolor()
    

root = tk.Tk()
root.title("Robot Control Panel")
root.minsize(600,800)
root.maxsize(600,800)
speed = 0.0
angle = 0.0
color = "#FFFFFF"
grid_size = 10
position = (0,0)
speed_label = tk.Label(root, text="Speed:")
speed_label.grid(row =0, column = 0, padx = 5, pady = 5, sticky='w')
entry_speed = tk.Entry(root,width=10)
entry_speed.grid(row = 0, column = 1, padx = 5, pady = 5, sticky='w')
angle_label = tk.Label(root, text="Angle:")
angle_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky='w')
entry_angle = tk.Entry(root,width=10)
entry_angle.grid(row = 1, column = 1, padx = 5, pady = 5, sticky='w')
color_label = tk.Label(root, text="Color:")
color_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky='w')
color_button = tk.Button(root, text="Select Color", command=open_color_picker)
color_button.grid(row = 2, column = 1, padx = 5, pady = 5, sticky='w')
grid_label = tk.Label(root, text="Grid Size:")
grid_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky='w')
entry_grid = tk.Entry(root,width=10)
entry_grid.grid(row = 3, column = 1, padx = 5, pady = 5, sticky='w')

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)
root.grid_columnconfigure(3, weight=1)
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.grid(row = 4, column = 0, columnspan=4, sticky="nsew", padx = 0, pady = 0)
root.grid_rowconfigure(4, weight=1)
canvas.delete("all")
canvas.create_rectangle(position[0], position[1], 100, 50, fill=color, outline=color, width=2)

root.mainloop()
