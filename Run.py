import RPi.GPIO as GPIO
from Controller import *
from Display import *
from DatabaseManagement import *

def main() :

    try :
        ration_database = DatabaseManager("rations.db")
        display = ConsoleDisplay(ration_database)
        controller = Controller(display, ration_database)

        display.menu()

        #controller.run("Test")
    except :
        print("Error")
        raise
    finally :
        GPIO.cleanup()

if __name__ == "__main__":
    main()
