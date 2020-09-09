import tkinter as tk

class SplashPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(
            self, text="Start", font=controller.main_font, command=lambda: self.controller.show_frame("PinPage")
        )
        button.pack(fill="none", expand="True")
        button = tk.Button(
            self, text="Shutdown", font=controller.main_font, command=self.controller.shutdown
        )
        button.pack(fill="none", expand="True")