
import RPi.GPIO as GPIO
from abc import ABCMeta, abstractmethod
from WiiBoard import *

class WeightInput(metaclass = ABCMeta) :

    def __init__(self, weight = 0) :
        self.weight = weight

    @abstractmethod
    def get_weight(self) :
        pass
        #TODO: Get weight here


class WiiBoard(WeightInput) :

    def __init__(self, weight = 0) :
        super().__init__(self, weight)
        processor = EventProcessor()

        self.board = WiiBoard(processor)
        if len(sys.argv) == 1:
            print
            "Discovering board..."
            address = self.board.discover()
        else:
            address = sys.argv[1]

        try:
            # Disconnect already-connected devices.
            # This is basically Linux black magic just to get the thing to work.
            subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
            subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
        except:
            pass

        print
        "Trying to connect..."
        self.board.connect(address)  # The wii board must be in sync mode at this time
        self.board.wait(200)
        # Flash the LED so we know we can step on.
        self.board.setLight(False)
        self.board.wait(500)
        self.board.setLight(True)

    def get_weight(self) :
        return self.board.recieve

class PulseInput(WeightInput) :

    def __init__(self, weight_pin, weight = 0) :
        self.weight = weight
        self.pin = weight_pin
        self.old_status = GPIO.input(self.pin)



    def get_weight(self) :
        status = GPIO.input(self.pin)
        if self.old_status != status:
            if status == False:
                print("up")
                self.weight += 10
            self.old_status = status

        return self.weight

    def setweight(self, weight) :
        self.weight = weight
