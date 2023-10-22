from machine import Pin, PWM, I2C
import time, struct
import uasyncio as asyncio
import Servo
import Giotto
import ArmDrive
import BlueTooth as bt
import myWifi
import mqtt
import json

myWifi.connect(myWifi.TUFTS)

vacuum = Pin(21, Pin.OUT)
vacuum.on()
setLow = Servo.ContinuousServo(27)
setLow.set_speed(-40)

message = ""

# class to drive the car, assumes 360 degree servos
class TankDrive:
    def __init__(self,leftPin,rightPin):
        self.leftM = Servo.ContinuousServo(pin_number=leftPin)
        self.rightM = Servo.ContinuousServo(pin_number=rightPin)

    def move(self,joyY,joyX):
        leftMotor = 100 * (joyY - joyX)
        rightMotor = -100 * (joyY + joyX)
        
        self.leftM.set_speed(int(leftMotor-17))
        self.rightM.set_speed(int(rightMotor-17))
    
    #def surgeryMove(self,

def gotMessage(topic, msg):
    
    #print("recieved a message")
    #print((topic.decode(), msg.decode()))
    
    info = msg.decode()
    message = info.split(", ")
    inputDict = json.loads(info)
    print(inputDict)
    
    if inputDict['vac']:
        vacuum.on()
    else:
        vacuum.off()
        
    theCar.move(inputDict['leftJoyY'],inputDict['leftJoyX'])
    
        
theCar= TankDrive(26,27)
theArm = ArmDrive.ArmDrive(pinA=12,pinB=13,pinZ=14,pinR=15,lenA=100,lenB=100,minX=10)

try:
    fred = mqtt.MQTTClient('MyPico', 'broker.hivemq.com', keepalive=1000)
    print('Connected to MQTT')
    fred.connect()
    fred.set_callback(gotMessage)
except OSError as e:
    print('Failed')
    
fred.subscribe("theVacuum")

try:
    while True:
        fred.check_msg()
        time.sleep(0.05)
        #debug
        #testInput = input("Enter angles: A B Z\n").split(" ")
        #theArm.setAngles(int(testInput[0]),int(testInput[1]),int(testInput[2]))
        #testInput = input("Enter position: X Y Z R\n").split(" ")
        #print(theArm.move(int(testInput[0]),int(testInput[1]),int(testInput[2])))
        #theArm.armR.set_speed(int(testInput[3]))
except Exception as e:
    print(e)
finally:
    fred.disconnect()
