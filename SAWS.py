#!/usr/bin/python3

import os
import itertools
import configparser
import argparse
import tkinter as tk
import RPi.GPIO as GPIO
from tkinter.font import Font
from openpyxl.utils import column_index_from_string

import data.settings as settings
import database.database_management as db
import excel.excel_management as ex
import exceptions as err
import pages as pgs
import pages.message_pages as mpgs


class SAWS(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry("{0}x{1}+0+0".format(self.screen_width, self.screen_height))
        self.resizable(False, False)
        self.overrideredirect(True)
        self.mainFont = Font(size=25)
        self.textFont = Font(size=15)
        self.option_add('*Dialog.msg.font', self.mainFont)
        self.option_add("*TCombobox*Listbox*Font", self.mainFont)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.config = configparser.ConfigParser()
        self.config.read("./data/config.ini")
        usb_dir = self.config["DEFAULT"].get("usb_location")
        self.weigher_increment = int(self.config["DEFAULT"].get("weigher_increment"))
        
        self.ration_db = db.DatabaseManager("./database", "rations.db")
        self.ration_ex = ex.WorksheetManager(usb_dir, "rations")
        self.ration_logs_ex = ex.WorksheetManager(usb_dir, "ration_logs")

        self.frames = {}

        self.create_frame(mpgs.ErrorPage, self.container)
        self.create_frame(mpgs.WarningPage, self.container)

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        database_warning = None

        try:
            self.setup_database()
        except err.SAWSWarning as warning:
            database_warning = warning

        for F in (pgs.SplashPage, pgs.PinPage, pgs.MainMenuPage, pgs.RationPage, pgs.RunPage, mpgs.AreYouSurePage, pgs.BatchPage):
            self.create_frame(F, self.container)

        self.show_frame("SplashPage")

        if database_warning is not None:
            self.display_warning(database_warning)

    def create_frame(self, F, container, *args):
        page_name = F.__name__
        frame = F(parent=container, controller=self, *args)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        #frame.grid(row=1, column=1, sticky="nsew")
        frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.lift()

    def hide_frame(self, page_name):
        '''Hide a frame for the given page name'''
        frame = self.frames[page_name]
        frame.lower()

    def setup_database(self):
        self.ration_db.clear()
        self.ration_db.build()

        rations_with_empty_cells = ""

        ingredient_cell = self.ration_ex.find("Ingredient")
        if ingredient_cell is None:
            raise err.USBError
        top_row = ingredient_cell.row
        column = column_index_from_string(ingredient_cell.column)
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            weigher = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 1, row))
            ordering = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 2, row))
            if name is None:
                break
            self.ration_db.insert_ingredient([name, weigher, ordering])

        ration_cell = self.ration_ex.find("Ration")
        top_row = ration_cell.row
        column = column_index_from_string(ration_cell.column)
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            self.ration_db.insert_ration([name])
            for col in itertools.count(column + 1):
                ration_id = self.ration_db.get_id_by_name("rations", name)
                ingredient = self.ration_ex.read_cell(self.ration_ex.get_cell(col, top_row))
                if ingredient is None:
                    break
                ingredient_id = self.ration_db.get_id_by_name("ingredients", ingredient)
                amount_cell = self.ration_ex.get_cell(col, row)
                amount = self.ration_ex.read_cell(amount_cell)
                if amount is None:
                    rations_with_empty_cells += "{}\n".format(name)
                    self.ration_ex.write_cell(0, amount_cell)
                    self.ration_ex.save()
                    amount = 0
                self.ration_db.insert_ration_ingredients((ration_id, ingredient_id, amount))

        house_cell = self.ration_ex.find("Houses")
        top_row = house_cell.row
        column = column_index_from_string(house_cell.column)
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            self.ration_db.insert_house([name])

        if rations_with_empty_cells:
            raise err.EmptyCellWarning(rations_with_empty_cells)

    def display_error(self, error):
        self.frames["ErrorPage"].display_page(error)

    def display_warning(self, warning):
        self.frames["WarningPage"].display_page(warning)

    def shutdown(self):
        os.system("sudo shutdown -h now")


def main():
    parser = argparse.ArgumentParser(description="Parses arguments for SAWS")
    parser.add_argument("-d", "--devmode", action="store_true",
                        help="Enables Dev Mode")
    args = parser.parse_args()
    
    settings.init()
    settings.dev_mode = args.devmode
    if settings.dev_mode:
        print("DEV_MODE ACTIVE")

    try:
        saws = SAWS()
        try:
            saws.setup()
        except err.USBError as e:
            saws.display_error(e)
        finally:
            saws.mainloop()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        main()
    except:
        raise
