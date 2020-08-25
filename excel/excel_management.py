import os
import openpyxl
import itertools
import numpy as np
from pathlib import Path

RATIONS_SHEET_VERSION = 2.0
RATION_LOGS_SHEET_VERSION = 1.0

class WorksheetManager:
    def __init__(self, directory, name):
        dir = directory
        self.path = "{}/{}.xlsx".format(dir, name)
        workbook = Path(self.path)
        if workbook.is_file():
            self.workbook = openpyxl.load_workbook(self.path)
        else:
            self.workbook = openpyxl.Workbook()
            self.sheet = self.workbook.active
            self.save()
        self.sheet = self.workbook.active

    # Saves any work done
    def save(self):
        self.workbook.save(self.path)

    def create_sheet(self, title):
        self.workbook.create_sheet(title)
        self.save()

    # Returns a list of the sheets in the workbook
    def get_sheets(self):
        return self.workbook.get_sheet_names()

    # Returns a sheet object given its name
    def get_sheet(self, name):
        return self.workbook[name]

    # Changes the self.sheet value to the given sheet
    def change_sheet(self, sheet):
        self.sheet = sheet

    # Renames the current sheet to the given value
    def rename_sheet(self, title):
        self.sheet.title = title

    # Returns a cell variable given its column and row as numbers
    def get_cell(self, column, row):
        cell_name = "{}{}".format(openpyxl.utils.get_column_letter(column), str(row))
        return self.sheet[cell_name]

    # Returns the value in a given cell object
    def read_cell(self, cell):
        return cell.value

    # Writes the given value into the given cell object
    def write_cell(self, value, cell):
        cell.value = value

    # Setups sheet i.e. creates layout of file
    def setup_sheet(self, title, headings):
        self.sheet.title = title
        self.write_cell(title, self.sheet["B2"])
        for i, heading in enumerate(headings):
            self.write_cell(heading, self.get_cell(i+2, 4))
            self.write_cell("-", self.get_cell(i+2, 3))
        self.save()

    # Finds a value in the worksheet and returns its cell
    def find(self, search_string):
        for row in self.sheet.rows:
            for cell in row:
                if self.read_cell(cell) == search_string:
                    return cell
        return None

    def log_run(self, time_run, ration, complete, ingredients, batch_number):
        row = self.sheet.max_row + 1
        column = self.find("Date Run").column
        self.write_cell(time_run, self.get_cell(column, row))
        self.write_cell(ration, self.get_cell(column + 1, row))
        if complete:
            complete = "Yes"
        else:
            complete = "No"
        self.write_cell(complete, self.get_cell(column + 2, row))
        total = 0
        for ingredient in ingredients:
            column = self.find(ingredient.name).column
            self.write_cell(ingredient.current_amount, self.get_cell(column, row))
            total += ingredient.current_amount
        column = self.find("Total").column
        self.write_cell(total, self.get_cell(column, row))
        column = self.find("Batch Number").column
        self.write_cell(batch_number, self.get_cell(column, row))

    def update_sheets(self, sheet_type):
        for sheet_name in self.get_sheets():
            sheet = self.get_sheet(sheet_name)
            self.change_sheet(sheet)

            sheet_version = 0
            version_cell = self.find("VERSION")
            if version_cell is not None:
                sheet_version = float(self.read_cell(self.get_cell(version_cell.column + 1, version_cell.row)))
            
            if sheet_type == "rations" and sheet_version < RATIONS_SHEET_VERSION:
                if sheet_version < 1.0:
                    sheet_version = 1.0
                    version_cell = self._create_version_cell(sheet_version)
                    self.save()
                if sheet_version < 2.0:
                    self._move_table(self.find("Ingredient"), 192, 3000)
                    # sheet_version = 2.0
                    # self._update_version_cell(sheet_version, version_cell)
                    self.save()
                    

            elif sheet_type == "ration_logs" and sheet_version < RATION_LOGS_SHEET_VERSION:
                pass
    
    def _create_version_cell(self, version):
        version_cell = None
        for row in self.sheet.rows:
            for cell in row:
                cell_value = self.read_cell(cell)
                if cell_value is None and cell_value == '':
                    if version_cell is not None:
                        self.write_cell("VERSION", version_cell)
                        self.write_cell(str(version), cell)
                        return version_cell
                    else:
                        version_cell = cell
                else:
                    version_cell = None

    def _update_version_cell(self, version, version_cell):
        self.write_cell(version, self.get_cell(version_cell.column + 1, version_cell.row))

    def _move_table(self, origin_cell, column_shift=0, row_shift=0):
        origin_cell = self._get_upper_left_most_cell(origin_cell)
        table_cells, column_bounds, row_bounds = self._get_table_cells(origin_cell)
        column_order = 1
        row_order = 1
        if column_shift > 0:
            column_order = -1
            for row in range(row_bounds[0] - 1, row_bounds[1] + 2):
                for shift in range(1, column_shift + 1):
                    cell = self.get_cell(column_bounds[1] + shift, row)
                    cell_value = self.read_cell(cell)
                    if cell_value is not None and cell_value != '':
                        self._move_table(cell, column_shift, row_shift) 
        elif column_shift < 0:
            for row in range(row_bounds[0] - 1, row_bounds[1] + 2):
                for shift in range(1, abs(column_shift) + 1):
                    cell = self.get_cell(origin_cell.column - shift, row)
                    cell_value = self.read_cell(cell)
                    if cell_value is not None and cell_value != '':
                        self._move_table(cell, column_shift, row_shift)
        if row_shift > 0:
            row_order = -1
            for column in range(column_bounds[0] - 1, column_bounds[1] + 2):
                for shift in range(1, row_shift + 1):
                    cell = self.get_cell(column, row_bounds[1] + shift)
                    cell_value = self.read_cell(cell)
                    if cell_value is not None and cell_value != '':
                        self._move_table(cell, column_shift, row_shift)
        elif row_shift < 0:
            for column in range(column_bounds[0] - 1, column_bounds[1] + 2):
                for shift in range(1, abs(row_shift) + 1):
                    cell = self.get_cell(column, row_bounds[1] - shift)
                    cell_value = self.read_cell(cell)
                    if cell_value is not None and cell_value != '':
                        self._move_table(cell, column_shift, row_shift)

        self.sheet.move_range("{}:{}".format(table_cells[0, 0].coordinate, table_cells[-1, -1].coordinate), rows=row_shift, cols=column_shift)

        # table_cells_view = table_cells[::row_order,::column_order]
        # for i, row in enumerate(table_cells_view):
        #     for j, cell in enumerate(row):
        #         new_cell = self.get_cell(cell.column + column_shift, cell.row + row_shift)
        #         self.write_cell(cell.value, new_cell)
        #         self.write_cell("", cell)
        #         cell = new_cell
        #         table_cells_view[i, j] = cell
        self.save()

    def _get_upper_left_most_cell(self, cell):
        if cell.row > 1:
            cell_check = self.get_cell(cell.column, cell.row - 1)
            cell_value = self.read_cell(cell_check)
            while cell_value is not None and cell_value != '':
                cell = cell_check
                cell_check = self.get_cell(cell.column, cell.row - 1)
                cell_value = self.read_cell(cell_check)
        if cell.column > 1:
            cell_check = self.get_cell(cell.column - 1, cell.row)
            cell_value = self.read_cell(cell_check)
            if cell_value is not None:
                while cell_value is not None and cell_value != '':
                    cell = cell_check
                    cell_check = self.get_cell(cell.column - 1, cell.row)
                    cell_value = self.read_cell(cell_check)
                cell = self._get_upper_left_most_cell(cell)
        return cell

    def _get_table_cells(self, origin_cell):
        origin_column = origin_cell.column
        origin_row = origin_cell.row
        column_bounds = [origin_column, origin_column]
        row_bounds = [origin_row, origin_row]

        row = row_bounds[0]
        cell_value = self.read_cell(self.get_cell(origin_column, row))
        while cell_value is not None and cell_value != '':
            row_bounds[1] = max(row, row_bounds[1])
            column = column_bounds[0]
            cell_value = self.read_cell(self.get_cell(column, row))
            while cell_value is not None and cell_value != '':
                column_bounds[1] = max(column, column_bounds[1])
                column += 1
                cell_value = self.read_cell(self.get_cell(column, row))
            row += 1
            cell_value = self.read_cell(self.get_cell(origin_column, row))

        cells = []
        for row in range(row_bounds[0], row_bounds[1] + 1):
            row_cells = []
            for column in range(column_bounds[0], column_bounds[1] + 1):
                row_cells.append(self.get_cell(column, row))
            cells.append(row_cells)
        return np.array(cells), column_bounds, row_bounds


