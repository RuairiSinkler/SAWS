import time
import tkinter as tk
import numpy as np
from tkinter import ttk
from operator import itemgetter

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

    def increment_value(self, selected_weigher, increment=None):
        ingredients = [(name, amount, ordering) for (name, amount, weigher, ordering) in self.ingredients if weigher == selected_weigher]
        ingredients = sorted(ingredients, key=itemgetter(2), reverse=True)
        current_name = None
        current_amount = None
        next = None
        for (name, amount, _) in ingredients:
            if self.current_weighed[name].get() < amount:
                next = current_name
                current_name = name
                current_amount = amount
        if current_name is None:
            next = None
            current_name = ingredients[0][0]
            current_amount = ingredients[0][1]
        if increment is None:
            new_value = self.current_weighed[current_name].get() + self.controller.weigher_increment
        else:
            new_value = self.current_weighed[current_name].get() + increment
        self.current_weighed[current_name].set(new_value)
        self.label_texts[current_name].set("{}\n{}\n/{}kg".format(current_name, str(self.current_weighed[current_name].get()), str(current_amount)))
        if int(self.desired_amounts.get(current_name)) == 0:
            percentage = 100
        else:
            percentage = (self.current_weighed[current_name].get() / self.desired_amounts.get(current_name)) * 100
        self.weigher_canvases[selected_weigher].fill_hopper(percentage)
        if self.current_weighed[current_name].get() >= current_amount:
            if next is not None:
                self.weigher_canvases[selected_weigher].draw_hopper()
        if self.running:
            if self.current_weighed[current_name].get() >= current_amount:
                self.turn_off_augar(current_name)
                if next is not None:
                    self.turn_on_augar(next)
            else:
                self.turn_on_augar(current_name)
        self.check_done()

    def ingredient_done(self, name, amount):
        if self.current_weighed[name].get() == 0:
            self.current_weighed[name].set(amount)
        else:
            self.current_weighed[name].set(0)
        self.label_texts[name].set("{}\n{}\n/{}kg".format(name, str(self.current_weighed[name].get()), str(amount)))
        self.check_done()

    def check_done(self):
        self.done = True
        for key in self.current_weighed:
            if self.current_weighed.get(key).get() < self.desired_amounts.get(key):
                self.done = False
        if self.done:
            self.end_text.set("Complete")
            self.quit_button.grid()
        else:
            self.end_text.set("End\nRun\nEarly")

    def turn_on_augar(self, name):
        self.augars[name].turn_on_augar()
        self.augars[name].canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="green")

    def turn_off_augar(self, name):
        self.augars[name].turn_off_augar()
        self.augars[name].canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="red")

    def start_pause(self):
        if self.running:
            self.running = False
            self.start_pause_text.set("Start")
            for weigher in range(1, self.max_weigher + 1):
                ingredients = [name for (name, _, ing_weigher, _) in self.ingredients if weigher == ing_weigher]
                for name in ingredients:
                    self.turn_off_augar(name)
            self.quit_button.grid()
        else:
            self.running = True
            self.start_pause_text.set("Pause")
            for weigher in range(1, self.max_weigher + 1):
                self.increment_value(weigher, 0)
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
            headings = ["Date Run", "Ration", "Complete"] + [name for (name, _, _, _) in self.ingredients] + ["Total", "Batch Number"]
            self.controller.ration_logs_ex.setup_sheet(house, headings)
            sheet = self.controller.ration_logs_ex.get_sheet(house)
        self.controller.ration_logs_ex.change_sheet(sheet)
        time_run = time.strftime("%d/%m/%y")
        ration = self.controller.ration_db.get_ration(self.ration_id)[1]
        self.controller.ration_logs_ex.log_run(time_run, ration, self.done, self.current_weighed, batch_number)
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

        self.ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)
        self.desired_amounts = {name: amount for (name, amount, _, _) in self.ingredients}
        weigher_counters = np.ones(10, dtype=int)
        weigher_frames = [None] * 10
        self.weigher_canvases = [None] * 10
        unmeasured_counter = 0
        self.current_weighed = {}
        self.label_texts = {}
        self.augars = {}
        self.max_weigher = 0
        self.canvas_size = int(self.controller.screen_height / 2)
        for ingredient in self.ingredients:
            name = ingredient[0]
            amount = ingredient[1]
            weigher = ingredient[2]
            ordering = ingredient[3]
            if weigher is not None:
                self.max_weigher = max(self.max_weigher, weigher)
            self.current_weighed[name] = tk.DoubleVar()
            self.current_weighed[name].set(0)
            self.label_texts[name] = tk.StringVar()
            self.label_texts[name].set("{}\n{}\n/{}kg".format(name, str(self.current_weighed[name].get()), str(amount)))
            if weigher is None:
                button = tk.Button(
                    self.footer, textvariable=self.label_texts[name], font=self.controller.textFont,
                    command=lambda name=name, amount=amount: self.ingredient_done(name, amount)
                )
                button.grid(column=unmeasured_counter, row=0)
                unmeasured_counter += 1
            else:
                if weigher_frames[weigher] is None:
                    weigher_frames[weigher] = tk.Frame(self.main)
                    weigher_frames[weigher].pack(side=tk.LEFT, expand=True)
                frame = weigher_frames[weigher]
                label = tk.Label(
                    frame, textvariable=self.label_texts[name], font=self.controller.textFont
                )
                label.grid(column=weigher_counters[weigher - 1], row=0)
                self.augars[name] = Augar(
                    int(self.controller.config["AUGAR_PINS"].get(name.lower()+"_pin")), 
                    tk.Canvas(frame, width=self.canvas_size / 10, height=self.canvas_size / 10)
                )
                self.augars[name].canvas.grid(column=weigher_counters[weigher - 1] + 1, row=0)
                self.turn_off_augar(name)
                weigher_counters[weigher - 1] += 2
        for weigher in range(1, self.max_weigher + 1):
            if settings.dev_mode:
                button = tk.Button(
                    weigher_frames[weigher], text="More",
                    command=lambda weigher=weigher: self.increment_value(weigher)
                )
            button.grid(column=1, row=3)
            input = WeightInput(self, self.controller, weigher, int(self.controller.config["WEIGHER_PINS"].get(str(weigher))))
            self.weigher_canvases[weigher] = Hopper(
                weigher_frames[weigher], self.controller, self.canvas_size, self.canvas_size
            )
            self.weigher_canvases[weigher].grid(row=2, column=1, columnspan=4, sticky="nsew")

        for weigher in range(1, self.max_weigher + 1):
            new_width = weigher_frames[weigher].winfo_width()
            if new_width > self.canvas_size:
                self.weigher_canvases[weigher].configure(width=new_width)
                self.weigher_canvases[weigher].width = new_width
                self.weigher_canvases[weigher].draw_hopper()

        self.check_done()
        self.controller.show_frame("RunPage")