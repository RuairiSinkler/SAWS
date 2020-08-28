#!/usr/bin/python3


class SAWSError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ConfigError(SAWSError):

    def __init__(self, section, option):
        self.message = "There is something wrong with the config.ini file\n Expected option '{}' under the '{}' section".format(option, section)
        super().__init__(self.message)


class USBError(SAWSError):

    def __init__(self, message="Couldn't read rations.xlsx\nIs the USB plugged in and\nthe sheet formatted correctly?"):
        self.message = message
        super().__init__(self.message)


class CellError(SAWSError):

    def __init__(self, cell_value):
        self.message = "Couldn't find the '{}' cell when reading rations.xlsx".format(cell_value)
        super().__init__(self.message)


class IngredientError(SAWSError):

    def __init__(self, ingredient_name):
        self.message = "Error reading ingredient '{}'\nIt is missing a value for one of it's fields\nPlease resolve this in rations.xlsx".format(ingredient_name)
        super().__init__(self.message)


class IngredientWeigherError(SAWSError):

    def __init__(self, ingredient_name, weigher_id):
        self.message = "Error reading ingredient '{}'\nIt refers to a weigher with id '{}', but this is not present in the Weighers table\nPlease resolve this in rations.xlsx".format(ingredient_name, weigher_id)
        super().__init__(self.message)
