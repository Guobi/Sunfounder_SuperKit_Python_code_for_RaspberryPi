#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPin7 = 7    # pin7
LedPin11 = 11  # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       		# Numbers GPIOs by physical location
	GPIO.setup(LedPin7, GPIO.OUT)   	# Set LedPin's mode is output
	GPIO.output(LedPin7, GPIO.HIGH) 	# Set LedPin high(+3.3V) to off led
	GPIO.setup(LedPin11, GPIO.OUT)   	# Set LedPin's mode is output
	GPIO.output(LedPin11, GPIO.HIGH) 	# Set LedPin high(+3.3V) to off led

def loop():
	while True:
		print('...led on')
		GPIO.output(LedPin7, GPIO.LOW)  	# led on
		GPIO.output(LedPin11, GPIO.HIGH)  	# led on
		time.sleep(0.5)
		print('led off...')
		GPIO.output(LedPin7, GPIO.HIGH) 	# led off
		GPIO.output(LedPin11, GPIO.LOW) 	# led off
		time.sleep(0.5)

def destroy():
	GPIO.output(LedPin7, GPIO.LOW)     	# led off
	GPIO.output(LedPin11, GPIO.HIGH)     	# led off
	GPIO.cleanup()                     		# Release resource

if __name__ == '__main__':     				# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  				# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

