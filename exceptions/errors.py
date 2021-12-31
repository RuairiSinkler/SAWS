#!/usr/bin/python3


class SAWSError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ConfigError(SAWSError):

    def __init__(self, section, option):
        self.message = f"There is something wrong with the config.ini file. Expected option '{option}' under the '{section}' section."
        super().__init__(self.message)


class USBError(SAWSError):

    def __init__(self, message="Couldn't read rations.xlsx. Is the USB plugged in and rations.xlsx formatted correctly?"):
        self.message = message
        super().__init__(self.message)


class CellError(SAWSError):

    def __init__(self, cell_value):
        self.message = f"Couldn't find the '{cell_value}' cell when reading rations.xlsx."
        super().__init__(self.message)


class IngredientError(SAWSError):

    def __init__(self, ingredient_name):
        self.message = f"Error reading ingredient '{ingredient_name}'. It is missing a value for one of it's fields, please resolve this in rations.xlsx."
        super().__init__(self.message)


class IngredientWeigherError(SAWSError):

    def __init__(self, ingredient_name, weigher_id):
        self.message = f"Error reading ingredient '{ingredient_name}'. It refers to a weigher with id '{weigher_id}', but this is not present in the Weighers table, please resolve this in rations.xlsx."
        super().__init__(self.message)

class NoPowerError(SAWSError):

    def __init__(self, message="Mains power to the system has been lost, tidying up and shutting down."):
        self.message = message
        super().__init__(self.message)
