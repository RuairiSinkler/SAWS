import RPi.GPIO as GPIO

class Augar:

    def __init__(self, augar_pin, canvas):
        self.augar_pin = augar_pin
        self.canvas = canvas
        GPIO.setup(augar_pin, GPIO.OUT)

    def turn_on_augar(self):
        GPIO.output(self.augar_pin, True)

    def turn_off_augar(self):
        GPIO.output(self.augar_pin, False)