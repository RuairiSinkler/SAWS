
from MotorController import *
from WeightInput import *

class Controller :

    def __init__(self, display, ration_database) :
        self.display = display
        self.motor_pins = {0: 16, 1: 13, 2: 19, 3: 26}
        self.weight_pins = {"wheat": 20, "barley": 20, "soya": 21, "limestone": 21}

        self.motor_controller = LEDMotorController(self.motor_pins)
        self.ration_database = ration_database

        self.setup()

    def setup(self) :
        GPIO.setmode(GPIO.BCM)

        for key in self.motor_pins :
            GPIO.setup(self.motor_pins[key], GPIO.OUT)
        for key in self.weight_pins :
            GPIO.setup(self.weight_pins[key], GPIO.IN)

    def setup_ration(self, ration) :
        result = self.ration_database.get_ration(ration)
        return result[2], result[3], result[4], result[5]

    def run(self, ration) :

        wheat_limit, barley_limit, soya_limit, limestone_limit = self.setup_ration(ration)
        weight_limits = [wheat_limit, barley_limit, soya_limit, limestone_limit]

        self.wheat_input = PulseInput(self.weight_pins["wheat"])
        self.soya_input = PulseInput(self.weight_pins["soya"])
        self.barley_input = None
        self.limestone_input = None

        complete = False
        wheat = True
        soya = True

        wheat_weight = 0
        barley_weight = 0
        soya_weight = 0
        limestone_weight = 0

        wb_done = False
        sl_done = False

        self.display.setup_weights()

        while not (complete):

            if wheat:
                wheat_weight = self.wheat_input.get_weight()
            else:
                barley_weight = self.barley_input.get_weight()
            if soya:
                soya_weight = self.soya_input.get_weight()
            else:
                limestone_weight = self.limestone_input.get_weight()

            self.display.update_weights([wheat_weight, barley_weight, soya_weight, limestone_weight], weight_limits)

            if not(wb_done) :
                if wheat :
                    if wheat_weight < wheat_limit:
                        self.motor_controller.turn_on_motor(0)
                    else:
                        self.motor_controller.turn_off_motor(0)
                        self.barley_input = PulseInput(self.weight_pins["barley"])
                        wheat = False
                else:
                    if barley_weight < barley_limit:
                        self.motor_controller.turn_on_motor(1)
                    else:
                        self.motor_controller.turn_off_motor(1)
                        wb_done = True

            if not(sl_done) :
                if soya:
                    if soya_weight < soya_limit:
                        self.motor_controller.turn_on_motor(2)
                    else:
                        self.motor_controller.turn_off_motor(2)
                        self.limestone_input = PulseInput(self.weight_pins["limestone"])
                        soya = False
                else:
                    if limestone_weight < limestone_limit:
                        self.motor_controller.turn_on_motor(3)
                    else:
                        self.motor_controller.turn_off_motor(3)
                        sl_done = True
                        
            complete = wb_done and sl_done
            time.sleep(0.02)
        end_weights = [wheat_weight, barley_weight, soya_weight, limestone_weight]
        weight_limits = [wheat_limit, barley_limit, soya_limit, limestone_limit]
        return end_weights, weight_limits

    def assign_rations(self) :
        self.display.assignments()

    def add_ration(self) :
        pass

    def edit_ration(self) :
        pass

    def delete_ration(self) :
        pass