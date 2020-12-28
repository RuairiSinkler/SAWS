import tkinter as tk
from tkinter import ttk
from pages.page_tools.num_pad import NumPad

__all__ = ["BatchPage"]

class BatchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        explanation = tk.Label(self, text="Please enter the 6 digit Batch Number:", font=self.controller.main_font)
        explanation.grid(row=1, column=1)

        # houses = self.controller.ration_db.get_all_houses()
        # house_names = [house[1] for house in houses]
        # self.house_dropdown = ttk.Combobox(self, values=house_names, state="readonly", font=self.controller.main_font)
        # self.house_dropdown.current(0)
        # self.house_dropdown.grid(row=2, column=1)

        self.num_pad = NumPad(self, controller, lambda: self.controller.frames["RunPage"].log_run(self.house_dropdown, self.num_pad))
        self.num_pad.grid(row=2, column=1)