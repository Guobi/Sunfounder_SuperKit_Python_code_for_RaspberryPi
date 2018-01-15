#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPinRed = 11
LedPinYellow = 13
LedPinGreen = 15

GreenTime = 10
YellowTime = 3
RedTime = 10

def getColorFromPin(pin):
	color = ""
	if (pin == LedPinGreen):
		color = "Green"
	elif (pin == LedPinYellow):
		color = "Yellow"
	elif (pin == LedPinRed):
		color = "Red"
	return color

def signalOn(pin, numberOfSeconds):
	color = getColorFromPin(pin)
	print('Light {0} for {1} seconds'.format(color, numberOfSeconds))
	GPIO.output(pin, GPIO.LOW)
	time.sleep(numberOfSeconds)
	GPIO.output(pin, GPIO.HIGH)
	return

def flashLight(pin, times):
	color = getColorFromPin(pin)
	print('Flash {0} for {1} times'.format(color, times))
	for x in range(1, times+1):
		time.sleep(0.5)
		print(x)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(pin, GPIO.HIGH)

def setup():
	# Numbers GPIOs by physical location
	GPIO.setmode(GPIO.BOARD)

	# Set LedPin's mode is output
	GPIO.setup(LedPinRed, GPIO.OUT)
	GPIO.setup(LedPinYellow, GPIO.OUT)
	GPIO.setup(LedPinGreen, GPIO.OUT)

	# Set LedPin high(+3.3V) to off led
	GPIO.output(LedPinRed, GPIO.HIGH)
	GPIO.output(LedPinYellow, GPIO.HIGH)
	GPIO.output(LedPinGreen, GPIO.HIGH)

def loop():
	while True:
		signalOn(LedPinGreen, GreenTime)
		flashLight(LedPinGreen, 3)
		flashLight(LedPinYellow, 3)
		signalOn(LedPinRed, RedTime)
		flashLight(LedPinRed, 3)

def destroy():
	GPIO.output(LedPinRed, GPIO.HIGH)
	GPIO.output(LedPinYellow, GPIO.HIGH)
	GPIO.output(LedPinGreen, GPIO.HIGH)
		
	GPIO.cleanup()

# Program start from here
if __name__ == '__main__':
	setup()
	try:
		loop()
	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
	except KeyboardInterrupt:
		destroy()