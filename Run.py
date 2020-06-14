import RPi.GPIO as GPIO

from Controller import *
from Display import *
from DatabaseManagement import *

def main():

    ration_database = DatabaseManager("rations.db")
    display = GUIDisplay(ration_database)
    controller = Controller(display, ration_database)

    on = True

    while (on):

        command = display.menu()

        if (command == "run"):

            success = False
            while not (success):
                house_id = display.assignments()
                if (house_id == "back" or house_id == "Back"):
                    break
                if (house_id.isdigit()):
                    if (int(house_id) > ration_database.get_max_house_id()):
                        display.message("Sorry, that's not an option, try again")
                    else:
                        end_weights, weight_limits = controller.run(house_id)
                        display.end(end_weights, weight_limits)
                        success = True
                else:
                    display.message("Sorry, that's not an option, try again")

        elif (command == "settings"):
            settings = True
            while (settings):
                invalid_input = True
                while (invalid_input):
                    choice = display.settings()
                    invalid_input = False
                    if (choice == "assign rations"):
                        controller.assign_rations()
                    elif (choice == "add ration"):
                        controller.add_ration()
                    elif (choice == "edit ration"):
                        controller.edit_ration()
                    elif (choice == "delete ration"):
                        controller.delete_ration()
                    elif (choice == "change batch"):
                        controller.change_batch()
                    elif (choice == "back"):
                        settings = False
                    else:
                        invalid_input = True
        elif (command == "shutdown"):
            os.system('shutdown now -h')

            # controller.run("Test")


if __name__ == "__main__":
    try:
        main()
    except:
        raise
    finally:
        GPIO.cleanup()
