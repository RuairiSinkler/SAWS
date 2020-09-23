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
        title_label = tk.Label(self.main, textvariable=self.title, font=self.controller.main_font)
        title_label.grid(row=0, column=0, columnspan=2)

        self.message = tk.StringVar()
        self.message_label = tk.Label(self.main, textvariable=self.message, font=self.font)
        self.message_label.grid(row=1, column=0, columnspan=2)

        self.close_button = tk.Button(
            self.main, text="Close SAWS", font=self.controller.main_font, command=lambda: sys.exit(0)
        )
        self.close_button.grid(row=2, column=0, sticky="ew")

        self.shutdown_button = tk.Button(
            self.main, text="Shutdown", font=self.controller.main_font, command=self.controller.shutdown
        )
        self.shutdown_button.grid(row=2, column=1, sticky="ew")

    def display_page(self, error, non_SAWS_error=False):
        if non_SAWS_error:
            self.title.set("UNEXPECTED ERROR")
            self.message.set(traceback.format_exc())
            self.message_label.config(wraplength=0)
        else:
            self.title.set("ERROR") 
            self.message.set(str(error))
            self.message_label.config(wraplength=self.controller.screen_width)
        self.resize(resize_width=non_SAWS_error)
        self.controller.show_frame("ErrorPage")

    def resize(self, resize_width=False):
        print("resize_width: {}".format(resize_width))
        height = self.winfo_height()
        width = self.winfo_width()
        resize_font_height(self.font, self.controller.main_font['size'], self.main, height - self.close_button.winfo_height())
        if resize_width:
            resize_font_width(self.message.get(), self.font, width)