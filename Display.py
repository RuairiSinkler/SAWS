
from abc import ABC, abstractmethod

class Display(ABC) :

    def __init__(self, ration_database) :
        self.weights = None
        self.ration_database = ration_database

    def setup_weights(self) :
        self.weights = [None, None, None, None]

    @abstractmethod
    def menu(self) :
        pass

#    @abstractmethod
    def run(self) :
        pass

    @abstractmethod
    def end(self, end_weights) :
        pass

    @abstractmethod
    def rations(self) :
        pass

    @abstractmethod
    def settings(self) :
        pass

    @abstractmethod
    def display_weights(self, weights, weight_limits) :
        pass

    @abstractmethod
    def update_weights(self, weights) :
        pass

    @abstractmethod
    def message(self, message) :
        pass

class ConsoleDisplay(Display) :

    def menu(self) :
        print("Welcome to ASWA (Automatic Sinkler Weighing System)")
        print("Main Menu:")
        print("-Run")
        print("-Settings")
        print("-Shutdown")
        print("Please type in a command from the above menu")
        command = input("> )").lower()
        return command

    def print_row(self, values) :
        print(("{v[0]:^3d} | {v[1]:^15} | {v[2]:^5d} | {v[3]:^6d} | {v[4]:^5d} | {v[5]:^9d} | " +
            "{v[6]:^8d} | {v[7]:^8d} | {v[8]:^10d} | {v[9]:^7d}").format(v=values)
        )
        print("{:-^103}".format(""))

    def end(self, end_weights, weight_limits) :
        print("Run complete, end result:")
        self.display_weights(end_weights, weight_limits)

    def print_assignment(self, assignment) :
        print(("{a[0]:^8} | {a[1]:^11} | {a[2]:^9} | {a[3]:^15}").format(a=assignment)
              )
        print("{:-^52}".format(""))

    def assignments(self) :
        assignments = self.ration_database.get_assignments()
        print(("{:^8} | {:^11} | {:^9} | {:^15}").format("House ID", "House", "Ration ID" "Ration"))
        print("{:-^52}".format(""))
        for assignment in assignments :
            self.print_assignment(assignment)
        print("Select a house to assign a ration to using its ID")
        command = input("> ").lower()
        return command

    def rations(self) :
        print("Please select a ration using its ID: ")
        rations = self.ration_database.get_all_rations()
        print(("{:^3} | {:^15} | {:^5} | {:^6} | {:^5} | {:^9} | {:^8} | {:^8} | {:^10} | {:^7}").format(
            "ID", "Name", "Wheat", "Barley", "Soya", "Limestone", "Soya Oil", "Arbocell", "Methionine", "Premix"
        ))
        print("{:-^103}".format(""))
        for ration in rations :
            self.print_row(ration)
        command = input("> ").lower()
        return command

    def settings(self) :
        print("Settings:")
        print("-Assign rations")
        print("-Add ration")
        print("-Edit ration")
        print("-Delete ration")
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

    def update_weights(self, weights, weight_limits) :
        update = (self.weights != weights)
        if update :
            self.weights = weights
            self.display_weights(weights, weight_limits)

    def message(self, message) :
        print(message)