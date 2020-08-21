import time
import tkinter as tk
import numpy as np
from tkinter import ttk
from operator import itemgetter

import data.settings as settings
from pages.page_tools.ingredient import Ingredient
from pages.page_tools.weigher import Weigher
from pages.page_tools.augar import Augar
from pages.page_tools.weight_input import WeightInput
from pages.page_tools.hopper import Hopper

class RunPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.main = tk.Frame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.main.grid(column=2, row=2, rowspan=4, sticky="nsew")
        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=2, row=6, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)

        self.controller = controller

        self.running = False
        self.max_weigher = 0
        self.done = False
        self.ration_id = None

        self.start_pause_text = tk.StringVar()
        self.start_pause_text.set("Start")
        button = tk.Button(
            self, textvariable=self.start_pause_text, font=self.controller.mainFont, command=self.start_pause
        )
        button.grid(column=1, row=3)

        houses = self.controller.ration_db.get_all_houses()
        house_names = [house[1] for house in houses]
        self.house_dropdown = ttk.Combobox(self, values=house_names, state="readonly", font=self.controller.mainFont)
        self.house_dropdown.current(0)
        self.house_dropdown.grid(column=2, row=1)

        self.end_text = tk.StringVar()
        self.end_text.set("End\nRun\nEarly")
        self.quit_button = tk.Button(
            self, textvariable=self.end_text, font=self.controller.mainFont,
            command=lambda: self.controller.frames["AreYouSurePage"].display_page(self.done)
        )
        self.quit_button.grid(column=4, row=3)

    def increment_weight(self, weigher, increment=None):
        ingredient = weigher.get_active_ingredient()
        if ingredient is None:
            ingredient = weigher.ingredients[-1]

        if increment is None:
            increment = self.controller.weigher_increment

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
        if next_ingredient is not None:
            weigher.hopper.draw_hopper()
        self.check_done()

    def ingredient_done(self, ingredient):
        if ingredient.current_amount == 0:
            ingredient.current_amount = ingredient.desired_amount
        else:
            ingredient.current_amount = 0
        ingredient.label.set("{}\n{}\n/{}kg".format(ingredient.name, str(ingredient.current_amount), str(ingredient.desired_amount)))
        self.check_done()

    def check_done(self):
        self.done = True
        for ingredient in self.ingredients:
            if not ingredient.done():
                self.done = False
        if self.done:
            self.end_text.set("Complete")
            self.quit_button.grid()
        else:
            self.end_text.set("End\nRun\nEarly")

    def start_pause(self):
        if self.running:
            self.running = False
            self.start_pause_text.set("Start")
            for _, weigher in self.weighers.items():
                for ingredient in weigher.ingredients:
                    ingredient.augar.turn_off()
            self.quit_button.grid()
        else:
            self.running = True
            self.start_pause_text.set("Pause")
            for _, weigher in self.weighers.items():
                self.increment_weight(weigher, 0)
            if not self.done:
                self.quit_button.grid_remove()

    def log_run(self, num_pad):
        batch_number = num_pad.entry.get()
        house = self.house_dropdown.get()
        if house in self.controller.ration_logs_ex.workbook.sheetnames:
            sheet = self.controller.ration_logs_ex.get_sheet(house)
        else:
            self.controller.ration_logs_ex.create_sheet(house)
            sheet = self.controller.ration_logs_ex.get_sheet(house)
            self.controller.ration_logs_ex.change_sheet(sheet)
            headings = ["Date Run", "Ration", "Complete"] + [ingredient.name for ingredient in self.ingredients] + ["Total", "Batch Number"]
            self.controller.ration_logs_ex.setup_sheet(house, headings)
            sheet = self.controller.ration_logs_ex.get_sheet(house)
        self.controller.ration_logs_ex.change_sheet(sheet)
        time_run = time.strftime("%d/%m/%y")
        ration = self.controller.ration_db.get_ration(self.ration_id)[1]
        self.controller.ration_logs_ex.log_run(time_run, ration, self.done, self.ingredients, batch_number)
        self.controller.ration_logs_ex.save()

        self.controller.show_frame("MainMenuPage")
        num_pad.clear()

    def display_page(self, ration_id):
        self.main.destroy()
        self.footer.destroy()
        self.main = tk.Frame(self)
        self.main.grid(column=2, row=2, rowspan=4)
        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=2, row=6)
        self.running = False
        self.start_pause_text.set("Start")
        self.done = False
        self.ration_id = ration_id

        self.weighers = {}
        self.ingredients = []

        db_ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)
        self.desired_amounts = {name: desired_amount for (name, desired_amount, _, _) in self.ingredients}
        unmeasured_counter = 0
        
        self.canvas_size = int(self.controller.screen_height / 2)

        for db_ingredient in db_ingredients:
            name = db_ingredient[0]
            desired_amount = db_ingredient[1]
            weigher_id = db_ingredient[2]
            ordering = db_ingredient[3]
            ingredient = Ingredient(name, desired_amount, ordering)
            self.ingredients.append(ingredient)
            if weigher_id is None:
                button = tk.Button(
                    self.footer, textvariable=ingredient.label, font=self.controller.textFont,
                    command=lambda name=name, amount=ingredient: self.ingredient_done(ingredient)
                )
                button.grid(column=unmeasured_counter, row=0)
                unmeasured_counter += 1
            else:
                if weigher_id not in self.weighers:
                    self.weighers[weigher_id] = Weigher(self, self.controller, weigher_id)
                weigher = self.weighers[weigher_id]
                weigher.add_ingredient(ingredient)
                ingredient.augar = Augar(
                    int(self.controller.config["AUGAR_PINS"].get(name.lower()+"_pin")), 
                    tk.Canvas(weigher.frame, width=self.canvas_size / 10, height=self.canvas_size / 10),
                    self.canvas_size
                )
                ingredient.augar.canvas.grid(column=len(weigher.ingredients) + 1, row=0)
                ingredient.augar.turn_off()
                
        for _, weigher in self.weighers.items():
            if settings.dev_mode:
                button = tk.Button(
                    weigher.frame, text="More",
                    command=lambda weigher=weigher: self.increment_weight(weigher)
                )
                button.grid(column=1, row=3)
            WeightInput(self, self.controller, weigher, int(self.controller.config["WEIGHER_PINS"].get(str(weigher_id))))
            weigher.hopper = Hopper(
                weigher.frame, self.controller, self.canvas_size, self.canvas_size
            )
            weigher.hopper.grid(row=2, column=1, columnspan=4, sticky="nsew")

        for _, weigher in self.weighers.items():
            new_width = weigher.frame.winfo_width()
            if new_width > self.canvas_size:
                weigher.hopper.configure(width=new_width)
                weigher.hopper.width = new_width
                weigher.hopper.draw_hopper()

        self.check_done()
        self.controller.show_frame("RunPage")