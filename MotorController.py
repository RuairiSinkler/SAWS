
import RPi.GPIO as GPIO
from abc import ABCMeta, abstractmethod

class MotorController(metaclass = ABCMeta) :

    def __init__(self, pin_numbers) :
        self.pin_numbers = pin_numbers
        GPIO.setmode(GPIO.BCM)
        for key in pin_numbers :
            GPIO.setup(pin_numbers[key], GPIO.OUT)

    def get_pin(self, motor_number) :
        return self.pin_numbers[motor_number]

    @abstractmethod
    def turn_on_motor(self, motor_number) :
        pass
        #TODO: Turn on motor here

    @abstractmethod
    def turn_off_motor(self, motor_number) :
        pass
        #TODO: Turn off motor here

class LEDMotorController(MotorController) :

    def turn_on_motor(self, motor_number):
        GPIO.output(self.pin_numbers[motor_number], True)

    def turn_off_motor(self, motor_number):
        GPIO.output(self.pin_numbers[motor_number], False)