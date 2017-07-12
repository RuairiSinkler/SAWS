
from abc import ABC, abstractmethod

class Display(ABC) :

    @abstractmethod
    def __init__(self) :
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

    def __init__(self) :
        pass