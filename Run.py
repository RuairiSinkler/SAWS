import RPi.GPIO as GPIO
from Controller import *
from Display import *

def main() :

    try :
        display = ConsoleDisplay()

        controller = Controller(display)

        controller.run("Test")
    except :
        print("Error")
    finally :
        GPIO.cleanup()

if __name__ == "__main__":
    main()
