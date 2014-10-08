#!/usr/bin/python
# 10_02_fancy_clock.py

import i2c7segment as display
import time
import RPi.GPIO as io

"""
The 'print_int()' as found in the 'i2c7segment' module does not display leading zeros which are required for a clock display. 
As well, it does not clear all digits prior to updating with the integer value, potentially leaving the display is an unintends state.

The 'write_time_digits(arg1, arg2)' was added to the 'i2c7segment' module to better address the display of time components.
arg1 and arg2 can be any two-digit time component, eg. year, month, day, hours, minutes, seconds
"""

switch_pin=17
io.setmode(io.BCM)
io.setup(switch_pin, io.IN, pull_up_down=io.PUD_UP)
disp = display.Adafruit7Segment()

time_mode, seconds_mode, date_mode = range(3)
disp_mode = time_mode

def display_time():
	h = time.localtime().tm_hour
	m = time.localtime().tm_min
	
	#Original code
	#	disp.print_int(h * 100 + m)
	
	#Modified code
	disp.write_time_digits(h,m)

	disp.draw_colon(True)
	disp.write_display()
	time.sleep(0.5)
	disp.draw_colon(False)
	disp.write_display()
	time.sleep(0.5)

def display_date():
	d = time.localtime().tm_mday
	m = time.localtime().tm_mon
	
	#Original code
	#	disp.print_int(d * 100 + m) # World format
	#	disp.print_int(m * 100 + d) # US format
	
	#Modified code
	disp.write_time_digits(d,m) # World format
	#disp.write_time_digits(m,d) # US format

	disp.draw_colon(True)
	disp.write_display()
	time.sleep(0.5)

def display_seconds():
	s = time.localtime().tm_sec
	disp.print_str('----')
	
	#Original code
	#disp.print_int(s)

	#Modified code
	disp.write_digit_num(2,s//10)
	disp.write_digit_num(3,s%10)

	disp.draw_colon(True)
	disp.write_display()
	time.sleep(0.5)

while True:
	key_pressed = not io.input(switch_pin)
	if key_pressed:
		disp_mode = disp_mode + 1
		if disp_mode > date_mode:
			disp_mode = time_mode
	if disp_mode == time_mode:
		display_time()
	if disp_mode == seconds_mode:
		display_seconds()
	if disp_mode == date_mode:
		display_date()
