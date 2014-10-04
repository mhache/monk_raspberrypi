#!/usr/bin/python
# 10_01_clock.py

import i2c7segment as display
import time
"""
The 'print_int()' as found in the 'i2c7segment' module does not display leading zeros which are required for a clock display. 
As well, it does not clear all digits prior to updating with the integer value, potentially leaving the display is an unintends state.

The 'write_time_digits(arg1, arg2)' was added to the 'i2c7segment' module to better address the display of time components.
arg1 and arg2 can be any two-digit time component, eg. year, month, day, hours, minutes, seconds
"""

disp = display.Adafruit7Segment()

while True:
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
