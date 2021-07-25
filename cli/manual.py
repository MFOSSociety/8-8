import time
import sys
sys.path.append("..") # Add higher directory to python modules path
from drivers.motor1 import rotatemotor as rotateY
from drivers.motor2 import rotatemotor as rotateX
from drivers.ElectroMagnet import toggleMagnet


motorcurentx = 0
motorcurenty = 0

xscale = 5
yscale = 5

half_square = 1

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
    #rotateX(half_square)

def moveToNewPos(x1,y1,x2,y2):
    moveY(y1,y2)
    moveX(x1,x2)
    print("current position "+str(x2) +" "+str(y2))
    print("dropping the piece moving towards zero")
    #rotateX(-1*half_square)
    toggleMagnet(False)
    moveMotortozero(x2,y2)

def moveMotortozero(x,y):
    moveY(y,0)
    moveX(x,0)
    print("finally at zero")

def convertMove():
    print("inside the motor")
    x1 = int(input())
    y1 = int(input())
    x2 = int(input())
    y2 = int(input())
    print("current position 0,0")
    moveToOldPos(x1,y1)
    moveToNewPos(x1,y1,x2,y2)
    ch = input()

convertMove()
