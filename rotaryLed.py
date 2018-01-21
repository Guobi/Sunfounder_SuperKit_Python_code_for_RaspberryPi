#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RoAPin = 11    # pin11
RoBPin = 12    # pin12
RoSPin = 13    # pin13

LedPinRed = 15
LedPinGreen = 16

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	rotaryClear()

	global pRed
	GPIO.setup(LedPinRed, GPIO.OUT)   # Set LedPinRed's mode is output
	GPIO.output(LedPinRed, GPIO.LOW)  # Set LedPinRed to low(0V)
	pRed = GPIO.PWM(LedPinRed, 1000)     # set Frequece to 1KHz
	pRed.start(0)                     # Duty Cycle = 0

	global pGreen
	GPIO.setup(LedPinGreen, GPIO.OUT)   # Set LedPinRed's mode is output
	GPIO.output(LedPinGreen, GPIO.LOW)  # Set LedPinRed to low(0V)
	pGreen = GPIO.PWM(LedPinGreen, 1000)     # set Frequece to 1KHz
	pGreen.start(0)

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
		if ((Last_RoB_Status == 1) and (Current_RoB_Status == 0)):
			globalCounter = globalCounter - 1
		if (globalCounter > 100):
			globalCounter = 100
		if (globalCounter < 0):
			globalCounter = 0
		print('globalCounter = {0}'.format(globalCounter))

def clear(ev=None):
	global globalCounter
	globalCounter = 0
	# print 'globalCounter = %d' % globalCounter
	print('Button pressed, reset globalCounter to {0}'.format(globalCounter))
	time.sleep(1)

def rotaryClear():
	GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling

def loop():
	global globalCounter
	while True:
		rotaryDeal()
		pRed.ChangeDutyCycle(globalCounter)
		pGreen.ChangeDutyCycle(100 - globalCounter)

def destroy():
	pRed.stop()
	GPIO.output(LedPinRed, GPIO.LOW)    # turn off all leds
	pGreen.stop()
	GPIO.output(LedPinRed, GPIO.LOW)    # turn off all leds
	GPIO.cleanup()
	
if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

