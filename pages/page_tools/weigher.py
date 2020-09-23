import tkinter as tk
import tkinter.font as tkfont
import RPi.GPIO as GPIO

import data.settings as settings
from pages.page_tools.hopper import Hopper
from pages.page_tools.augar import Augar
from pages.page_tools.font_manager import *

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

        self.label_font = tkfont.Font(size=15)

        frame_column = len(self.run_page.weighers)

        self.frame = tk.Frame(self.parent, relief=tk.RAISED, borderwidth=1)
        self.frame.grid(row=0, column=frame_column, sticky="ew")

        self.parent.columnconfigure(frame_column, weight=1)

        self.ingredients_frame = tk.Frame(self.frame)
        self.ingredients_frame.pack(fill="x")

        self.active = True
        self.state = GPIO.input(self.weigher_pin)
        self.check_input()

    @classmethod
    def fromDbWeigher(cls, run_page, parent, controller, db_weigher):
        return cls(run_page, parent, controller, *db_weigher)

    def add_hopper(self):
        self.hopper = Hopper(self.frame)
        self.hopper.pack(fill=tk.BOTH, expand=True)

        if settings.dev_mode:
            button = tk.Button(
                self.frame, text="More",
                command=lambda weigher=self: self.run_page.increment_weight(weigher)
            )
            button.pack()

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        self.ingredients.sort(key=lambda ingredient: ingredient.ordering)

        label_column = ((len(self.ingredients) * 2) - 2)

        label = tk.Label(
            self.ingredients_frame, textvariable=ingredient.label, font=self.label_font
        )
        label.grid(row=0, column=label_column, sticky="ew")

        self.ingredients_frame.columnconfigure(label_column, weight=1)

        ingredient.augar = Augar(
            self.ingredients_frame,
            int(ingredient.augar_pin)
        )
        ingredient.augar.canvas.grid(row=0, column=label_column + 1, sticky="ew")

        self.ingredients_frame.update_idletasks()

        ingredient.augar.turn_off()
        
        for ingredient in self.ingredients:
            resize_font_width(ingredient.label.get(), self.label_font, label.winfo_width())

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