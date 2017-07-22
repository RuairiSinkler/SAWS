import RPi.GPIO as GPIO
from Controller import *
from Display import *
from DatabaseManagement import *

def main() :

    ration_database = DatabaseManager("rations.db")
    display = ConsoleDisplay(ration_database)
    controller = Controller(display, ration_database)

    command = display.menu()

    if (command == "run") :
        ration = display.display_rations()

        success = False

        while not(success) :
            try :
                controller.run(ration)
                success = True
            except IndexError :
                print("Sorry, that's not an option, try again")
                ration = display.display_rations()

    #controller.run("Test")

if __name__ == "__main__":
    try :
        main()
    except :
        raise
    finally :
        GPIO.cleanup()