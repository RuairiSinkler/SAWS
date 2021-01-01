import tkinter as tk
from tkinter import ttk
from pages.page_tools.vertical_scrolled_frame import VerticalScrolledFrame
from pages.page_tools.ingredient import Ingredient

class RationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.main = tk.Frame(self)
        self.main.pack()
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM)

        self.controller = controller

        self.ration = None
        self.button_to_remove = None

        self.house_dropdown = None

        button = tk.Button(
            self.footer, text="Back", font=self.controller.main_font,
            command=lambda: self.controller.show_frame("MainMenuPage")
        )

        button.pack(side=tk.LEFT)

        button = tk.Button(
            self.footer, text="Next", font=self.controller.main_font,
            command=self.button_callback
        )

        button.pack(side=tk.LEFT)

    def button_callback(self):
        if self.ration.house is None:
            self.ration.house = self.house_dropdown.get()
        if self.button_to_remove is not None:
            self.controller.frames["MainMenuPage"].remove_button(self.button_to_remove)
        self.controller.frames["RunPage"].display_page(self.ration)

    def display_page(self, ration, button_to_remove=None):

        self.main.destroy()
        self.main = tk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.ration = ration
        self.button_to_remove = button_to_remove

        db_ingredients = self.controller.ration_db.get_ration_ingredients(self.ration.id)
        ration_ingredients = self.ration.ingredients
        ration.ingredients = []
        for db_ingredient in db_ingredients:
            ingredient = Ingredient.fromDbIngredient(db_ingredient)
            for ration_ingredient in ration_ingredients:
                if ingredient.name == ration_ingredient.name:
                    ingredient.increment_amount(ration_ingredient.current_amount)

            self.ration.add_ingredient(ingredient)

        label = tk.Label(
            self.main, text=self.ration.name, font=self.controller.main_font
        )
        label.pack()

        ingredients_list = VerticalScrolledFrame(self.main)
        ingredients_list.pack(fill=tk.BOTH, expand=tk.TRUE)
        for ingredient in self.ration.ingredients:
            label = tk.Label(
                ingredients_list.interior, text="{}, {}/{}kg".format(ingredient.name, str(ingredient.current_amount), str(ingredient.desired_amount)), font=self.controller.main_font
            )
            label.pack()

        if self.ration.house is None:
            houses = self.controller.ration_db.get_all_houses()
            house_names = [house[1] for house in houses]
            self.house_dropdown = ttk.Combobox(self.main, values=house_names, state="readonly", font=self.controller.main_font, height=6)
            self.house_dropdown.current(0)
            self.house_dropdown.pack()
        else:
            label = tk.Label(
                self.main, text="House: {}".format(self.ration.house), font=self.controller.main_font
            )
            label.pack()


        self.controller.show_frame("RationPage")