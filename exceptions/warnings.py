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

    def __init__(self, ration, house):
        self.message = "The most recent '{}' ration run for house '{}' was ended unexpectedly. It will be available to continue at the main menu. It will disappear (and the data lost!) if a new '{}' for '{}' is run again.".format(ration, house, ration, house)
        super().__init__(self.message)

class BadJSONFile(SAWSWarning):

    def __init__(self, json_file):
        self.message = "The json file '{}' cannot be read. If you were expecting to recover from an incomplete ration contact supplier, otherwise ignore this.".format(json_file)
        super().__init__(self.message)

class HouseNameTooLong(SAWSWarning):

    def __init__(self, house, max_length):
        self.message = "House '{}' has a name that is too long. It will be unavailable for use. Please reduce to fewer than {} characters.".format(house, max_length)
        super().__init__(self.message)

class RationNameTooLong(SAWSWarning):

    def __init__(self, ration, max_length):
        self.message = "Ration '{}' has a name that is too long. It will be unavailable for use. Please reduce to fewer than {} characters.".format(ration, max_length)
        super().__init__(self.message)
