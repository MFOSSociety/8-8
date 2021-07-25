from .motor1 import rotatemotor as rotateY
from .motor2 import rotatemotor as rotateX
from .ElectroMagnet import toggleMagnet
import time

motorcurentx = 0
motorcurenty = 0

xscale = 5
yscale = 5

half_square = 2


def moveMotor(move):
    convertMove(move)

def trackInitial(x2,y2):
	moveY(y2,0)
	moveX(x2,0)

def moveX(x1, x2):
    dx = x2-x1
    rotateX(dx*xscale)

def moveY(y1, y2):
    dy = y2-y1
    rotateY(-1*dy*yscale)


def moveToOldPos(x1, y1):
    moveY(0,y1)
    moveX(0,x1)
    print("current position "+str(x1) +" "+str(y1))
    print("picking the peice up")
    toggleMagnet(True)
    rotateX(-1*half_square)
    rotateY(1*half_square)

def moveToNewPos(x1,y1,x2,y2):
    moveY(y1,y2)
    moveX(x1,x2)
    print("current position "+str(x2) +" "+str(y2))
    print("dropping the piece moving towards zero")
    rotateX(1*half_square)
    rotateY(-1*half_square)
    toggleMagnet(False)
    moveMotortozero(x2,y2)

def moveMotortozero(x,y):
    moveY(y,0)
    moveX(x,0)
    print("finally at zero")

def convertMove(move):
    print("inside the motor")
    x1 = move.oldPos[0]
    y1 = move.oldPos[1]
    x2 = move.newPos[0]
    y2 = move.newPos[1]
    x1 = abs(7-x1)
    y1 = abs(7-y1)
    x2 = abs(7-x2)
    y2 = abs(7-y2)
    print("("+str(x1)+","+str(y1)+") ("+str(x2)+","+str(y2)+")")
    print("current position 0,0")
    moveToOldPos(x1,y1)
    moveToNewPos(x1,y1,x2,y2)

