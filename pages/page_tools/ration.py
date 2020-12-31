import tkinter as tk

class Ration:

    def __init__(self, id, name, house=None, start_time=None, end_time=None, complete=False, batch_number=None, ingredients=[]):
        self.id = id
        self.name = name
        self.house = house
        self.start_time = start_time
        self.end_time = end_time
        self.complete = complete
        self.batch_number = batch_number
        self.ingredients = ingredients

    @classmethod
    def fromDbRation(cls, db_ration):
        return cls(*db_ration)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)