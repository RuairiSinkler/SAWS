#!/usr/bin/python3


class Warning(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyCellWarning(Warning):

    def __init__(self, ration_names):
        self.message = "Found an empty cell(s) in the following rations:\n{}\nAssuming empty cell(s) as 0".format(ration_names)
        super().__init__(self.message)
