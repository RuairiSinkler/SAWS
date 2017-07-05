
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

    def __init__(self, weight_pins, weight = 0) :
        self.wb_weight = weight
        self.sl_weight = weight
        self.pins = weight_pins
        self.wb_pin = self.pins["Wheat/Barley"]
        self.sl_pin = self.pins["Soya/Limestone"]
        for key in self.pins :
            GPIO.setup(self.pins[key], GPIO.IN)

        self.old_wb_status = GPIO.input(self.wb_pin)
        self.old_sl_status = GPIO.input(self.sl_pin)



    def get_weights(self) :
        wb_status = GPIO.input(self.wb_pin)
        if self.old_wb_status != wb_status:
            if wb_status == False:
                self.wb_weight += 10
            self.old_wb_status = wb_status

        sl_status = GPIO.input(self.sl_pin)
        if self.old_sl_status != sl_status:
            if sl_status == False:
                self.sl_weight += 10
            self.old_sl_status = sl_status

        return self.wb_weight, self.sl_weight

    def set_wb_weight(self, weight) :
        self.wb_weight = weight

    def set_sl_weight(self, weight) :
        self.sl_weight = weight
