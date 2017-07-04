
import time
from Controller import *
from MotorController import *
from WeightInput import *

def main() :
    GPIO.setmode(GPIO.BCM)
    pins = { 0 : 22 }
    motor_controller = LEDMotorController(pins)
    weight_input = PulseInput(5)
    controller = Controller(motor_controller, weight_input)

    while True :
        weight = weight_input.get_weight()
        print(weight)
        if weight < 100 :
            motor_controller.turn_on_motor(0)
        else :
            motor_controller.turn_off_motor(0)

if __name__ == "__main__":
    main()
