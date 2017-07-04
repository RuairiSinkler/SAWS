
import time
from Controller import *
from MotorController import *

def main() :
    pins = { 0 : 4 }
    motor_controller = LEDMotorController(pins)
    controller = Controller(motor_controller)

    controller.motor_controller.turn_on_motor(0)
    time.sleep(1)
    controller.motor_controller.turn_off_motor(0)
    GPIO.cleanup()

if __name__ == "__main__":
    main()