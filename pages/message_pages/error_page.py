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
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.font = tkfont.Font(size=25)

        self.title = tk.StringVar()
        w = tk.Label(self, textvariable=self.title, font=self.controller.mainFont)
        w.grid(row=1, column=1, columnspan=2)

        self.message = tk.StringVar()
        w = tk.Label(self, textvariable=self.message, font=self.font)
        w.grid(row=2, column=1, columnspan=2)
        button = tk.Button(
            self, text="Close SAWS", font=self.controller.mainFont, command=lambda: sys.exit(0)
        )
        button.grid(row=3, column=1, sticky="ew")
        button = tk.Button(
            self, text="Shutdown", font=self.controller.mainFont, command=self.controller.shutdown
        )
        button.grid(row=3, column=2, sticky="ew")

        self.bind("<Configure>", self.resize)

    def display_page(self, error, non_SAWS_error=False):
        if non_SAWS_error:
            self.title.set("UNEXPECTED ERROR")
            self.message.set(traceback.format_exc())
        else:
            self.title.set("ERROR") 
            self.message.set(str(error))
        self.controller.show_frame("ErrorPage")

    def resize(self, event):
        self.font['size'] = 25
        resize_font(self.message.get(), self.font, event.width)