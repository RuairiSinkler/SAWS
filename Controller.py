
from MotorController import *
from WeightInput import *

class Controller :

    def __init__(self) :
        self.motor_controller = None

        self.wheat_input = None
        self.barley_input = None
        self.soya_input = None
        self.limestone_input = None

    def setup(self) :
        GPIO.setmode(GPIO.BCM)
        motor_pins = {0: 16, 1: 13, 2: 19, 3: 26}
        weight_pins = {"wheat": 20, "barley": 20, "soya": 21, "limestone": 21}

        for key in motor_pins:
            GPIO.setup(motor_pins[key], GPIO.OUT)
        for key in weight_pins:
            GPIO.setup(weight_pins[key], GPIO.IN)

        self.motor_controller = LEDMotorController(motor_pins)
        self.wheat_input = PulseInput(weight_pins["wheat"])
        self.barley_input = PulseInput(weight_pins["barley"])
        self.soya_input = PulseInput(weight_pins["soya"])
        self.limestone_input = PulseInput(weight_pins["limestone"])

    def run(self) :
        complete = False
        wheat = True
        soya = True

        wheat_weight = 0
        barley_weight = 0
        soya_weight = 0
        limestone_weight = 0

        wb_done = False
        sl_done = False

        while not (complete):

            if wheat:
                wheat_weight = self.wheat_input.get_weight()
            else:
                barley_weight = self.barley_input.get_weight()
            if soya:
                soya_weight = self.soya_input.get_weight()
            else:
                limestone_weight = self.limestone_input.get_weight()

            print(
                "Wheat weight: " + str(wheat_weight) +
                " Barley weight: " + str(barley_weight) +
                " Soya weight: " + str(soya_weight) +
                " Limestone weight: " + str(limestone_weight)
            )

            if not(wb_done) :
                if wheat :
                    if wheat_weight < 50:
                        self.motor_controller.turn_on_motor(0)
                    else:
                        self.motor_controller.turn_off_motor(0)
                        wheat = False
                else:
                    if barley_weight < 50:
                        self.motor_controller.turn_on_motor(1)
                    else:
                        self.motor_controller.turn_off_motor(1)
                        wb_done = True

            if not(sl_done) :
                if soya:
                    if soya_weight < 50:
                        self.motor_controller.turn_on_motor(2)
                    else:
                        self.motor_controller.turn_off_motor(2)
                        soya = False
                else:
                    if limestone_weight < 50:
                        self.motor_controller.turn_on_motor(3)
                    else:
                        self.motor_controller.turn_off_motor(3)
                        sl_done = True
                        
            complete = wb_done and sl_done
            time.sleep(0.02)
