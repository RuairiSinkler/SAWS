import RPi.GPIO as GPIO
from Controller import *
from Display import *
from DatabaseManagement import *

def main() :

    try :
        display = ConsoleDisplay()
        ration_database = DatabaseManager("rations.db")
        controller = Controller(display, ration_database)

        controller.run("Test")
    except :
        print("Error")
    finally :
        GPIO.cleanup()

if __name__ == "__main__":
    main()
