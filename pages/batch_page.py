import tkinter as tk
from pages.page_tools.num_pad import NumPad

__all__ = ["BatchPage"]

class BatchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        explanation = tk.Label(self, text="Please enter the 6 digit\nBatch Number:", font=self.controller.mainFont)
        explanation.grid(row=1, column=1)
        self.num_pad = NumPad(self, controller, lambda: self.controller.frames["RunPage"].log_run(self.num_pad))
        self.num_pad.grid(row=2, column=1)