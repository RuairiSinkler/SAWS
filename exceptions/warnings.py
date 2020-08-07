#!/usr/bin/python3


class SAWSWarning(Warning):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyCellWarning(SAWSWarning):

    def __init__(self, ration_names):
        self.message = "Found an empty cell(s) in the following rations:\n{}Assuming empty cell(s) as 0".format(ration_names)
        super().__init__(self.message)
