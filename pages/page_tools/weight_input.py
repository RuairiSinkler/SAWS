import RPi.GPIO as GPIO

class WeightInput:

    def __init__(self, parent, controller, weigher, weight_pin):
        self.active = True
        self.controller = controller
        self.parent = parent
        self.weigher = weigher
        self.pin = weight_pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.state = GPIO.input(self.pin)
        self.check_input()

    def check_input(self):
        old_state = self.state
        new_state = GPIO.input(self.pin)
        if old_state != new_state:
            self.state = new_state
            if new_state == GPIO.HIGH:
                self.parent.increment_weight(self.weigher)
        if self.active:
            self.controller.after(200, self.check_input)