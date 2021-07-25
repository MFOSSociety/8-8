import RPi.GPIO as GPIO
import time

in3 = 36
in2 = 32
in1 = 22
in4 = 38

out1 = in2
out2 = in3
out3 = in1
out4 = in4

i = 0
positive = 0
negative = 0
y = 0
slp = 0.001

enb=40
ena=18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(enb, GPIO.OUT)
GPIO.output(enb, GPIO.HIGH)
GPIO.setup(ena, GPIO.OUT)
GPIO.output(ena, GPIO.HIGH)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)




nstep=20
def rotate(dir):
    i = 0
    positive = 0
    negative = 0
    y = 0
    slp = 0.001
    x = 400 * dir
    if x > 0 and x <= 400:
        for y in range(x, 0, -1):
            if negative == 1:
                if i == 7:
                    i = 0
                else:
                    i = i + 1
                y = y + 2
                negative = 0
            positive = 1

            # print((x+1)-y)

            if i == 0:
                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 1:

                # time.sleep(1)

                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 2:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 3:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 4:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 5:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)
            elif i == 6:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)
            elif i == 7:

                # time.sleep(1)

                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)

                # time.sleep(1)

            if i == 7:
                i = 0
                continue
            i = i + 1
    elif x < 0 and x >= -400:

        x = x * -1
        for y in range(x, 0, -1):
            if positive == 1:
                if i == 0:
                    i = 7
                else:
                    i = i - 1
                y = y + 3
                positive = 0
            negative = 1

            # print((x+1)-y)

            if i == 0:
                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 1:

                # time.sleep(1)

                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 2:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 3:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.HIGH)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 4:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.LOW)
                time.sleep(slp)
            elif i == 5:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.HIGH)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)
            elif i == 6:

                # time.sleep(1)

                GPIO.output(out1, GPIO.LOW)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)
            elif i == 7:

                # time.sleep(1)

                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                GPIO.output(out3, GPIO.LOW)
                GPIO.output(out4, GPIO.HIGH)
                time.sleep(slp)

                # time.sleep(1)

            if i == 0:
                i = 7
                continue
            i = i - 1


def rotatemotor(x):
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)
    dir = 1
    if x < 0:
        dir = -1
        x = x * -1
    for i in range(x):
        rotate(dir)


# try:
#     while 1:

#         # GPIO.output(out1, GPIO.LOW)
#         # GPIO.output(out2, GPIO.LOW)
#         # GPIO.output(out3, GPIO.LOW)
#         # GPIO.output(out4, GPIO.LOW)

#         x = input()
#         rotatemotor(x)
# except KeyboardInterrupt:

#     GPIO.cleanup()


def initializemotor1():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(enb, GPIO.OUT)
    GPIO.output(enb, GPIO.HIGH)
    GPIO.setup(ena, GPIO.OUT)
    GPIO.output(ena, GPIO.HIGH)
    GPIO.setup(out1, GPIO.OUT)
    GPIO.setup(out2, GPIO.OUT)
    GPIO.setup(out3, GPIO.OUT)
    GPIO.setup(out4, GPIO.OUT)

