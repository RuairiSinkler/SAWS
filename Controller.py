
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

    def setup_ration(self, ration_id) :
        result = self.ration_database.get_ration(ration_id)
        return result[1], result[2], result[3], result[4], result[5]

    def run(self, ration_id) :

        ration_name, wheat_limit, barley_limit, soya_limit, limestone_limit = self.setup_ration(ration_id)
        weight_limits = [wheat_limit, barley_limit, soya_limit, limestone_limit]
        self.display.message("Ration {} running".format(ration_name))

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

        success = False
        cancel = False
        while not (success or cancel):
            house = self.display.assignments()
            if (house == "cancel"):
                cancel = True
                break
            if (house.isdigit()) :
                if (int(house) > self.ration_database.get_max_house_id()) :
                    self.display.message("Sorry, that's not an option, try again")
                else :
                    success = True
            else :
                self.display.message("Sorry, that's not an option, try again")

        success = False
        while not (success or cancel):
            ration = self.display.rations()
            if (ration == "cancel"):
                cancel = True
                break
            if (ration.isdigit()):
                if (int(ration) > self.ration_database.get_max_ration_id()):
                    self.display.message("Sorry, that's not an option, try again")
                else:
                    success = True
            else:
                self.display.message("Sorry, that's not an option, try again")

        if not (cancel) :
            self.ration_database.assign_ration(house, ration)

    def add_ration(self) :
        name = self.display.enter("name")
        wheat = self.display.enter("wheat")
        barley = self.display.enter("barley")
        soya = self.display.enter("soya")
        limestone = self.display.enter("limestone")
        soya_oil = self.display.enter("soya oil")
        arbocell = self.display.enter("arbocell")
        methionine = self.display.enter("methionine")
        premix = self.display.enter("premix")
        ration = [name, wheat, barley, soya, limestone, soya_oil, arbocell, methionine, premix]
        self.ration_database.insert_ration(ration)

    def edit_ration(self) :
        ration_id = self.display.rations()
        ration = self.ration_database.get_ration(ration_id)
        self.display.message("Leave any entries blank that you don't want to change: ")
        name = self.display.change("name", ration[1])
        wheat = self.display.change("wheat", ration[2])
        barley = self.display.change("barley", ration[3])
        soya = self.display.change("soya", ration[4])
        limestone = self.display.change("limestone", ration[5])
        soya_oil = self.display.change("soya oil", ration[6])
        arbocell = self.display.change("arbocell", ration[7])
        methionine = self.display.change("methionine", ration[8])
        premix = self.display.change("premix", ration[9])
        ration = [name, wheat, barley, soya, limestone, soya_oil, arbocell, methionine, premix]
        self.ration_database.insert_ration(ration)

    def delete_ration(self) :
        success = False
        cancel = False
        while not (success or cancel):
            ration = self.display.rations()
            if (ration == "cancel"):
                cancel = True
                break
            if (ration.isdigit()):
                if (int(ration) > self.ration_database.get_max_ration_id()):
                    self.display.message("Sorry, that's not an option, try again")
                else:
                    self.ration_database.delete_ration(ration)
                    success = True
            else:
                self.display.message("Sorry, that's not an option, try again")