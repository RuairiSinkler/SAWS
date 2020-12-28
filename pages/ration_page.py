import tkinter as tk
from tkinter import ttk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame

class RationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.main = tk.Frame(self)
        self.main.pack()
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM)

        self.controller = controller

        self.ration_id = None
        self.name = None

        self.house_dropdown = None

        button = tk.Button(
            self.footer, text="Back", font=self.controller.main_font,
            command=lambda: self.controller.show_frame("MainMenuPage")
        )

        button.pack(side=tk.LEFT)

        button = tk.Button(
            self.footer, text="Next", font=self.controller.main_font,
            command=lambda: self.controller.frames["RunPage"].display_page(self.ration_id)
        )

        button.pack(side=tk.LEFT)

    def display_page(self, ration_id):

        self.main.destroy()
        self.main = tk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.main.grid_rowconfigure(2, weight=1)

        self.ration_id = ration_id

        self.name = self.controller.ration_db.get_ration(self.ration_id)[1]
        ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)
        label = tk.Label(
            self.main, text=self.name, font=self.controller.main_font
        )
        label.grid(row=0, column=0)

        houses = self.controller.ration_db.get_all_houses()
        house_names = [house[1] for house in houses]
        self.house_dropdown = ttk.Combobox(self.main, values=house_names, state="readonly", font=self.controller.main_font)
        self.house_dropdown.current(0)
        self.house_dropdown.grid(row=1, column=0)

        ingredients_list = VerticalScrolledFrame(self.main)
        ingredients_list.grid(row=2, column=0)
        for ingredient in ingredients:
            label = tk.Label(
                ingredients_list.interior, text="{}, {}kg".format(ingredient[0], str(ingredient[1])), font=self.controller.main_font
            )
            label.pack()


        self.controller.show_frame("RationPage")