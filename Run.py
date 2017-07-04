
import time
from Controller import *
from MotorController import *
from WeightInput import *

def main() :
    pins = { 0 : 22 }
    motor_controller = LEDMotorController(pins)
    wii_board = WiiBoard()
    controller = Controller(motor_controller, wii_board)

    while True :
        if wii_board.get_weight() < 20 :
            motor_controller.turn_on_motor(0)
        else :
            motor_controller.turn_off_motor(0)

if __name__ == "__main__":
    main()
