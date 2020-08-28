import tkinter as tk
import sys

class ErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.message = tk.StringVar()
        w = tk.Label(self, textvariable=self.message, font=self.controller.mainFont)
        w.grid(row=1, column=1, columnspan=2)
        button = tk.Button(
            self, text="Close SAWS", font=self.controller.mainFont, command=lambda: sys.exit(0)
        )
        button.grid(row=2, column=1, sticky="ew")
        button = tk.Button(
            self, text="Shutdown", font=self.controller.mainFont, command=self.controller.shutdown
        )
        button.grid(row=2, column=2, sticky="ew")

    def display_page(self, error, non_SAWS_error=False):
        if non_SAWS_error:
            self.message.set("UNEXPECTED ERROR\n{}".format(str(error)))
        else:    
            self.message.set(str(error))
        self.controller.show_frame("ErrorPage")