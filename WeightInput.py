
from abc import ABCMeta, abstractmethod

class WeightInput(metaclass = ABCMeta) :

    def __init__(self, weight = 0) :
        self.weight = weight

    @abstractmethod
    def get_weight(self) :
        pass
        #TODO: Get weight here


class WiiBoard(WeightInput) :

    def get_weight(self) :
        pass
        #TODO: Get weight here

class PulseInput(WeightInput) :
    
    def get_weight(self):
        pass
        # TODO: Get weight here