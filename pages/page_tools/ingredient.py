import tkinter as tk

class Ingredient:

    def __init__(self, name, desired_amount, ordering, augar=None):
        self.name = name
        self.desired_amount = desired_amount
        self.ordering = ordering
        self.augar = augar

        self.current_amount = 0
        self.label = tk.StringVar()
        self.label.set("{}\n{}\n/{}kg".format(name, str(self.current_amount), str(desired_amount)))

    def increment_amount(self, increment):
        self.current_amount += increment
        self.label.set("{}\n{}\n/{}kg".format(self.name, str(self.current_amount), str(self.desired_amount)))

    def percentage(self):
        if self.desired_amount == 0:
            return 100
        else:
            return (self.current_amount // self.desired_amount) * 100

    def done(self):
        return self.current_amount >= self.desired_amount