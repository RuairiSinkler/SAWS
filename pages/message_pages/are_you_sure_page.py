import tkinter as tk

class AreYouSurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        w = tk.Label(self, text="Are you sure you want to end the run?\nThe ration is not yet complete.", font=self.controller.main_font)
        w.grid(row=1, column=1, columnspan=2)

        button = tk.Button(
            self, text="Yes", font=controller.main_font, command=lambda: controller.show_frame("BatchPage")
        )
        button.grid(row=2, column=1, sticky="ew")

        button = tk.Button(
            self, text="No", font=controller.main_font, command=lambda: controller.show_frame("RunPage")
        )
        button.grid(row=2, column=2, sticky="ew")

    def display_page(self, done):
        if done:
            self.controller.show_frame("BatchPage")
        else:
            self.controller.show_frame("AreYouSurePage")