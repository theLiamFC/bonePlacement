from machine import Pin, PWM, I2C
import time, struct
import uasyncio as asyncio
import Servo
import Giotto
import ArmDrive
import BlueTooth as bt

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


theArm = ArmDrive.ArmDrive(pinA=12,pinB=13,pinZ=14,lenA=60,lenB=60,minX=10)

for i in range(20):
    print("trying bluetooth")
    try:   
        L = bt.Listen('aMilliaMilliaMilli')
        if L.connect_up(on_rx):
            time.sleep(5)
            L.write('heyo')
            time.sleep(5)
    except Exception as e:
        print(e)

finally:
    print('closing up')
    L.disconnect()
