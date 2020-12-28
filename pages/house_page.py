import tkinter as tk
from tkinter import ttk

class HousePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.header = tk.Frame(self)
        self.header.pack()
        self.main = tk.Frame(self)
        self.main.pack()
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM)

        self.controller = controller

        self.ration_id = None
        self.house_dropdown = None

        explanation = tk.Label(self.header, text="Please pick a house", font=self.controller.main_font)
        explanation.pack()

        button = tk.Button(
            self.footer, text="Back", font=self.controller.main_font,
            command=lambda: self.controller.frames["RationPage"].display_page(self.ration_id)
        )

        button.pack(side=tk.LEFT)

        button = tk.Button(
            self.footer, text="Run", font=self.controller.main_font,
            command=lambda: self.controller.frames["RunPage"].display_page(self.ration_id, self.house_dropdown)
        )

        button.pack(side=tk.LEFT)

    def display_page(self, ration_id):
        self.main.destroy()
        self.main = tk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=tk.TRUE)

        houses = self.controller.ration_db.get_all_houses()
        house_names = [house[1] for house in houses]
        self.house_dropdown = ttk.Combobox(self.main, values=house_names, state="readonly", font=self.controller.main_font)
        self.house_dropdown.current(0)
        self.house_dropdown.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.ration_id = ration_id

        self.controller.show_frame("HousePage")