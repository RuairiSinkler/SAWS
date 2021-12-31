import tkinter as tk

class Ingredient:

    def __init__(self, name, desired_amount, augar_pin, weigher_id, ordering, augar=None, current_amount=0, label=None):
        self.name = name
        self.desired_amount = desired_amount
        self.augar_pin = augar_pin
        self.weigher_id = weigher_id
        self.ordering = ordering
        self.augar = augar
        self.current_amount = current_amount
        self.increment = 0

        self.label = tk.StringVar()
        self.update_label()

    @classmethod
    def copy(cls, ingredient):
        ingredient_copy = cls(**ingredient.__dict__)
        return ingredient_copy

    @classmethod
    def from_db_ingredient(cls, db_ingredient, augar=None):
        return cls(*db_ingredient, augar)

    def update_label(self):
        self.label.set(self.get_label_text())

    def get_label_text(self):
        return f"{self.name}\n{self.current_amount:.2f}/{self.desired_amount:.2f}kg"

    def get_full_label_text(self):
        return f"{self.name}\n{self.desired_amount:.2f}/{self.desired_amount:.2f}kg"

    def increment_amount(self, increment):
        self.increment = increment
        self.current_amount += increment
        self.update_label()

    def percentage(self):
        if self.desired_amount == 0:
            return 100
        else:
            return (self.current_amount / self.desired_amount) * 100

    def done(self):
        return self.current_amount + (self.increment / 2) >= self.desired_amount