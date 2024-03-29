import os
import time
import json
import tkinter as tk
import tkinter.font as tkfont

import pages.page_tools.font_manager as fm
from pages.page_tools.weigher import Weigher
from pages.page_tools.ration import RationEncoder

class RunPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.header.grid(column=0, row=0, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1, uniform="controls")
        self.header.grid_columnconfigure(1, weight=1, uniform="controls")

        self.main = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.main.grid(column=0, row=1, sticky="nsew")

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=0, row=2, sticky="ew")

        self.controller = controller

        self.running = False
        self.max_weigher = 0
        self.ration = None
        self.json_log_file = None

        self.start_pause_text = tk.StringVar()
        self.start_pause_text.set("Start")
        self.start_pause_button = tk.Button(
            self.header, textvariable=self.start_pause_text, font=self.controller.main_font, command=self.start_pause
        )
        self.start_pause_button.grid(column=0, row=0, sticky="ew")

        self.end_text = tk.StringVar()
        self.end_text.set("End Run Early")
        self.quit_button = tk.Button(
            self.header, textvariable=self.end_text, font=self.controller.main_font,
            command=lambda: self.controller.frames["AreYouSurePage"].display_page(self.ration.complete)
        )
        self.quit_button.grid(column=1, row=0, sticky="ew")

    def increment_weight(self, weigher, increment=None):
        ingredient = weigher.get_active_ingredient()
        if ingredient is None:
            ingredient = weigher.ingredients[-1]

        if increment is None:
            increment = weigher.increment

        ingredient.increment_amount(increment)
        percentage = ingredient.percentage()
        weigher.hopper.fill_hopper(percentage)
        next_ingredient = None
        
        if self.running:
            if ingredient.done():
                ingredient.augar.turn_off()
                next_ingredient = weigher.get_active_ingredient()
                if next_ingredient is not None:
                    next_ingredient.augar.turn_on()
            else:
                ingredient.augar.turn_on()

        if ingredient.done():
            next_ingredient = weigher.get_active_ingredient()
            if next_ingredient is not None:
                weigher.hopper.draw_hopper()
        
        self.ration.complete = self.check_done()

    def ingredient_done(self, ingredient):
        if ingredient.current_amount == 0:
            ingredient.current_amount = ingredient.desired_amount
        else:
            ingredient.current_amount = 0
        ingredient.update_label()
        self.ration.complete = self.check_done()

    def check_done(self):
        done = True
        for ingredient in self.ration.ingredients:
            if not ingredient.done():
                done = False
        if done:
            self.end_text.set("Complete")
            self.header.grid_columnconfigure(1, weight=1, uniform="controls")
            self.quit_button.grid()
        else:
            self.end_text.set("End Run Early")

        self.update_log()
        
        return done

    def start_pause(self):
        if self.running:
            self.running = False
            self.start_pause_text.set("Start")
            for _, weigher in self.weighers.items():
                for ingredient in weigher.ingredients:
                    ingredient.augar.turn_off()
            self.header.grid_columnconfigure(1, weight=1, uniform="controls")
            self.quit_button.grid()
        else:
            self.running = True
            self.start_pause_text.set("Pause")
            for _, weigher in self.weighers.items():
                self.increment_weight(weigher, 0)
            if not self.ration.complete:
                self.quit_button.grid_remove()
                self.header.grid_columnconfigure(1, weight=0, uniform="")

    def emergency_stop(self):
        self.start_pause_button.configure(state=tk.DISABLED)
        self.quit_button.configure(state=tk.DISABLED)
        if self.unweighed_ingredients is not None:
            for _, button in self.unweighed_ingredients:
                button.configure(state=tk.DISABLED)

        for _, weigher in self.weighers.items():
            for ingredient in weigher.ingredients:
                ingredient.augar.turn_off()
        if self.ration is not None and os.path.exists(f"{self.controller.temp_log_location}/{self.json_log_file}"):
            self.update_log()

    def create_log(self):
        self.ration.start_time = time.strftime("%T %d/%m/%y")
        if not os.path.exists(self.controller.temp_log_location):
            os.makedirs(self.controller.temp_log_location)
        self.update_log()

    def update_log(self):
        with open(f"{self.controller.temp_log_location}/{self.json_log_file}", "w") as json_file:
            json.dump(self.ration, json_file, cls=RationEncoder)

    def log_run(self, num_pad):
        sheet = None
        if self.ration.house in self.controller.ration_logs_ex.workbook.sheetnames:
            sheet = self.controller.ration_logs_ex.get_sheet(self.ration.house)
        else:
            self.controller.ration_logs_ex.create_sheet(self.ration.house)
            sheet = self.controller.ration_logs_ex.get_sheet(self.ration.house)
            self.controller.ration_logs_ex.change_sheet(sheet)
            self.controller.ration_logs_ex.setup_sheet(self.ration.house)
            sheet = self.controller.ration_logs_ex.get_sheet(self.ration.house)
        self.controller.ration_logs_ex.change_sheet(sheet)

        self.ration.batch_number = num_pad.entry.get()

        self.ration.end_time = time.strftime("%T %d/%m/%y")

        self.controller.ration_logs_ex.log_run(self.ration)
        self.controller.ration_logs_ex.save()

        if os.path.exists(f"{self.controller.temp_log_location}/{self.json_log_file}"):
            os.remove(f"{self.controller.temp_log_location}/{self.json_log_file}")

        for _, weigher in self.weighers.items():
            weigher.active = False
        self.weighers = {}

        self.controller.show_frame("MainMenuPage")
        num_pad.clear()

    def display_page(self, ration):
        self.main.destroy()
        self.footer.destroy()

        self.main = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.main.grid(column=0, row=1, sticky="nsew")
        self.main.grid_rowconfigure(1, weight=1)

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=0, row=2, sticky="ew")

        self.running = False
        self.start_pause_text.set("Start")
        self.ration = ration
        self.json_log_file = f"{self.ration.name}_{self.ration.house}_temp_log.json".replace(" ", "_")

        self.create_log()

        self.weighers = {}

        self.unweighed_ingredients = []
        unweighed_button_font = tkfont.Font(size=self.controller.text_font['size'])

        for ingredient in self.ration.ingredients:
            if ingredient.weigher_id is None:
                button_column = len(self.unweighed_ingredients)
                button = tk.Button(
                    self.footer, textvariable=ingredient.label, font=unweighed_button_font,
                    command=lambda ingredient=ingredient: self.ingredient_done(ingredient)
                )
                if ingredient.done():
                    button.configure(state=tk.DISABLED)
                button.grid(row=0, column=button_column, sticky="ew")
                self.footer.grid_columnconfigure(button_column, weight=1, uniform="unweighed_ingredients_buttons")
                self.unweighed_ingredients.append((ingredient, button))
            else:
                if ingredient.weigher_id not in self.weighers:
                    db_weigher = self.controller.ration_db.get_weigher(ingredient.weigher_id)
                    self.weighers[ingredient.weigher_id] = Weigher.fromDbWeigher(self, self.main, self.controller, db_weigher)
                weigher = self.weighers[ingredient.weigher_id]
                weigher.add_ingredient(ingredient)


        self.main.update_idletasks()

        for _, weigher in self.weighers.items():
            weigher.resize_labels()
            weigher.add_hopper()
            for ingredient in weigher.ingredients:
                increment = ingredient.current_amount 
                ingredient.current_amount = 0
                self.increment_weight(weigher, increment)

        for ingredient, button in self.unweighed_ingredients:
            button.update_idletasks()
            text = ingredient.get_full_label_text()
            fm.resize_font_width(text, unweighed_button_font, button.winfo_width())

        self.ration.complete = self.check_done()
        self.controller.show_frame("RunPage")