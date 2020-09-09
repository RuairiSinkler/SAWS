import tkinter as tk
import sys
import traceback
import tkinter.font as tkfont
from pages.page_tools.font_manager import *

class ErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.main = tk.Frame(self)
        self.main.grid(row=1, column=1)

        self.font = tkfont.Font(size=self.controller.main_font['size'])

        self.title = tk.StringVar()
        title_label = tk.Label(self.main.grid, textvariable=self.title, font=self.controller.main_font)
        title_label.grid(row=0, column=0, columnspan=2)

        self.message = tk.StringVar()
        self.message_label = tk.Label(self.main.grid, textvariable=self.message, font=self.font)
        self.message_label.grid(row=1, column=0, columnspan=2)

        close_button = tk.Button(
            self.main.grid, text="Close SAWS", font=self.controller.main_font, command=lambda: sys.exit(0)
        )
        close_button.grid(row=2, column=0, sticky="ew")

        shutdown_button = tk.Button(
            self.main.grid, text="Shutdown", font=self.controller.main_font, command=self.controller.shutdown
        )
        shutdown_button.grid(row=2, column=1, sticky="ew")

        self.bind("<Configure>", self.resize)

    def display_page(self, error, non_SAWS_error=False):
        if non_SAWS_error:
            self.title.set("UNEXPECTED ERROR")
            self.message.set(traceback.format_exc())
            self.message_label['wraplength'] = 0
        else:
            self.title.set("ERROR") 
            self.message.set(str(error))
            self.message_label['wraplength'] = self.controller.winfo_width - 100
        self.controller.show_frame("ErrorPage")

    def resize(self, event):
        resize_font_height(self.font, self.controller.main_font['size'], self.main, event.height)