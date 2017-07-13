
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
    def display_rations(self) :
        pass

    @abstractmethod
    def update_weights(self, weights) :
        pass

class ConsoleDisplay(Display) :

    def menu(self) :
        print("Welcome to ASWA (Automatic Sinkler Weighing System)")
        print("Main Menu:")
        print("Run")
        command = input("Please type in a command from the above menu: ").lower()
        if(command == "run") :
            print("Please select a ration:")
            self.display_rations()

    def display_rations(self) :
        rations = self.ration_database.get_all_rations()
        print(rations)


    def update_weights(self, weights, weight_limits) :
        update = (self.weights != weights)
        if update :
            self.weights = weights
            print(
                "Wheat weight: " + str(self.weights[0]) +
                "/" + str(weight_limits[0]) +
                " Barley weight: " + str(self.weights[1]) +
                "/" + str(weight_limits[1])
            )
            print(
                "Soya weight: " + str(self.weights[2]) +
                "/" + str(weight_limits[2]) +
                " Limestone weight: " + str(self.weights[3]) +
                "/" + str(weight_limits[3])
            )
