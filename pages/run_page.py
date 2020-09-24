import time
import numpy as np
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from operator import itemgetter

from pages.page_tools.ingredient import Ingredient
from pages.page_tools.weigher import Weigher
from pages.page_tools.font_manager import *

class RunPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.header.grid(column=0, row=0, columnspan=3, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)

        self.main = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.main.grid(column=0, row=1, sticky="nsew")

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=0, row=2, sticky="ew")

        self.controller = controller

        self.running = False
        self.max_weigher = 0
        self.done = False
        self.ration_id = None

        self.start_pause_text = tk.StringVar()
        self.start_pause_text.set("Start")
        button = tk.Button(
            self.header, textvariable=self.start_pause_text, font=self.controller.main_font, command=self.start_pause
        )
        button.grid(column=0, row=0, sticky="ew")

        self.end_text = tk.StringVar()
        self.end_text.set("End Run Early")
        self.quit_button = tk.Button(
            self.header, textvariable=self.end_text, font=self.controller.main_font,
            command=lambda: self.controller.frames["AreYouSurePage"].display_page(self.done)
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
        
        self.done = self.check_done()

    def ingredient_done(self, ingredient):
        if ingredient.current_amount == 0:
            ingredient.current_amount = ingredient.desired_amount
        else:
            ingredient.current_amount = 0
        ingredient.label.set("{}\n{}/{}kg".format(ingredient.name, str(ingredient.current_amount), str(ingredient.desired_amount)))
        self.done = self.check_done()

    def check_done(self):
        done = True
        for ingredient in self.ingredients:
            if not ingredient.done():
                done = False
        if done:
            self.end_text.set("Complete")
            self.header.grid_columnconfigure(1, weight=1)
            self.quit_button.grid()
        else:
            self.end_text.set("End Run Early")
        return done

    def start_pause(self):
        if self.running:
            self.running = False
            self.start_pause_text.set("Start")
            for _, weigher in self.weighers.items():
                for ingredient in weigher.ingredients:
                    ingredient.augar.turn_off()
            self.header.grid_columnconfigure(1, weight=1)
            self.quit_button.grid()
        else:
            self.running = True
            self.start_pause_text.set("Pause")
            for _, weigher in self.weighers.items():
                self.increment_weight(weigher, 0)
            if not self.done:
                self.quit_button.grid_remove()
                self.header.grid_columnconfigure(1, weight=0)

    def log_run(self, house_dropdown, num_pad):
        house = house_dropdown.get()
        batch_number = num_pad.entry.get()
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
        house_dropdown.current(0)
        num_pad.clear()

    def display_page(self, ration_id):
        self.main.destroy()
        self.footer.destroy()

        self.main = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.main.grid(column=0, row=1, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)

        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=0, row=2, sticky="ew")

        self.running = False
        self.start_pause_text.set("Start")
        self.done = False
        self.ration_id = ration_id

        self.weighers = {}
        self.ingredients = []

        db_ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)

        unweighed_ingredients = []
        unweighed_button_font = tkfont.Font(size=self.controller.text_font['size'])

        for db_ingredient in db_ingredients:
            ingredient = Ingredient.fromDbIngredient(db_ingredient)
            self.ingredients.append(ingredient)
            if ingredient.weigher_id is None:
                button_column = len(unweighed_ingredients)
                button = tk.Button(
                    self.footer, textvariable=ingredient.label, font=unweighed_button_font,
                    command=lambda ingredient=ingredient: self.ingredient_done(ingredient)
                )
                button.grid(row=0, column=button_column, sticky="ew")
                self.footer.grid_columnconfigure(button_column, weight=1)
                unweighed_ingredients.append((ingredient, button))
            else:
                if ingredient.weigher_id not in self.weighers:
                    db_weigher = self.controller.ration_db.get_weigher(ingredient.weigher_id)
                    self.weighers[ingredient.weigher_id] = Weigher.fromDbWeigher(self, self.main, self.controller, db_weigher)
                weigher = self.weighers[ingredient.weigher_id]
                weigher.add_ingredient(ingredient)


        self.main.update_idletasks()
        weigher_frame_width = self.controller.screen_width // len(self.weighers)
        for _, weigher in self.weighers.items():
            weigher.frame.config(width=weigher_frame_width)
            weigher.add_hopper()

        for ingredient, button in unweighed_ingredients:
            button.update_idletasks()
            text = "{}\n{}/{}kg".format(ingredient.name, ingredient.desired_amount, ingredient.desired_amount)
            resize_font_width(text, unweighed_button_font, button.winfo_width())

        self.done = self.check_done()
        self.controller.show_frame("RunPage")