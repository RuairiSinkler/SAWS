import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import string
import random

class Hopper(tk.Canvas):

    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.triangle_y = 4 * self.winfo_height() / 10
        self.triangle_height = self.winfo_height() - self.triangle_y
        self.draw_hopper()

    def draw_hopper(self):
        self.delete("all")
        points = [0, 0, self.winfo_width(), 0, self.winfo_width(), self.triangle_y, self.winfo_width() / 2, self.winfo_height(), 0, self.triangle_y]
        self.hopper = self.create_polygon(points, fill='black', outline='black', width=3)
        self.update()

    def fill_hopper(self, percentage):
        fill_height = int(self.winfo_height() * (percentage / 100.0))
        fill_y = self.winfo_height() - fill_height
        if fill_height >= self.triangle_height:
            points = [0, fill_y, self.winfo_width(), fill_y, self.winfo_width(), self.triangle_y, self.winfo_width() / 2, self.winfo_height(), 0,
                      self.triangle_y]
            self.fill = self.create_polygon(points, fill='yellow')
        else:
            triangle_proportion = fill_height / (self.triangle_height)
            fill_width = self.winfo_width() * triangle_proportion
            gap = (self.winfo_width() - fill_width) / 2
            points = [gap, fill_y, self.winfo_width() - gap, fill_y, self.winfo_width() / 2, self.winfo_height()]
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
    label.pack(side=tk.LEFT)
    canvas = tk.Canvas(ingredients_frame, width=10, height=10)
    canvas.pack(side=tk.LEFT)
    print("a: {}".format(label.winfo_width()))
    frame.update_idletasks()
    print("b: {}".format(label.winfo_width()))
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="red")

root.mainloop()
