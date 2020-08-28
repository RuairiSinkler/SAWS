import tkinter as tk
# import RPi.GPIO as GPIO

import data.settings as settings
from hopper import Hopper

class Weigher:

    def __init__(self, run_page, parent, controller, weigher_id, weigher_pin, increment):
        self.run_page = run_page
        self.parent = parent
        self.controller = controller
        self.weigher_id = weigher_id
        self.weigher_pin = weigher_pin
        GPIO.setup(self.weigher_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.ingredients = []

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT, expand=True)

        if settings.dev_mode:
            print("dev_mode working")
            button = tk.Button(
                self.frame, text="More",
                command=lambda weigher=self: self.run_page.increment_weight(weigher)
            )
            button.grid(column=1, row=3)
        self.hopper = Hopper(
            self.frame, self.controller, self.run_page.canvas_size, self.run_page.canvas_size
        )
        self.hopper.grid(row=2, column=1, columnspan=4, sticky="nsew")

        self.active = True
        self.state = GPIO.input(self.weigher_pin)
        self.check_input()

    @classmethod
    def fromDbWeigher(cls, run_page, parent, controller, db_weigher):
        return cls(run_page, parent, controller, *db_weigher)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        self.ingredients.sort(key=lambda ingredient: ingredient.ordering)

        label = tk.Label(
            self.frame, textvariable=ingredient.label, font=self.controller.textFont
        )
        label.grid(column=(len(self.ingredients) * 2) - 1, row=0)

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