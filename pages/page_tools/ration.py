from pages.page_tools.ingredient import Ingredient
from json import JSONEncoder

class Ration:

    def __init__(self, id, name, house=None, start_time=None, end_time=None, complete=False, batch_number=None, ingredients=None):
        self.id = id
        self.name = name
        self.house = house
        self.start_time = start_time
        self.end_time = end_time
        self.complete = complete
        self.batch_number = batch_number
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients

    @classmethod
    def copy(cls, ration):
        ration_dict = dict(ration.__dict__)
        ingredients = []
        if "ingredients" in ration_dict:
            for ingredient in ration_dict["ingredients"]:
                ingredient_copy = Ingredient.copy(ingredient)
                ingredients.append(ingredient_copy)
        ration_dict["ingredients"] = ingredients
        return cls(**ration_dict)

    @classmethod
    def from_db_ration(cls, db_ration):
        return cls(*db_ration)
        
    @classmethod
    def from_dict(cls, ration_dict):
        ingredients = []
        if "ingredients" in ration_dict:
            for ingredient_dict in ration_dict["ingredients"]:
                ingredients.append(Ingredient(**ingredient_dict))
        ration_dict["ingredients"] = ingredients
        return cls(**ration_dict)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)


class RationEncoder(JSONEncoder):

    def default(self, o):
        ration_dict = dict(o.__dict__)
        ingredients = []
        for ingredient in ration_dict["ingredients"]:
            ingredient_copy = Ingredient.copy(ingredient)
            ingredients.append(ingredient_copy.__dict__)
        ration_dict["ingredients"] = ingredients

        return ration_dict