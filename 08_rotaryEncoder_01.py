#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RoAPin = 11    # pin11
RoBPin = 12    # pin12
RoSPin = 13    # pin13
LedPin = 7

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.LOW)  # Set LedPin to low(0V)
	p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
	p.start(0)
	rotaryClear()

def rotaryDeal():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalCounter
	Last_RoB_Status = GPIO.input(RoBPin)
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalCounter = globalCounter + 1
			print 'globalCounter = %d' % globalCounter
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalCounter = globalCounter - 1
			print 'globalCounter = %d' % globalCounter

def clear(ev=None):
        globalCounter = 0
	print 'globalCounter = %d' % globalCounter
	time.sleep(1)

def rotaryClear():
        GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling


def loop():
	global globalCounter
	p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
	p.start(0)
	while True:
		if globalCounter <= 0:
			globalCounter = globalCounter + 1
		else:
			if globalCounter >= 100:
				globalCounter = globalCounter - 1
			else:
				rotaryDeal()
				p.ChangeDutyCycle(globalCounter)     # Change duty cycle


def destroy():
	GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

