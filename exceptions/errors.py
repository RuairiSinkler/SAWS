#!/usr/bin/python3


class SAWSError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class USBError(SAWSError):

    def __init__(self, message="Error reading rations.xlsx\nIs the USB plugged in and\nthe sheet formatted correctly?"):
        self.message = message
        super().__init__(self.message)