import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import string
import random

class Hopper(tk.Canvas):

    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.draw_hopper()

    def draw_hopper(self):
        self.delete("all")
        triangle_y = 4 * int(self['height']) / 10
        points = [0, 0, int(self['width']), 0, int(self['width']), triangle_y, int(self['width']) / 2, int(self['height']), 0, triangle_y]
        self.hopper = self.create_polygon(points, fill='black', outline='black', width=3)
        self.update()

    def fill_hopper(self, percentage):
        triangle_y = 4 * int(self['height']) / 10
        triangle_height = int(self['height']) - triangle_y
        fill_height = int(int(self['height']) * (percentage / 100.0))
        fill_y = int(self['height']) - fill_height
        if fill_height >= triangle_height:
            points = [0, fill_y, int(self['width']), fill_y, int(self['width']), triangle_y, int(self['width']) / 2, int(self['height']), 0,
                      triangle_y]
            self.fill = self.create_polygon(points, fill='yellow')
        else:
            triangle_proportion = fill_height / (triangle_height)
            fill_width = int(self['width']) * triangle_proportion
            gap = (int(self['width']) - fill_width) / 2
            points = [gap, fill_y, int(self['width']) - gap, fill_y, int(self['width']) / 2, int(self['height'])]
            self.fill = self.create_polygon(points, fill='yellow')
        self.update()

root = tk.Tk()

label_font = tkfont.Font(size=15)

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, expand=True)

ingredients_frame = tk.Frame(frame)
ingredients_frame.pack(fill="x")

hopper = Hopper(frame)
hopper.pack(fill=tk.BOTH, expand=True)

for letter in list(string.ascii_lowercase):
    label = tk.Label(
        ingredients_frame, text=letter*random.randint(5, 10), font=label_font
    )
    label.pack(side=tk.LEFT, fill="x")
    canvas = tk.Canvas(ingredients_frame, width=10, height=10)
    canvas.pack(side=tk.LEFT)
    print("a: {}".format(label.winfo_width()))
    frame.update_idletasks()
    print("b: {}".format(label.winfo_width()))
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="red")

root.mainloop()
