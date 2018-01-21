#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from random import randint

# colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
colors = [0xeae733, 0xe107ed, 0x0000FF]

pins = {'pin_R':11, 'pin_G':12, 'pin_B':13}  # pins is a dict

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
for i in pins:
	GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
	GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 5000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xFF0000) >> 16
	G_val = (col & 0x00FF00) >> 8
	B_val = (col & 0x0000FF) >> 0
	
	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(G_val)
	p_B.ChangeDutyCycle(B_val)

try:
	while True:
		red = randint(0, 0xff) << 16
		print('Red color', format(red, '#02x'))

		green = randint(0, 0xff) << 8
		print('Green color', format(green, '#02x'))

		blue = randint(0, 0xff)
		print('Blue color', format(blue, '#02x'))

		rgb = red + green + blue
		print('RGB color', format(rgb, '#02x'))

		setColor(rgb)
		time.sleep(2)

		setColor(0)
		time.sleep(1)

		# for col in range(0, 0x100, 4):
		# 	print(col)
		# 	setColor(col)
		# 	time.sleep(0.05)
		# for col in range(0xff, -1, -4):
		# 	print(col)
		# 	setColor(col)
		# 	time.sleep(0.05)
		# for col in colors:
			# setColor(col)
			# time.sleep(0.5)
except KeyboardInterrupt:
	p_R.stop()
	p_G.stop()
	p_B.stop()
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
	GPIO.cleanup()

