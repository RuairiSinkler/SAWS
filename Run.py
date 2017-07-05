
import time
from Controller import *
from MotorController import *
from WeightInput import *

def main() :
    GPIO.setmode(GPIO.BCM)
    pins = { 0 : 16 , 1 : 13 , 2 : 19 , 3 : 26 }
    motor_controller = LEDMotorController(pins)
    weight_input = PulseInput(5)
    controller = Controller(motor_controller, weight_input)

    while True :
        weight = weight_input.get_weight()
        print(weight)
        if weight < 100 :
            for i in range(0, 3) :
                motor_controller.turn_on_motor(i)
        else :
            for i in range(0, 3):
                motor_controller.turn_off_motor(i)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
