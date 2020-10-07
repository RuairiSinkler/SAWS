import tkinter as tk
import tkinter.font as tkfont
import RPi.GPIO as GPIO

import data.settings as settings
import pages.page_tools.font_manager as fm
from pages.page_tools.hopper import Hopper
from pages.page_tools.augar import Augar

class Weigher:

    def __init__(self, run_page, parent, controller, weigher_id, weigher_pin, increment):
        self.run_page = run_page
        self.parent = parent
        self.controller = controller
        self.weigher_id = weigher_id
        self.weigher_pin = weigher_pin
        self.increment = increment
        GPIO.setup(self.weigher_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.ingredients = []

        self.labels = {}

        self.label_font = tkfont.Font(size=15)

        self.frame_column = len(self.run_page.weighers)

        self.ingredients_frame = tk.Frame(self.parent, relief=tk.RAISED, borderwidth=1)
        self.ingredients_frame.grid(row=0, column=self.frame_column, sticky="nsew")
        self.ingredients_frame.grid_rowconfigure(0, weight=1)

        self.parent.grid_columnconfigure(self.frame_column, weight=1, uniform="weigher_frames")

        self.active = True
        self.state = GPIO.input(self.weigher_pin)
        self.check_input()

    @classmethod
    def fromDbWeigher(cls, run_page, parent, controller, db_weigher):
        return cls(run_page, parent, controller, *db_weigher)

    def resize_labels(self):
        self.parent.update_idletasks()
        for ingredient in self.ingredients:
            label = self.labels[ingredient.name]
            text = "{}\n{}/{}kg".format(ingredient.name, ingredient.desired_amount, ingredient.desired_amount)
            fm.resize_font_width(text, self.label_font, label.winfo_width())

    def add_hopper(self):
        self.hopper = Hopper(self.parent, self.ingredients_frame.winfo_width())
        self.hopper.grid(row=1, column=self.frame_column, sticky="nsew")

        if settings.dev_mode:
            self.hopper.bind("<Button-1>", lambda e, weigher=self: self.run_page.increment_weight(weigher))

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        self.ingredients.sort(key=lambda ingredient: ingredient.ordering)

        label_column = ((len(self.ingredients) * 2) - 2)

        label = tk.Label(
            self.ingredients_frame, textvariable=ingredient.label, font=self.label_font
        )
        label.grid(row=0, column=label_column, sticky="nsew")

        self.labels[ingredient.name] = label

        self.ingredients_frame.grid_columnconfigure(label_column, weight=1, uniform="weigher_{}_ingredient_labels".format(self.weigher_id))

        augar_square_size = self.controller.text_font.metrics('linespace')

        ingredient.augar = Augar(
            self.ingredients_frame,
            int(ingredient.augar_pin),
            augar_square_size
        )
        ingredient.augar.canvas.grid(row=0, column=label_column + 1, sticky="ew")

        self.ingredients_frame.update_idletasks()

        ingredient.augar.turn_off()

    def get_active_ingredient(self):
        for ingredient in self.ingredients:
            if ingredient.augar.active:
                return ingredient
        for ingredient in self.ingredients:
            if not ingredient.done():
                return ingredient
        return None

    def check_input(self):
        old_state = self.state
        new_state = GPIO.input(self.weigher_pin)
        if old_state != new_state:
            self.state = new_state
            if new_state == GPIO.HIGH:
                self.run_page.increment_weight(self)
        if self.active:
            self.controller.after(200, self.check_input)