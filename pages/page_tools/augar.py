import tkinter as tk
import RPi.GPIO as GPIO

class Augar:

    def __init__(self, parent, augar_pin, size):
        self.augar_pin = augar_pin
        self.canvas = tk.Canvas(parent, width=size, height=size)
        self.active = False
        GPIO.setup(augar_pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.augar_pin, True)
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="green")
        self.active = True

    def turn_off(self):
        GPIO.output(self.augar_pin, False)
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="red")
        self.active = False