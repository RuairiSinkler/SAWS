
from abc import ABC, abstractmethod

class Display(ABC) :

    def __init__(self) :
        self.weights = [0, 0, 0, 0]
        pass

    @abstractmethod
    def menu(self) :
        pass

    @abstractmethod
    def run(self) :
        pass

    @abstractmethod
    def update_weights(self, weights) :
        pass

class ConsoleDisplay(Display) :

    def update_weights(self, weights, weight_limits) :
        update = (self.weights == weights)
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
