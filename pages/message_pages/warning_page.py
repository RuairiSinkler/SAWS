import tkinter as tk
import tkinter.font as tkfont
from pages.page_tools.font_manager import *

class WarningPage(tk.Frame):

    def __init__(self, parent, controller, name="WarningPage", temp=False):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.name = name
        self.active = False
        self.temp = temp

        self.main = tk.Frame(self)
        self.main.grid(row=1, column=1)

        self.font = tkfont.Font(size=self.controller.main_font['size'])

        self.title = tk.StringVar()
        self.title.set("WARNING")
        title_label = tk.Label(self.main, textvariable=self.title, font=self.controller.main_font)
        title_label.pack()

        self.message = tk.StringVar()
        message_label = tk.Label(self.main, textvariable=self.message, font=self.font, wraplength=self.controller.winfo_width() - 100)
        message_label.pack()
        button = tk.Button(
            self.main, text="Continue", font=self.controller.main_font, command=lambda:self.hide_page()
        )
        button.pack()

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
        resize_font_height(self.font, self.controller.main_font['size'], self.main, event.height)