import tkinter as tk

class WarningPage(tk.Frame):

    def __init__(self, parent, controller, name="WarningPage", temp=False):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.name = name
        self.active = False
        self.temp = temp

        self.message = tk.StringVar()
        w = tk.Label(self, textvariable=self.message, font=self.controller.textFont)
        w.grid(row=1, column=1)
        button = tk.Button(
            self, text="Continue", font=self.controller.mainFont, command=lambda:self.hide_page()
        )
        button.grid(row=2, column=1, sticky="ew")

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