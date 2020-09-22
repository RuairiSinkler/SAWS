import time
import tkinter as tk
import numpy as np
from tkinter import ttk
from operator import itemgetter

from pages.page_tools.ingredient import Ingredient
from pages.page_tools.weigher import Weigher

class RunPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(4, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(4, weight=1)

        self.main = tk.Frame(self)
        self.main.grid(column=1, row=1)

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=1, row=2, rowspan=3)

        self.controller = controller

        self.running = False
        self.max_weigher = 0
        self.done = False
        self.ration_id = None

        self.start_pause_text = tk.StringVar()
        self.start_pause_text.set("Start")
        button = tk.Button(
            self, textvariable=self.start_pause_text, font=self.controller.main_font, command=self.start_pause
        )
        button.grid(column=0, row=1)

        houses = self.controller.ration_db.get_all_houses()
        house_names = [house[1] for house in houses]
        self.house_dropdown = ttk.Combobox(self, values=house_names, state="readonly", font=self.controller.main_font)
        self.house_dropdown.current(0)
        self.house_dropdown.grid(column=1, row=0)

        self.end_text = tk.StringVar()
        self.end_text.set("End\nRun\nEarly")
        self.quit_button = tk.Button(
            self, textvariable=self.end_text, font=self.controller.main_font,
            command=lambda: self.controller.frames["AreYouSurePage"].display_page(self.done)
        )
        self.quit_button.grid(column=2, row=1)

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
        
        self.done = self.check_done()

    def ingredient_done(self, ingredient):
        if ingredient.current_amount == 0:
            ingredient.current_amount = ingredient.desired_amount
        else:
            ingredient.current_amount = 0
        ingredient.label.set("{}\n{}\n/{}kg".format(ingredient.name, str(ingredient.current_amount), str(ingredient.desired_amount)))
        self.done = self.check_done()

    def check_done(self):
        done = True
        for ingredient in self.ingredients:
            if not ingredient.done():
                done = False
        if done:
            self.end_text.set("Complete")
            self.quit_button.grid()
        else:
            self.end_text.set("End\nRun\nEarly")
        return done

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

        for _, weigher in self.weighers.items():
            weigher.active = False
        self.weighers = {}

        self.controller.show_frame("MainMenuPage")
        num_pad.clear()

    def display_page(self, ration_id):
        self.main.destroy()
        self.footer.destroy()

        self.main = tk.Frame(self)
        self.main.grid(column=1, row=1)

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=1, row=2, rowspan=3)

        self.running = False
        self.start_pause_text.set("Start")
        self.done = False
        self.ration_id = ration_id

        self.weighers = {}
        self.ingredients = []

        db_ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)

        for db_ingredient in db_ingredients:
            ingredient = Ingredient.fromDbIngredient(db_ingredient)
            self.ingredients.append(ingredient)
            if ingredient.weigher_id is None:
                button = tk.Button(
                    self.footer, textvariable=ingredient.label, font=self.controller.text_font,
                    command=lambda ingredient=ingredient: self.ingredient_done(ingredient)
                )
                button.pack(side=tk.LEFT)
            else:
                if ingredient.weigher_id not in self.weighers:
                    db_weigher = self.controller.ration_db.get_weigher(ingredient.weigher_id)
                    self.weighers[ingredient.weigher_id] = Weigher.fromDbWeigher(self, self.main, self.controller, db_weigher)
                weigher = self.weighers[ingredient.weigher_id]
                weigher.add_ingredient(ingredient)

        # for _, weigher in self.weighers.items():
        #     new_width = weigher.frame.winfo_width()
        #     if new_width > self.canvas_size:
        #         weigher.hopper.configure(width=new_width)
        #         weigher.hopper.width = new_width
        #         weigher.hopper.draw_hopper()

        self.done = self.check_done()
        self.controller.show_frame("RunPage")