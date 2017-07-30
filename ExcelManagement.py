import openpyxl
from pathlib import Path


class WorksheetManager:
    def __init__(self, name):
        self.name = name
        workbook = Path(name)
        if workbook.is_file():
            self.workbook = openpyxl.load_workbook(name)
        else:
            self.workbook = openpyxl.Workbook()
            self.workbook.save(name)
        self.sheet = self.workbook.active

    # Returns a list of the sheets in the workbook
    def get_sheets(self):
        return self.workbook.get_sheet_names()

    # Returns a sheet object given its name
    def get_sheet(self, name):
        return self.workbook.get_sheet_by_name(name)

    # Changes the self.sheet value to the given sheet
    def change_sheet(self, sheet):
        self.sheet = sheet

    # Renames the current sheet to the given value
    def rename_sheet(self, title):
        self.sheet.title = title

    # Returns a cell variable given its name e.g. 'A1'
    def get_cell(self, cell_name):
        return self.sheet[cell_name]

    # Returns the value in a given cell object
    def read_cell(self, cell):
        return cell.value

    # Writes the given value into the given cell object
    def write_cell(self, value, cell):
        cell = value
