
import RPi.GPIO as GPIO
from abc import ABC, abstractmethod

class MotorController(ABC) :

    def __init__(self, pin_numbers) :
        self.pin_numbers = pin_numbers

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

    def turn_on_motor(self, motor_number) :
        #print("Turning on LED")
        #print(self.pin_numbers[motor_number])
        GPIO.output(self.pin_numbers[motor_number], True)

    def turn_off_motor(self, motor_number) :
        #print("Turning off LED")
        #print(self.pin_numbers[motor_number])
        GPIO.output(self.pin_numbers[motor_number], False)
