#!/usr/bin/python3


class Error(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class USBError(Error):

    def __init__(self, message="Error reading rations.xlsx\nIs the USB plugged in and the sheet formatted correctly?"):
        self.message = message
        super().__init__(self.message)
