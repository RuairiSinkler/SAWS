import RPi.GPIO as GPIO
import os
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
            display.rations()
            ration = input("> ")

            success = False

            while not(success) :
                try :
                    end_weights, weight_limits = controller.run(ration)
                    display.end(end_weights, weight_limits)
                    success = True
                except IndexError :
                    print("Sorry, that's not an option, try again")
                    display.rations()
                    ration = input("> ")
        elif (command == "settings") :
            display.settings()
            invalid_input = True
            while(invalid_input) :
                choice = input("> ")
                invalid_input = False
                if (choice == "assign rations") :
                    controller.assign_rations()
                elif (choice == "add ration") :
                    controller.add_ration()
                elif (choice == "edit ration") :
                    controller.edit_ration()
                elif (choice == "delete ration") :
                    controller.delete_ration()
                elif (choice == "back") :
                    pass
                else :
                    invalid_input = True
        elif (command == "shutdown") :
            os.system('shutdown now -h')

        #controller.run("Test")

if __name__ == "__main__":
    try :
        main()
    except :
        raise
    finally :
        GPIO.cleanup()