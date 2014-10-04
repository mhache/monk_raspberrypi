#!/usr/bin/python
# 10_01_clock.py

import i2c7segment as display
import time

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
