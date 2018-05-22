import DatabaseManagement as db
import ExcelManagement as ex
import RPi.GPIO as GPIO

import time
import sqlite3
import itertools
import configparser
import numpy as np
import tkinter as tk
from tkinter.font import Font
from operator import itemgetter
from openpyxl.utils import column_index_from_string

WEIGHER_INCREMENT = 25

class SAWS(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.ration_db = db.DatabaseManager("rations.db")
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        dir = self.config["DEFAULT"].get("usb_location")
        self.ration_ex = ex.WorksheetManager(dir, "rations")
        self.ration_logs_ex = ex.WorksheetManager(dir, "ration_logs")

        self.setup_database()

        GPIO.setmode(GPIO.BCM)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry("{0}x{1}+0+0".format(self.screen_width, self.screen_height))
        self.resizable(False, False)
        self.overrideredirect(True)
        self.mainFont = Font(size=25)
        self.textFont = Font(size=15)
        self.option_add('*Dialog.msg.font', self.mainFont)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        for F in (SplashPage, PinPage, MainMenu, RationPage, RunPage, AreYouSure, BatchPage):
            self.create_frame(F, container)

        self.show_frame("SplashPage")

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
        frame.tkraise()

    def setup_database(self):
        try:
            self.ration_db.clear()
        except sqlite3.OperationalError:
            pass
        self.ration_db.build()

        ingredient_cell = self.ration_ex.find("Ingredient")
        top_row = ingredient_cell.row
        column = column_index_from_string(ingredient_cell.column)
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            weigher = self.ration_ex.read_cell(self.ration_ex.get_cell(column  + 1, row))
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
                amount = self.ration_ex.read_cell(self.ration_ex.get_cell(col, row))
                self.ration_db.insert_ration_ingredients((ration_id, ingredient_id, amount))

        house_cell = self.ration_ex.find("Houses")
        top_row = house_cell.row
        column = column_index_from_string(house_cell.column)
        for row in itertools.count(top_row + 1):
            name = self.ration_ex.read_cell(self.ration_ex.get_cell(column, row))
            if name is None:
                break
            self.ration_db.insert_house([name])


class SplashPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(
            self, text="Start", font=controller.mainFont, command=lambda: self.controller.show_frame("PinPage")
        )
        button.pack(fill="none", expand="True")

class PinPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        explanation = tk.Label(self, text="Please enter the PIN code:", font=self.controller.mainFont)
        explanation.grid(row=1, column=1)
        pin_pad = NumPad(self, controller, lambda: self.check_pin(pin_pad))
        pin_pad.grid(row=2, column=1)

    def check_pin(self, pin_pad):
        pin = pin_pad.entry.get()
        pin_cell = self.controller.ration_ex.find("PIN")
        column = column_index_from_string(pin_cell.column)
        row = pin_cell.row
        set_pin = self.controller.ration_ex.read_cell(self.controller.ration_ex.get_cell(column + 1, row))
        if pin == str(set_pin):
            pin_pad.entry.delete(0, tk.INSERT)
            self.controller.show_frame("MainMenu")

class BatchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        explanation = tk.Label(self, text="Please enter the 6 digit\nBatch Number:", font=self.controller.mainFont)
        explanation.grid(row=1, column=1)
        num_pad = NumPad(self, controller, lambda: self.controller.frames["RunPage"].log_run(num_pad.entry.get()))
        num_pad.grid(row=2, column=1)

class NumPad(tk.Frame):

    def __init__(self, parent, controller, enter_function):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.entry = tk.Entry(self, font=self.controller.mainFont)
        self.entry.grid(column=0, row=0, columnspan=3)
        for number in range(1, 10):
            button = tk.Button(
                self, text=str(number), font=controller.mainFont, command=lambda n=number: self.entry.insert(tk.INSERT, str(n))
            )
            button.grid(column=(number - 1) % 3, row=int((number - 1) / 3) + 1, sticky="ew")
        delete = tk.Button(
            self, text="  DEL  ", font=controller.mainFont, command=lambda: self.entry.delete(self.entry.index(tk.INSERT) - 1)
        )
        delete.grid(column=0, row=4, sticky="ew")
        zero = tk.Button(
            self, text="   0   ", font=controller.mainFont, command=lambda: self.entry.insert(tk.INSERT, "0")
        )
        zero.grid(column=1, row=4, sticky="ew")
        enter = tk.Button(
            self, text="ENTER", font=controller.mainFont, command=enter_function
        )
        enter.grid(column=2, row=4, sticky="ew")

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        rations = self.controller.ration_db.get_all_rations()

        for ration in rations:
            id = ration[0]
            name = ration[1]
            button = tk.Button(
                self, text=name, font=self.controller.mainFont,
                command=lambda id=id: self.controller.frames["RationPage"].display_page(id)
            )
            button.pack(fill="x")

        button = tk.Button(
            self, text="Quit", font=controller.mainFont, command=lambda: self.controller.show_frame("SplashPage")
        )
        button.pack(fill="x")

        button = tk.Button(
            self, text="QUIT", font=controller.mainFont, fg="red", command=controller.quit
        )
        button.pack(fill="x")

class RationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.master = tk.Frame(self)
        self.master.pack()
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM)

        self.controller = controller

        self.ration_id = None
        self.name = None

        # for x in range(2):
        #     tk.Grid.rowconfigure(self, x, weight=1)
        # for y in range(5):
        #     tk.Grid.columnconfigure(self, y, weight=1)

        button = tk.Button(
            self.footer, text="Back", font=self.controller.mainFont,
            command=lambda: self.controller.show_frame("MainMenu")
        )

        button.pack(side=tk.LEFT)

        button = tk.Button(
            self.footer, text="Run", font=self.controller.mainFont,
            command=lambda: self.controller.frames["RunPage"].display_page(self.ration_id)
        )

        button.pack(side=tk.LEFT)


    def display_page(self, ration_id):

        self.master.destroy()
        self.master = tk.Frame(self)
        self.master.pack()

        self.ration_id = ration_id

        self.name = self.controller.ration_db.get_ration(self.ration_id)[1]
        ingredients = self.controller.ration_db.get_ration_ingredients(ration_id)
        label = tk.Label(
            self.master, text=self.name, font=self.controller.mainFont
        )
        label.pack()
        for ingredient in ingredients:
            label = tk.Label(
                self.master, text="{}, {}kg".format(ingredient[0], str(ingredient[1])), font=self.controller.mainFont
            )
            label.pack()


        self.controller.show_frame("RationPage")


class RunPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.master = tk.Frame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.master.grid(column=2, row=2, rowspan=4, sticky="nsew")
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
        self.house = tk.StringVar()
        self.house.set(house_names[0])
        self.house_dropdown = tk.OptionMenu(self, self.house, *house_names)
        self.house_dropdown.config(font=self.controller.mainFont)
        self.house_dropdown["menu"].config(font=self.controller.mainFont)
        self.house_dropdown.grid(column=2, row=1)

        self.end_text = tk.StringVar()
        self.end_text.set("End\nRun\nEarly")
        self.quit_button = tk.Button(
            self, textvariable=self.end_text, font=self.controller.mainFont,
            command=lambda: self.controller.show_frame("AreYouSure")
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
            new_value = self.current_weighed[current_name].get() + WEIGHER_INCREMENT
        else:
            new_value = self.current_weighed[current_name].get() + increment
        self.current_weighed[current_name].set(new_value)
        self.label_texts[current_name].set("{}\n{}\n/{}kg".format(current_name, str(self.current_weighed[current_name].get()), str(current_amount)))
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
        GPIO.output(self.augars[name][0], True)
        self.augars[name][1].create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="green")

    def turn_off_augar(self, name):
        GPIO.output(self.augars[name][0], False)
        self.augars[name][1].create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="red")

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

    def log_run(self, batch_number):
        # result = messagebox.askyesno("End run early", "Are you sure you want to end the run before completing the ration?", icon='warning')
        # if result:
        house = self.house.get()
        if house in self.controller.ration_logs_ex.workbook.sheetnames:
            sheet = self.controller.ration_logs_ex.get_sheet(house)
        else:
            self.controller.ration_logs_ex.create_sheet(house)
            sheet = self.controller.ration_logs_ex.get_sheet(house)
            self.controller.ration_logs_ex.change_sheet(sheet)
            headings = ["Time Run", "Ration", "Complete"] + [name for (name, _, _, _) in self.ingredients] + ["Total", "Batch Number"]
            self.controller.ration_logs_ex.setup_sheet(house, headings)
            sheet = self.controller.ration_logs_ex.get_sheet(house)
        self.controller.ration_logs_ex.change_sheet(sheet)
        time_run = time.strftime("%H:%M:%S, %d/%m/%y")
        ration = self.controller.ration_db.get_ration(self.ration_id)[1]
        self.controller.ration_logs_ex.log_run(time_run, ration, self.done, self.current_weighed, batch_number)
        self.controller.ration_logs_ex.save()

        self.controller.show_frame("MainMenu")


    def display_page(self, ration_id):
        self.master.destroy()
        self.footer.destroy()
        self.master = tk.Frame(self)
        self.master.grid(column=2, row=2, rowspan=4)
        self.footer = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.footer.grid(column=2, row=6)
        self.running = False
        self.start_pause_text.set("Start")
        self.done = False
        self.ration_id = ration_id

        # unmeasured = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        # unmeasured.pack(side=tk.BOTTOM)
        # measured = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        # measured.pack(side=tk.BOTTOM, expand=True)

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
            # print(ingredient)
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
                    weigher_frames[weigher] = tk.Frame(self.master)
                    weigher_frames[weigher].pack(side=tk.LEFT, expand=True)
                frame = weigher_frames[weigher]
                label = tk.Label(
                    frame, textvariable=self.label_texts[name], font=self.controller.textFont
                )
                label.grid(column=weigher_counters[weigher - 1], row=0)
                print(name)
                print(name.lower())
                print(name.lower()+"_pin")
                print(self.controller.config["AUGAR_PINS"].get(name.lower()+"_pin"))
                self.augars[name] = (int(self.controller.config["AUGAR_PINS"].get(name.lower()+"_pin")), tk.Canvas(
                    frame, width=self.canvas_size / 10, height=self.canvas_size / 10
                ))
                GPIO.setup(self.augars[name][0], GPIO.OUT)
                self.augars[name][1].grid(column=weigher_counters[weigher - 1] + 1, row=0)
                self.turn_off_augar(name)
                weigher_counters[weigher - 1] += 2
        for weigher in range(1, self.max_weigher + 1):
            # button = tk.Button(
            #     weigher_frames[weigher], text="More",
            #     command=lambda weigher=weigher: self.increment_value(weigher)
            # )
            # button.grid(column=1, row=3)
            input = WeightInput(weigher, int(self.controller.config["WEIGHER_PINS"].get(str(weigher))))
            self.weigher_canvases[weigher] = Hopper(
                weigher_frames[weigher], self.controller, self.canvas_size, self.canvas_size
            )
            self.weigher_canvases[weigher].grid(row=2, column=1, columnspan=4, sticky="nsew")
            # weigher_frames[weigher].grid_rowconfigure(1, weight=1)
            # weigher_frames[weigher].grid_columnconfigure(0, weight=1)
            # weigher_frames[weigher].grid_rowconfigure(1, weight=1)
            # weigher_frames[weigher].grid_rowconfigure(3, weight=1)
            # weigher_frames[weigher].grid_columnconfigure(0, weight=1)
            # weigher_frames[weigher].grid_columnconfigure(weigher_counters[weigher - 1], weight=1)
        for weigher in range(1, self.max_weigher + 1):
            new_width = weigher_frames[weigher].winfo_width()
            if new_width > self.canvas_size:
                self.weigher_canvases[weigher].configure(width=new_width)
                self.weigher_canvases[weigher].width = new_width
                self.weigher_canvases[weigher].draw_hopper()

        self.check_done()
        self.controller.show_frame("RunPage")

class AreYouSure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        w = tk.Label(self, text="Are you sure you want to end the run?\nThe ration is not yet complete.", font=self.controller.mainFont)
        w.grid(row=1, column=1, columnspan=2)

        button = tk.Button(
            self, text="Yes", font=controller.mainFont, command=lambda: controller.show_frame("BatchPage")
        )
        button.grid(row=2, column=1, sticky="ew")

        button = tk.Button(
            self, text="No", font=controller.mainFont, command=lambda: controller.show_frame("RunPage")
        )
        button.grid(row=2, column=2, sticky="ew")

class Hopper(tk.Canvas):

    def __init__(self, parent, controller, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.controller = controller
        self.width = width
        self.height = height
        self.triangle_y = 4 * height / 10
        self.triangle_height = self.height - self.triangle_y
        self.draw_hopper()

    def draw_hopper(self):
        self.delete("all")
        points = [0, 0, self.width, 0, self.width, self.triangle_y, self.width / 2, self.height, 0, self.triangle_y]
        self.hopper = self.create_polygon(points, fill='black', outline='black', width=3)
        self.update()

    def fill_hopper(self, percentage):
        fill_height = int(self.height * (percentage / 100.0))
        fill_y = self.height - fill_height
        if fill_height >= self.triangle_height:
            points = [0, fill_y, self.width, fill_y, self.width, self.triangle_y, self.width / 2, self.height, 0,
                      self.triangle_y]
            self.fill = self.create_polygon(points, fill='yellow')
        else:
            triangle_proportion = fill_height / (self.triangle_height)
            fill_width = self.width * triangle_proportion
            gap = (self.width - fill_width) / 2
            points = [gap, fill_y, self.width - gap, fill_y, self.width / 2, self.height]
            self.fill = self.create_polygon(points, fill='yellow')
        self.update()

class WeightInput():

    def __init__(self, weigher, weight_pin):
        self.weigher = weigher
        self.pin = weight_pin
        GPIO.setup(self.pin, GPIO.IN)
        self.state = GPIO.input(self.pin)
        self.check_input()

    def check_input(self):
        oldstate = self.state
        newstate = GPIO.input(self.pin)
        if oldstate != newstate:
            self.state = newstate
            if newstate == GPIO.LOW:
                self.increment_value(self.weigher)
        self.master.after(0.01, self.check_input)

def main():
    # root = tk.Tk()
    # hopper = Hopper(root, root, 1000, 600)
    # hopper.pack()
    # root.mainloop()
    saws = SAWS()
    saws.mainloop()

if __name__ == "__main__":
    try:
        main()
    except:
        raise
