from machine import Pin, PWM, I2C
import time, struct
import uasyncio as asyncio
import Servo
import Giotto

# class to drive the arm, all measurements in mm
# should probably make its own file eventually
class ArmDrive:
    def __init__(self,pinA,pinB,pinZ,lenA=60,lenB=60,minX=10):
        self.lenA = 60
        self.lenB = 60
        self.armA = Servo.PositionServo(pin_number=pinA)
        self.armB = Servo.PositionServo(pin_number=pinB)
        self.armZ = Servo.PositionServo(pin_number=pinZ)
        self.giotto = Giotto.Giotto(self.lenA,self.lenB,mode="high")
        self.minX = 10
        self.homeX = 50
        self.homeY = 50
        self.homeT = 180
        self.workX = 50
        self.workY = 50
        self.workT = 0
    
    # function to precisely move the arm
    def move(self,x,y,theta):
        # check that location is in bounds
        if x < self.minX:
            x = self.minX:
        
        # solve for angles
        try:
            [angA,angB] = self.giotto.solve(x,y)
            
            # update servos
            # BUG !!! probably need to adjust angles according to servo mins and maxes
            # aka ensure that angle 0 is equal to base axis
            armA.set_position(angA)
            armB.set_position(angB)
            armZ.set_position(theta)

            return 100
        except Exception as e:
            print(e)
            return 101
        
    # function to efficiently put the arm into home position 
    def goHome():
        self.move(self.homeX,self.homeY,self.homeT)
        
    # function to efficiently put the arm into working position 
    def goForward():
        self.move(self.workX,self.workY,self.workT)
        
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
theArm.move(60,0,0)
