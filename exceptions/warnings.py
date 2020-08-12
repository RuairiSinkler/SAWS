#!/usr/bin/python3


class SAWSWarning(Warning):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyCellWarning(SAWSWarning):

    def __init__(self, ration):
        self.message = "Found empty cell(s) in the following ration:\n{}\nChanging empty cell(s) to 0".format(ration)
        super().__init__(self.message)


class MissingIngredientWarning(SAWSWarning):

    def __init__(self, ingredient, ration):
        self.message = "Ingredient {} has been used in ration {}\nbut it is not listed in the Ingredients list\nRation {} will be unavailable\nPlease check rations.xlsx".format(ingredient, ration)
        super().__init__(self.message)


class InvalidRation(SAWSWarning):

    def __init__(self, ration):
        self.message = "Ration {} is invalid\nIt will be unavailable until fixed\nPlease check rations.xlsx".format(ration)
        super().__init__(self.message)
