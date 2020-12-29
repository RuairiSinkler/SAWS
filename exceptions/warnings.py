#!/usr/bin/python3


class SAWSWarning(Warning):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyCellWarning(SAWSWarning):

    def __init__(self, ration):
        self.message = "Found empty cell(s) in ration '{}'. Changing empty cell(s) to 0.".format(ration)
        super().__init__(self.message)


class MissingIngredientWarning(SAWSWarning):

    def __init__(self, ingredient, ration):
        self.message = "Ingredient '{}' has been used in ration '{}' but it is not listed in the Ingredients list. This ingredient will not appear in the ration. Please check rations.xlsx.".format(ingredient, ration)
        super().__init__(self.message)


class InvalidRation(SAWSWarning):

    def __init__(self, ration):
        self.message = "Ration '{}' is invalid. It will be unavailable until fixed. Please check rations.xlsx.".format(ration)
        super().__init__(self.message)

class IncompleteLog(SAWSWarning):

    def __init__(self, house):
        self.message = "The most recent mix for house '{}' was ended unexpectedly. It will be available to continue at the main menu. It will disappear if another ration is run for house '{}'.".format(house, house)
        super().__init__(self.message)
