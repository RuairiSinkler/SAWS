from pages.page_tools.ingredient import Ingredient
import tkinter as tk
import json
from json import JSONEncoder

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
    def from_db_ration(cls, db_ration):
        return cls(*db_ration)
        
    @classmethod
    def from_json(cls, ration_json):
        ration_dict = json.loads(ration_json)
        ingredients = []
        for ingredient_dict in ration_dict["ingredients"]:
            ingredients.append(Ingredient(**ingredient_dict))
        ration_dict["ingredients"] = ingredients
        return cls(**ration_dict)

    def to_json(self):
        return json.dumps(self, indent=2, cls=RationEncoder)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)


class RationEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__