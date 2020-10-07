import tkinter as tk

class NumPad(tk.Frame):

    def __init__(self, parent, controller, enter_function):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.entry = tk.Entry(self, font=self.controller.main_font)
        self.entry.grid(column=0, row=0, columnspan=3)
        for number in range(1, 10):
            button = tk.Button(
                self, text=str(number), font=controller.main_font, command=lambda n=number: self.entry.insert(tk.INSERT, str(n))
            )
            button.grid(column=(number - 1) % 3, row=int((number - 1) / 3) + 1, sticky="ew")
        delete = tk.Button(
            self, text="  DEL  ", font=controller.main_font, command=lambda: self.entry.delete(self.entry.index(tk.INSERT) - 1)
        )
        delete.grid(column=0, row=4, sticky="ew")
        zero = tk.Button(
            self, text="   0   ", font=controller.main_font, command=lambda: self.entry.insert(tk.INSERT, "0")
        )
        zero.grid(column=1, row=4, sticky="ew")
        enter = tk.Button(
            self, text="ENTER", font=controller.main_font, command=enter_function
        )
        enter.grid(column=2, row=4, sticky="ew")

    def clear(self):
        self.entry.delete(0, tk.INSERT)