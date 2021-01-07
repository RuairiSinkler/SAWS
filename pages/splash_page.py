import tkinter as tk

class SplashPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1, uniform="splash_rows")
        self.grid_rowconfigure(1, weight=1, uniform="splash_rows")
        self.grid_rowconfigure(2, weight=1, uniform="splash_rows")
        self.grid_columnconfigure(0, weight=1, uniform="splash_columns")
        self.grid_columnconfigure(1, weight=1, uniform="splash_columns")
        self.grid_columnconfigure(2, weight=1, uniform="splash_columns")

        button = tk.Button(
            self, text="Start", font=controller.main_font, command=lambda: self.controller.show_frame("PinPage")
        )
        button.grid(row=1, column=1, sticky="nsew")
        button = tk.Button(
            self, text="Shutdown", font=controller.main_font, command=self.controller.shutdown
        )
        button.grid(row=2, column=0, sticky="sw")