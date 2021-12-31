#!/usr/bin/python3


class SAWSWarning(Warning):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyCellWarning(SAWSWarning):

    def __init__(self, ration):
        self.message = f"Found empty cell(s) in ration '{ration}'. Changing empty cell(s) to 0."
        super().__init__(self.message)


class MissingIngredientWarning(SAWSWarning):

    def __init__(self, ingredient, ration):
        self.message = f"Ingredient '{ingredient}' has been used in ration '{ration}' but it is not listed in the Ingredients list. This ingredient will not appear in the ration. Please check rations.xlsx."
        super().__init__(self.message)


class InvalidRation(SAWSWarning):

    def __init__(self, ration):
        self.message = f"Ration '{ration}' is invalid. It will be unavailable until fixed. Please check rations.xlsx."
        super().__init__(self.message)

class IncompleteLog(SAWSWarning):

    def __init__(self, ration, house):
        self.message = f"The most recent '{ration}' ration run for house '{house}' was ended unexpectedly. It will be available to continue at the main menu. It will disappear (and the data lost!) if a new '{ration}' for '{house}' is run again."
        super().__init__(self.message)

class BadJSONFile(SAWSWarning):

    def __init__(self, json_file):
        self.message = f"The json file '{json_file}' cannot be read. If you were expecting to recover from an incomplete ration contact supplier, otherwise ignore this."
        super().__init__(self.message)

class HouseNameTooLong(SAWSWarning):

    def __init__(self, house, max_length):
        self.message = f"House '{house}' has a name that is too long. It will be unavailable for use. Please reduce to fewer than {max_length} characters."
        super().__init__(self.message)

class RationNameTooLong(SAWSWarning):

    def __init__(self, ration, max_length):
        self.message = f"Ration '{ration}' has a name that is too long. It will be unavailable for use. Please reduce to fewer than {max_length} characters."
        super().__init__(self.message)
