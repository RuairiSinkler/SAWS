import RPi.GPIO as GPIO
from Controller import *
from Display import *
from DatabaseManagement import *

def main() :

    try :
        ration_database = DatabaseManager("rations.db")
        display = ConsoleDisplay(ration_database)
        controller = Controller(display, ration_database)

        command = display.menu()

        success = False

        while not(success) :
            try :
                controller.run(command)
                success = True
            except IndexError :
                print("Sorry, that's not an option, try again")
                command = display.display_rations()

        #controller.run("Test")
    except :
        print("Error")
        raise
    finally :
        GPIO.cleanup()

if __name__ == "__main__":
    main()
