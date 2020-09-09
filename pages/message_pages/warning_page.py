import tkinter as tk
import tkinter.font as tkfont
from pages.page_tools.font_manager import *

class WarningPage(tk.Frame):

    def __init__(self, parent, controller, name="WarningPage", temp=False):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.name = name
        self.active = False
        self.temp = temp

        self.font = tkfont.Font(size=25)

        self.title = tk.StringVar()
        self.title.set("WARNING")
        w = tk.Label(self, textvariable=self.title, font=self.controller.mainFont)
        w.grid(row=1, column=1)

        self.message = tk.StringVar()
        w = tk.Label(self, textvariable=self.message, font=self.font)
        w.grid(row=2, column=1)
        button = tk.Button(
            self, text="Continue", font=self.controller.mainFont, command=lambda:self.hide_page()
        )
        button.grid(row=3, column=1, sticky="ew")

        self.bind("<Configure>", self.resize)

    def display_page(self, warning, belowThis=None):
        self.active = True
        self.message.set(warning.message)
        self.controller.show_frame(self.name, belowThis=belowThis)
    
    def hide_page(self):
        self.active = False
        self.controller.hide_frame(self.name)
        if self.temp:
            del self.controller.frames[self.name]
            self.controller.warning_frames.remove(self)
            self.destroy()

    def resize(self, event):
        self.font['size'] = 25
        resize_font(self.message.get(), self.font, event.width)