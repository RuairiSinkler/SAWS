import tkinter as tk

class Ingredient:

    def __init__(self, name, desired_amount, augar_pin, weigher_id, ordering, augar=None, current_amount=0):
        self.name = name
        self.desired_amount = desired_amount
        self.augar_pin = augar_pin
        self.weigher_id = weigher_id
        self.ordering = ordering
        self.augar = augar
        self.current_amount = current_amount

        self.label = tk.StringVar()
        self.label.set("{}\n{}/{}kg".format(self.name, str(self.current_amount), str(self.desired_amount)))

    @classmethod
    def copy(cls, ingredient):
        ingredient_dict = dict(ingredient.__dict__)
        del ingredient_dict["label"]
        del ingredient_dict["augar"]
        return cls(**ingredient_dict)

    @classmethod
    def from_db_ingredient(cls, db_ingredient, augar=None):
        return cls(*db_ingredient, augar)

    def increment_amount(self, increment):
        self.current_amount += increment
        self.label.set("{}\n{}/{}kg".format(self.name, str(self.current_amount), str(self.desired_amount)))

    def percentage(self):
        if self.desired_amount == 0:
            return 100
        else:
            return (self.current_amount / self.desired_amount) * 100

    def done(self):
        return self.current_amount >= self.desired_amount