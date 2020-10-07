import tkinter as tk

class Hopper(tk.Canvas):

    def __init__(self, parent, width):
        tk.Canvas.__init__(self, parent, width=width)
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