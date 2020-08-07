import tkinter as tk

class WarningPage(tk.Frame):

    def __init__(self, parent, controller, temp=False):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.active = False
        self.temp = temp

        self.message = tk.StringVar()
        w = tk.Label(self, textvariable=self.message, font=self.controller.mainFont)
        w.grid(row=1, column=1, columnspan=2)
        button = tk.Button(
            self, text="Continue", font=self.controller.mainFont, command=self.hide_page
        )
        button.grid(row=2, column=1, sticky="ew")

    def display_page(self, warning, belowThis=None):
        self.active = True
        self.message.set(warning.message)
        self.controller.show_frame("WarningPage", belowThis=belowThis)
    
    def hide_page(self):
        self.active = False
        self.controller.hide_frame("WarningPage")
        if self.temp:
            self.destroy()