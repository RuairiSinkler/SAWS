import tkinter as tk
from pages.page_tools.num_pad import NumPad

class PinPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.text = tk.StringVar()
        self.text.set("Please enter the PIN code:")
        explanation = tk.Label(self, textvariable=self.text, font=self.controller.main_font)
        explanation.grid(row=1, column=1)
        pin_pad = NumPad(self, controller, lambda: self.check_pin(pin_pad))
        pin_pad.grid(row=2, column=1)

    def check_pin(self, pin_pad):
        pin = pin_pad.entry.get()
        pin_cell = self.controller.ration_ex.find("PIN")
        column = pin_cell.column
        row = pin_cell.row
        set_pin = self.controller.ration_ex.read_cell(self.controller.ration_ex.get_cell(column + 1, row))
        if int(pin) == int(set_pin):
            pin_pad.clear()
            self.controller.show_frame("MainMenuPage")
        else:
            self.text.set("Incorrect PIN please try again")