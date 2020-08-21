import tkinter as tk

class Weigher:

    def __init__(self, parent, controller, weigher_id):
        self.parent = parent
        self.controller = controller
        self.weigher_id = weigher_id

        self.ingredients = []

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT, expand=True)

        self.hopper = None

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        self.ingredients.sort(key=lambda ingredient: ingredient.ordering)

        label = tk.Label(
            self.frame, textvariable=ingredient.label, font=self.controller.textFont
        )
        label.grid(column=(len(self.ingredients) * 2) - 1, row=0)

    def get_active_ingredient(self):
        for ingredient in self.ingredients:
            if ingredient.augar.active:
                return ingredient
        for ingredient in self.ingredients:
            if not ingredient.done():
                return ingredient
        return None