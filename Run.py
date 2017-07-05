
import time
from Controller import *
from MotorController import *
from WeightInput import *

def main() :
    GPIO.setmode(GPIO.BCM)
    motor_pins = { 0 : 16 , 1 : 13 , 2 : 19 , 3 : 26 }
    weight_pins = { "Wheat/Barley" : 20 , "Soya/Limestone" : 21}
    motor_controller = LEDMotorController(motor_pins)
    weight_input = PulseInput(weight_pins)
    controller = Controller(motor_controller, weight_input)

    complete = False
    wheat = True
    soya = True

    wheat_weight, barley_weight, soya_weight, limestone_weight = 0

    while not(complete) :
        wb_weight, sl_weight  = weight_input.get_weights()
        if wheat :
            wheat_weight = wb_weight
        else :
            barley_weight = wb_weight
        if soya :
            soya_weight = sl_weight
        else :
            limestone_weight = sl_weight

        print(
            "Wheat weight: " + wheat_weight +
            " Barley weight: " + barley_weight +
            " Soya weight: " + soya_weight +
            " Limestone weight: " + limestone_weight
        )

        if wheat :
            if wb_weight < 50 :
                motor_controller.turn_on_motor(0)
            else :
                motor_controller.turn_off_motor(0)
                weight_input.set_wb_weight(0)
                wheat = False
        else :
            if wb_weight < 50 :
                motor_controller.turn_on_motor(1)
            else :
                motor_controller.turn_off_motor(1)
                weight_input.set_wb_weight(0)
                wb_done = True
        if soya :
            if wb_weight < 50 :
                motor_controller.turn_on_motor(2)
            else :
                motor_controller.turn_off_motor(2)
                weight_input.set_sl_weight(0)
                soya = False
        else :
            if wb_weight < 50 :
                motor_controller.turn_on_motor(3)
            else :
                motor_controller.turn_off_motor(3)
                weight_input.set_sl_weight(0)
                sl_done = True
        complete = wb_done + sl_done
        time.sleep(0.02)

if __name__ == "__main__":
    main()
