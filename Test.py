import RPi.GPIO as GPIO
import tkinter as tk

class WeightInput():

    def __init__(self, weight_pin):
        self.pin = weight_pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda: print("button pressed"))
        # self.state = GPIO.input(self.pin)
        # self.check_input()

    # def check_input(self):
    #     oldstate = self.state
    #     newstate = GPIO.input(self.pin)
    #     if oldstate != newstate:
    #         self.state = newstate
    #         if newstate == GPIO.HIGH:
    #             self.parent.increment_value(self.weigher)
    #     self.controller.after(200, self.check_input)

def main():
    try:
        input1 = WeightInput(19)
        input2 = WeightInput(26)
        wait = input("Press enter to exit:")
    except:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except:
        raise
