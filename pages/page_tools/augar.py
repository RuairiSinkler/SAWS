import RPi.GPIO as GPIO

class Augar:

    def __init__(self, augar_pin, canvas, canvas_size):
        self.augar_pin = augar_pin
        self.canvas = canvas
        self.canvas_size = canvas_size
        self.active = False
        GPIO.setup(augar_pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.augar_pin, True)
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="green")
        self.active = True

    def turn_off(self):
        GPIO.output(self.augar_pin, False)
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="red")
        self.active = False