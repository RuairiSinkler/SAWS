import openpyxl
from pathlib import Path


class WorksheetManager:
    def __init__(self, directory, name):
        self.name = name
        workbook = Path("{}/{}.xlsx".format(directory, name))
        if workbook.is_file():
            self.workbook = openpyxl.load_workbook(name)
        else:
            self.workbook = openpyxl.Workbook()
            self.sheet = self.workbook.active
            self.setup_sheet()
            self.workbook.save(name)
        self.sheet = self.workbook.active

    # Saves any work done
    def save(self):
        self.workbook.save()

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

    # Returns a cell variable given its column and row
    def get_cell(self, column, row):
        cell_name = "{}{}".format(column, row)
        return self.sheet[cell_name]

    # Returns the value in a given cell object
    def read_cell(self, cell):
        return cell.value

    # Writes the given value into the given cell object
    def write_cell(self, value, cell):
        cell = value

    # Setups sheet i.e. creates layout of file
    def setup_sheet(self):
        column_titles = ["Time, Date", "Ration", "Wheat", "Barley", "Soya", "Limestone",
                         "Soya Oil", "Arbocell", "Methionine", "Premix"]
        for i in range(10):
            self.write_cell(column_titles[i], self.get_cell(i+2, 2))
            self.write_cell("-", self.get_cell(i+2, 3))

    # Fills a row appropriately with a runs information
    def fill_row(self, ration_name, end_weights, weight_limits, now):
        row = self.sheet.max_row + 1
        self.write_cell(now, self.get_cell("B", str(row)))
        self.write_cell(ration_name, self.get_cell("C", str(row)))
        for i in range(8):
            string = "{}/{}".format(end_weights[i], weight_limits[i])
            self.write_cell(string, self.get_cell(str(openpyxl.cell.get_column_letter(i+4)), str(row)))
        self.save()