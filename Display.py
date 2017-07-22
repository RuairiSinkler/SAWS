
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
    def display_weights(self, weights, weight_limits) :
        pass

    @abstractmethod
    def update_weights(self, weights) :
        pass

class ConsoleDisplay(Display) :

    def menu(self) :
        print("Welcome to ASWA (Automatic Sinkler Weighing System)")
        print("Main Menu:")
        print("Run")
        print("Shutdown")

    def print_row(self, values) :
        print(("{v[1]:^15} | {v[2]:^5d} | {v[3]:^6d} | {v[4]:^5d} | {v[5]:^9d} | " +
            "{v[6]:^8d} | {v[7]:^8d} | {v[8]:^10d} | {v[9]:^7d}").format(v=values)
        )
        print("{:-^97}".format(""))

    def end(self, end_weights, weight_limits) :
        print("Run complete, end result:")
        self.display_weights(end_weights, weight_limits)


    def rations(self) :
        print("Please select a ration: ")
        rations = self.ration_database.get_all_rations()
        print(("{:^15} | {:^5} | {:^6} | {:^5} | {:^9} | {:^8} | {:^8} | {:^10} | {:^7}").format(
            "Name", "Wheat", "Barley", "Soya", "Limestone", "Soya Oil", "Arbocell", "Methionine", "Premix"
        ))
        print("{:-^97}".format(""))
        for ration in rations :
            self.print_row(ration)

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
