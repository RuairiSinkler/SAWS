#!/usr/bin/python3

from json.decoder import JSONDecodeError
import os
import sys
import time
import glob
import json
import itertools
import configparser
import argparse
import tkinter as tk
import RPi.GPIO as GPIO
import traceback
import tkinter.font as tkfont

from tkinter import ttk

import data.settings as settings
import database.database_management as db
import excel.excel_management as ex
import exceptions as err
import pages as pgs
import pages.message_pages as mpgs

from pages.page_tools.ration import Ration

try:
    from pijuice import PiJuice
except ImportError as e:
    print("PIJUICE UNSUCCESSFULLY IMPORTED")
    traceback.print_exc()


class SAWS(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry("{0}x{1}+0+0".format(self.screen_width, self.screen_height))
        self.resizable(False, False)
        self.overrideredirect(True)
        self.main_font = tkfont.Font(size=25)
        self.text_font = tkfont.Font(size=15)
        self.option_add('*Dialog.msg.font', self.main_font)
        self.option_add("*TCombobox*Listbox*Font", self.main_font)

        ttk.Style().configure( 'Vertical.TScrollbar', width=self.winfo_screenwidth() / 10 )

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill=tk.BOTH, expand=tk.TRUE)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.pijuice = None

        self.frames = {}
        self.warning_frames = []

        self.report_callback_exception = self.display_callback_error


    def setup(self):
        GPIO.setmode(GPIO.BCM)

        pijuice_active = True
        if 'pijuice' in sys.modules:
            try:
                self.pijuice = PiJuice()
            except FileNotFoundError as e:
                print("PIJUICE UNSUCCESSFULLY INITIALISED")
                pijuice_active = False
                traceback.print_exc()
        else:
            pijuice_active = False

        if pijuice_active:
            self.check_pijuice()
        
        self.config = configparser.ConfigParser()
        self.config.read("./data/config.ini")

        option = "usb_location"
        section = "DEFAULT"
        if not self.config.has_option(section, option):
            raise err.ConfigError(section, option)
        usb_dir = self.config[section].get(option)

        option = "temp_log_location"
        if not self.config.has_option(section, option):
            raise err.ConfigError(section, option)
        self.temp_log_location = self.config[section].get(option)

        option = "default_weigher_increment"
        if not self.config.has_option(section, option):
            raise err.ConfigError(section, option)
        self.default_weigher_increment = int(self.config[section].get(option))

        if not os.path.ismount(usb_dir):
            raise err.USBError()
        
        self.ration_db = db.DatabaseManager("./database", "rations.db")
        self.ration_ex = ex.WorksheetManager(usb_dir, "rations")
        self.ration_logs_ex = ex.WorksheetManager(usb_dir, "ration_logs")

        self.ration_ex.update_sheets("rations")
        self.ration_logs_ex.update_sheets("ration_logs")

        self.setup_database()

        for F in (pgs.SplashPage, pgs.PinPage, pgs.MainMenuPage, pgs.RationPage, pgs.RunPage, mpgs.AreYouSurePage, pgs.BatchPage):
            self.create_frame(F, self.container)
            self.hide_frame(F.__name__)
        if "ErrorPage" not in self.frames:
            self.create_frame(mpgs.ErrorPage, self.container)
            self.hide_frame("ErrorPage")
        if "WarningPage" not in self.frames:
            warning_frame = self.create_frame(mpgs.WarningPage, self.container)
            self.hide_frame("WarningPage")
            self.warning_frames.append(warning_frame)

        incomplete_rations = self.check_incomplete_rations()
        for ration, log_warning in incomplete_rations:
            self.display_warning(log_warning)
            self.frames["MainMenuPage"].add_incomplete_ration(ration)

        display_below = None
        if self.frames["WarningPage"].active:
            display_below = self.warning_frames[-1]
        
        self.show_frame("SplashPage", belowThis=display_below)

    def create_frame(self, F, container, name=None, *args):
        page_name = F.__name__
        if name is not None:
            page_name = name
        frame = F(parent=container, controller=self, *args)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        #frame.grid(row=1, column=1, sticky="nsew")
        frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        return frame

    def show_frame(self, page_name, aboveThis=None, belowThis=None):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if belowThis:
            frame.lower(belowThis)
        else:
            frame.lift(aboveThis)

    def hide_frame(self, page_name):
        '''Hide a frame for the given page name'''
        frame = self.frames[page_name]
        frame.lower()

    def check_incomplete_rations(self):
        incomplete_rations = []
        json_logs = glob.glob("{}/*_temp_log.json".format(self.temp_log_location))
        for json_log in json_logs:
            try:
                with open(json_log, "r") as json_file:
                    ration_dict = json.load(json_file)
                    ration = Ration.from_dict(ration_dict)
                    incomplete_rations.append((ration, err.IncompleteLog(ration.name, ration.house)))
            except JSONDecodeError as e:
                self.display_warning(err.BadJSONFile(json_log))
                os.rename(json_log, "{}.bad.json".format(json_log))
        return incomplete_rations

    def setup_database(self):
        self.ration_db.clear()
        self.ration_db.build()

        name_length_max = 20

        weigher_cell = self.ration_ex.find("Weighers")
        if weigher_cell is None:
            raise err.CellError("Weighers")
        top_row = weigher_cell.row
        column = weigher_cell.column
        for row in itertools.count(top_row + 1):
            weigher_id = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if weigher_id is None:
                break
            weigher_id = int(weigher_id)
            weigher_pin = int(self.ration_ex.read_cell(self.ration_ex.get_cell(column + 1, row)))
            increment = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 2, row))
            if increment is None:
                increment = self.default_weigher_increment
            self.ration_db.insert_weigher([weigher_id, weigher_pin, increment])

        ingredient_cell = self.ration_ex.find("Ingredient")
        if ingredient_cell is None:
            raise err.CellError("Ingredient")
        top_row = ingredient_cell.row
        column = ingredient_cell.column
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            augar_pin = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 1, row))
            if augar_pin:
                augar_pin = int(augar_pin)
            weigher_id = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 2, row))
            if weigher_id:
                weigher_id = int(weigher_id)
                db_weigher = self.ration_db.get_weigher(weigher_id)
                if db_weigher is None:
                    raise err.IngredientWeigherError(name, weigher_id)
            ordering = self.ration_ex.read_cell(self.ration_ex.get_cell(column + 3, row))
            if ordering:
                ordering = int(ordering)
            if (
                    (not augar_pin or not weigher_id or not ordering)
                    and
                    (augar_pin or weigher_id or ordering)
                ):
                raise err.IngredientError(name)
            self.ration_db.insert_ingredient([name, augar_pin, weigher_id, ordering])

        ration_cell = self.ration_ex.find("Ration")
        if ration_cell is None:
            raise err.CellError("Ration")
        top_row = ration_cell.row
        column = ration_cell.column
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            if len(name) > name_length_max:
                self.display_warning(err.RationNameTooLong(name, name_length_max))
            else:
                self.ration_db.insert_ration([name])
                for col in itertools.count(column + 1):
                    ration_id = self.ration_db.get_id_by_name("rations", name)
                    ingredient = self.ration_ex.read_cell(self.ration_ex.get_cell(col, top_row))
                    if ingredient is None:
                        break
                    ingredient_id = self.ration_db.get_id_by_name("ingredients", ingredient)
                    amount_cell = self.ration_ex.get_cell(col, row)
                    amount = self.ration_ex.read_cell(amount_cell)
                    if ingredient_id is None:
                        if amount is not None:
                            self.display_warning(err.MissingIngredientWarning(ingredient, name))
                    else:
                        if amount is None:
                            self.display_warning(err.EmptyCellWarning(name))
                            self.ration_ex.write_cell(0, amount_cell)
                            self.ration_ex.save()
                            amount = 0
                        if amount > 0:
                            self.ration_db.insert_ration_ingredients((ration_id, ingredient_id, amount))
                        
                

        house_cell = self.ration_ex.find("Houses")
        if house_cell is None:
            raise err.CellError("Houses")
        top_row = house_cell.row
        column = house_cell.column
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            if len(name) <= name_length_max:
                self.ration_db.insert_house([name])
            else:
                self.display_warning(err.HouseNameTooLong(name, name_length_max))

    def check_pijuice(self):
        status = self.pijuice.status.GetStatus()
        if 'data' in status:
            direct_power = status['data']['powerInput']
            rpi_power = status['data']['powerInput5vIo']
            if direct_power == 'NOT_PRESENT' and rpi_power == 'NOT_PRESENT':
                if 'RunPage' in self.frames:
                    if self.frames['RunPage'].running:
                        self.frames['RunPage'].emergency_stop()
                self.after(10000, self.shutdown)
                raise err.NoPowerError()
            else:
                self.after(1000, self.check_pijuice)
        else:
            self.after(1000, self.check_pijuice)

    def display_error(self, error, saws_error=True):
        traceback.print_exc()
        if "ErrorPage" not in self.frames:
            self.create_frame(mpgs.ErrorPage, self.container)
        self.frames["ErrorPage"].display_page(error, saws_error)

    def display_callback_error(self, exception_class, error, traceback):
        self.display_error(error, isinstance(error, err.SAWSError))

    def display_warning(self, warning):
        if "WarningPage" not in self.frames:
            warning_frame = self.create_frame(mpgs.WarningPage, self.container)
            self.warning_frames.append(warning_frame)
        if self.frames["WarningPage"].active:
            timestamp = time.time_ns()
            page_name = "TempWarningPage.{}".format(timestamp)

            frame = mpgs.WarningPage(parent=self.container, controller=self, name=page_name, temp=True)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            #frame.grid(row=1, column=1, sticky="nsew")
            frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)

            self.frames[page_name].display_page(warning, belowThis=self.warning_frames[-1])
            self.warning_frames.append(frame)
        else:
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
        except err.SAWSError as e:
            saws.display_error(e)
        except Exception as e:
            saws.display_error(e, saws_error=False)
            raise e
        finally:
            saws.mainloop()
    except Exception as e:
        traceback.print_exc()
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
