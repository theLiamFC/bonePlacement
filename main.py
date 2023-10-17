from machine import Pin, PWM, I2C
import time, struct
import uasyncio as asyncio
import Servo
import Giotto

# class to drive the car, assumes 360 degree servos
class TankDrive:
    def __init__(self,leftPin,rightPin):
        self.leftM = Servo.ContinuousServo(pin_number=leftPin)
        self.rightM = Servo.ContinuousServo(pin_number=rightPin)
        self.pace = 1

    def move(self,joyY,joyX):
        leftMotor = (joyY - joyX) * self.pace
        rightMotor = -1 * (joyY + joyX) * self.pace
        
        leftM.set_speed(leftMotor)
        rightM.set_speed(rightMotor)

theArm = ArmDrive(pinA=12,pinB=13,pinZ=14,lenA=60,lenB=60,minX=10)
status = theArm.move(60,0,0)
print(status)
