from machine import Pin, PWM, I2C
import time, struct
import uasyncio as asyncio
import Servo
import Giotto

giotto = Giotto.Giotto(1,1)

armA = Servo.PositionServo(pin_number=12)
armB = Servo.PositionServo(pin_number=13)
armZ = Servo.PositionServo(pin_number=14)

angle = 0

# class to drive the arm, all measurements in mm
# should probably make its own file eventually
class theArm:
    def __init__(self,lenA=60,lenB=60,minX=10):
        self.lenA = 60
        self.lenB = 60
        self.armA = Servo.PositionServo(pin_number=12)
        self.armB = Servo.PositionServo(pin_number=13)
        self.armZ = Servo.PositionServo(pin_number=14)
        self.giotto = Giotto.Giotto(self.lenA,self.lenB,mode="high")
        self.minX = 10
        self.fast = False
    
    # function to precisely move the arm
    def move(self,x,y,theta):
        # check that location is in bounds
        # WRITE HERE
        
        # solve for angles
        [angA,angB] = self.giotto.solve(x,y)
        
        # update servos
        # BUG !!! probably need to adjust angles according to servo mins and maxes
        armA.set_position(angA)
        armB.set_position(angB)
        armZ.set_position(theta)
        
    # function to efficiently put the arm into home position 
    def goHome():
        
        
    # function to efficiently put the arm into working position 
    def goForward():

