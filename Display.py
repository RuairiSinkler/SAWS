from abc import ABC, abstractmethod
import tkinter
from tkinter import messagebox
from TkInterKeyboard import *

class Display(ABC):
    def __init__(self, ration_database):
        self.weights = None
        self.ration_database = ration_database

    def setup_weights(self):
        self.weights = [0, 0, 0, 0]

    @abstractmethod
    def menu(self):
        pass

    @abstractmethod
    def end(self, end_weights):
        pass

    @abstractmethod
    def assignments(self):
        pass

    @abstractmethod
    def rations(self):
        pass

    @abstractmethod
    def settings(self):
        pass

    @abstractmethod
    def display_weights(self):
        pass

    @abstractmethod
    def update_weights(self, weights, weight_limts):
        pass

    @abstractmethod
    def message(self, message):
        pass

    @abstractmethod
    def ask(self, question):
        pass

    @abstractmethod
    def get_input(self, prompt):
        pass

    @abstractmethod
    def enter(self, value):
        pass

    @abstractmethod
    def change(self, value, old_value):
        pass

class ConsoleDisplay(Display):
    def menu(self):
        print("Welcome to ASWA (Automatic Sinkler Weighing System)")
        print("Main Menu:")
        print("-Run")
        print("-Settings")
        print("-Shutdown")
        print("Please type in a command from the above menu")
        command = input("> ").lower()
        return command

    def print_row(self, values):
        print(("{v[0]:^3d} | {v[1]:^15} | {v[2]:^5d} | {v[3]:^6d} | {v[4]:^5d} | {v[5]:^9d} | " +
               "{v[6]:^8d} | {v[7]:^8d} | {v[8]:^10.2f} | {v[9]:^7d}").format(v=values)
              )
        print("{:-^103}".format(""))

    def end(self, end_weights, weight_limits):
        print("Run complete, end result:")
        self.display_weights(end_weights, weight_limits)

    def print_assignment(self, assignment):
        print(("{a[0]:^8} | {a[1]:^11} | {a[2]:^9} | {a[3]:^15} | {a[4]:^9}").format(a=assignment)
              )
        print("{:-^64}".format(""))

    def assignments(self):
        assignments = self.ration_database.get_assignments()
        print(("{:^8} | {:^11} | {:^9} | {:^15} | {:^9}").format("House ID", "House", "Ration ID", "Ration", "Batch No."))
        print("{:-^64}".format(""))
        for assignment in assignments:
            self.print_assignment(assignment)
        print("Select a house using its ID")
        command = input("> ").lower()
        return command

    def rations(self):
        print("Please select a ration using its ID: ")
        rations = self.ration_database.get_all_rations()
        print(("{:^3} | {:^15} | {:^5} | {:^6} | {:^5} | {:^9} | {:^8} | {:^8} | {:^10} | {:^7}").format(
            "ID", "Name", "Wheat", "Barley", "Soya", "Limestone", "Soya Oil", "Arbocell", "Methionine", "Premix"
        ))
        print("{:-^103}".format(""))
        for ration in rations:
            self.print_row(ration)
        command = input("> ").lower()
        return command

    def settings(self):
        print("Settings:")
        print("-Assign rations")
        print("-Add ration")
        print("-Edit ration")
        print("-Delete ration")
        print("-Change batch")
        print("-Back")
        command = input("> ").lower()
        return command

    def display_weights(self, weights, weight_limits):
        print(
            "Wheat weight: " + str(weights[0]) +
            "/" + str(weight_limits[0]) +
            " Barley weight: " + str(weights[1]) +
            "/" + str(weight_limits[1])
        )
        print(
            "Soya weight: " + str(weights[2]) +
            "/" + str(weight_limits[2]) +
            " Limestone weight: " + str(weights[3]) +
            "/" + str(weight_limits[3])
        )

    def update_weights(self, weights, weight_limits):
        update = (self.weights != weights)
        if update:
            self.weights = weights
            self.display_weights(weights, weight_limits)

    def message(self, message):
        print(message)

    def ask(self, question):
        print(question)
        success = False
        while not(success):
            result = input("Y/N> ").upper()
            if result == "Y":
                success = True
                return True
            elif result == "N":
                success = True
                return False
            else:
                pass

    def get_input(self, prompt):
        result = input(prompt)
        return result

    def enter(self, value):
        print("Please enter the value for {}".format(value))
        success = False
        while not (success):
            result = input("> ")
            success = True
            if not (value == "name"):
                if not (result.isdigit()):
                    success = False
                    print("Sorry I need a positive number as an input")
                else:
                    result = int(result)
        return result

    def change(self, value, old_value):
        print("Please enter the value for {}, it is currently {}".format(value, str(old_value)))
        success = False
        while not (success):
            result = input("> ")
            success = True
            if (result == ""):
                result = old_value
            elif not (value == "name"):
                if not (result.isdigit()):
                    success = False
                    print("Sorry I need a positive number as an input")
                else:
                    result = int(result)
        return result

class GUIDisplay(Display):

    BUTTONS = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "BACKSPACE"],
               ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "ENTER"],
               ["CAPS LOCK", "a", "s", "d", "f", "g", "h", "j", "k", "l"],
               ["SHIFT", "z", "x", "c", "v", "b", "n", "m", ",", "."],
               ["BLANK", "BLANK", "BLANK", "SPACE"]]
    ALT_BUTTONS = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "BACKSPACE"],
                   ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "ENTER"],
                   ["CAPS LOCK", "A", "S", "D", "F", "G", "H", "J", "K", "L"],
                   ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", "."],
                   ["BLANK", "BLANK", "BLANK", "SPACE"]]

    def __init__(self, ration_database):
        super().__init__(ration_database)
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.header = tkinter.Frame(self.root)
        self.header.pack()
        self.master = tkinter.Frame(self.root)
        self.master.pack()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(str(self.screen_width), str(self.screen_height)))
        self.mainloop_called = False
        #self.root.overrideredirect(1)

    def setup_weights(self):
        self.weights = [tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()]

    def clear(self):
        self.master.destroy()
        self.master = tkinter.Frame(self.root)
        self.master.pack()

    def menu(self):
        self.clear()
        result = tkinter.StringVar()
        welcome = tkinter.Label(self.master, text="Welcome to SAWS (Sinkler Automatic Weighing System)")
        welcome.pack()
        main_menu = tkinter.Label(self.master, text="Main Menu:")
        main_menu.pack()
        run = tkinter.Button(self.master, text="Run", command = lambda: result.set("Run"))
        run.pack()
        settings = tkinter.Button(self.master, text="Settings", command = lambda: result.set("Settings"))
        settings.pack()
        shutdown = tkinter.Button(self.master, text="Shutdown", command = lambda: result.set("Shutdown"))
        shutdown.pack()
        if not(self.mainloop_called):
            self.root.after(1000, self.menu)
            self.mainloop_called = True
            self.root.mainloop()
            self.mainloop_called = True
        while result.get() == "":
            pass
        return result.get()

    def end(self, end_weights):
        pass

    def assignments(self):
        self.clear()
        result = tkinter.IntVar()
        result.set(-1)
        assignments = self.ration_database.get_assignments()
        titles = ["House", "Ration", "Batch No."]
        r = 0
        c = 0
        for title in titles:
            tkinter.Label(text=title).grid(row=r, column=c)
            c = c + 1
        r = r + 1
        for assignment in assignments:
            callback = lambda a=assignment: result.set(assignment[0])
            tkinter.Button(text=assignment[1], command=callback).grid(row=r, column=0)
            tkinter.Label(text=assignment[3]).grid(row=r, column=1)
            tkinter.Label(text=assignment[4]).grid(row=r, column=2)
            r = r + 1

        while result.get() == -1:
            pass

        return result.get()

    def rations(self):
        pass

    def settings(self):
        pass

    def display_weights(self, weights, weight_limits):
        self.clear()
        r = 0
        c = 0
        for value in self.weights:
            tkinter.Label(text="{}/{}".format(str(value.get()), str(weight_limits[c]))).grid(row=r, column=c)
            c = c + 1

    def update_weights(self, weights):
        for i in range(4):
            self.weights[i].set(weights[i])

    def message(self, message):
        frame = tkinter.Frame(self.header).pack()

        msg = tkinter.Message(frame, text=message)
        msg.pack()

        button = tkinter.Button(frame, text="Dismiss", command=frame.destroy)
        button.pack()

    def ask(self, question):
        return messagebox.askyesno(message=question)

    def get_input(self, prompt):
        self.clear()
        result = tkinter.StringVar()
        textbox = tkinter.Entry()
        enter_function = lambda: result.set(textbox.get())
        kb = keyboard(self.root, self.master, textbox, self.BUTTONS, self.ALT_BUTTONS, enter_function)
        while result.get() == "":
            pass
        return result.get()


    def enter(self, value):
        pass

    def change(self, value, old_value):
        pass