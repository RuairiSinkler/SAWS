
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

    def print_row(self, values) :
        print(("{:^15{v[1]}} | {:^5d{v[2]}} | {:^6d{v[3]}} | {:^5d{v[4]}} | {:^9d{v[5]}} | " +
              "{:^8d{v[6]}} | {:^8d{v[7]}} | {:^10d{v[8]}} | ").format(v=values)#{:^7d{v[9]}}"
        )
        print("{:-^97}".format())

    def display_rations(self) :
        rations = self.ration_database.get_all_rations()
        print(("{:^15} | {:^5} | {:^6} | {:^5} | {:^9} | {:^8} | {:^8} | {:^10} | {:^7}").format(
            "Name", "Wheat", "Barley", "Soya", "Limestone", "Soya Oil", "Arbocell", "Methionine", "Premix"
        ))
        for ration in rations :
            self.print_row(ration)


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
