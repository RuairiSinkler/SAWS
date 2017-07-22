import RPi.GPIO as GPIO
from Controller import *
from Display import *
from DatabaseManagement import *

def main() :

    ration_database = DatabaseManager("rations.db")
    display = ConsoleDisplay(ration_database)
    controller = Controller(display, ration_database)

    on = True

    while(on) :

        display.menu()
        command = input("Please type in a command from the above menu: ").lower()

        if (command == "run") :
            display.display_rations()
            ration = input("> ")

            success = False

            while not(success) :
                try :
                    end_weights, weight_limits = controller.run(ration)
                    display.display_end(end_weights, weight_limits)
                    success = True
                except IndexError :
                    print("Sorry, that's not an option, try again")
                    display.display_rations()
                    ration = input("> ")

        #controller.run("Test")

if __name__ == "__main__":
    try :
        main()
    except :
        raise
    finally :
        GPIO.cleanup()