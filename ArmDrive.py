# ArmDrive.py

# class to drive a 2dof arm with rotating base

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
