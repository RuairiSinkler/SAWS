import tkinter as tk

class Hopper(tk.Canvas):

    def __init__(self, parent, controller, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.controller = controller
        self.width = width
        self.height = height
        self.triangle_y = 4 * height / 10
        self.triangle_height = self.height - self.triangle_y
        self.draw_hopper()

    def draw_hopper(self):
        self.delete("all")
        points = [0, 0, self.width, 0, self.width, self.triangle_y, self.width / 2, self.height, 0, self.triangle_y]
        self.hopper = self.create_polygon(points, fill='black', outline='black', width=3)
        self.update()

    def fill_hopper(self, percentage):
        fill_height = int(self.height * (percentage / 100.0))
        fill_y = self.height - fill_height
        if fill_height >= self.triangle_height:
            points = [0, fill_y, self.width, fill_y, self.width, self.triangle_y, self.width / 2, self.height, 0,
                      self.triangle_y]
            self.fill = self.create_polygon(points, fill='yellow')
        else:
            triangle_proportion = fill_height / (self.triangle_height)
            fill_width = self.width * triangle_proportion
            gap = (self.width - fill_width) / 2
            points = [gap, fill_y, self.width - gap, fill_y, self.width / 2, self.height]
            self.fill = self.create_polygon(points, fill='yellow')
        self.update()