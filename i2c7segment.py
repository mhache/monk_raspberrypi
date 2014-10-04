import smbus
import sys
"""
This is a library for using the Adafruit i2c 4 digit 7 segment LED displays
with i2c on a Raspberry Pi. It was built and tested on Raspbian Wheezy.

This is not an Adafruit product. 

To get i2c to work, you need Raspbian Wheezy or later and to do:
 sudo apt-get install python-smbus
 sudo apt-get install i2c-tools (usefull but not essential)
 sudo modprobe i2c-dev
 sudo modprobe i2c-bcm2708

Example Usage:
 
disp = Adafruit7Segment()
raw_input("print_int(65535, 16)")
disp.print_int(65535, 16)
disp.write_display()
raw_input("print_int(1234)")
disp.print_int(1234)
disp.write_display()
raw_input("print_str(----)")
disp.print_str('----')
disp.write_display()
raw_input("print_str(-12.3)")
disp.print_str('-12.3')
disp.write_display()

Simon Monk http://www.simonmonk.org Please give credit where credit is due.
 
"""

"""
This module originally written by Simon Monk, has been modified by 
Mark Hache, BSc(Comp Sci) UNB1992, 
contact:  mhache2416@gmail.com
"""

number_table = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71]

class Adafruit7Segment:

    def __init__(self, address=0x70):
        self.address = address
        #Original code
	#	self.bus = smbus.SMBus(0)
	#Modified code
	try:
        	self.bus = smbus.SMBus(0)
        except IOError:
		try:
			self.bus = smbus.SMBus(1)
		except IOError:
			print('Error occurred while setting up i2c bus.')
			print('Neither i2c0 nor i2c1 is available.')
			sys.exit()
        #End of modified code
	self.disp = [0, 0, 0, 0, 0] #digit1 digit2 digit3 digit4 colon
        self.bus.write_byte(address, 0x21)
        self.set_brightness(15)
        self.set_blink_rate(1)

    def set_brightness(self, brightness):
        """Set brightness 0 to 15"""
        self.bus.write_byte(self.address, 0xE0 | brightness)

    def set_blink_rate(self, blink):
        """Blink Rate 0, 1 or 2"""
        self.bus.write_byte(self.address, 0x80 | blink)

    def write_digit_raw(self, digit, bitmask):
        """ Write the LED segments for a digit directly dp g f e d c b a """
        self.disp[digit] = bitmask

    def write_digit_num(self, digit, number, dot=False):
        """ Write a number into a digit position optionally with a dot"""
        bitmask = number_table[number]
        if dot:
            bitmask = bitmask | 0x80
        self.write_digit_raw(digit, bitmask)

    def draw_colon(self, show_colon):
        """ Turn the colon in the middle on or off"""
        if show_colon:
            self.disp[4] = 0xFF
        else:
            self.disp[4] = 0x00

    def write_display(self):
        """ Refresh the display - nothing will appear until you call this"""
        self.bus.write_i2c_block_data(self.address, 0x00, [self.disp[0], 0x00, self.disp[1], 0x00, self.disp[4], 0x00, self.disp[2], 0x00, self.disp[3], 0x00])

    def print_int(self, n, base=10):
        """ Pint the integer, optionally with number base (2..16)"""
        i = 0
        while n > 0:
            self.write_digit_num(3-i, n % base, False)
            n = n / base
            i = i + 1

    def print_str(self, s):
        """
        Do the best you can with a 4 digit string (more with dots)
        this is how you deal with floats and signs etc
        format it first then print it
        unknown characters print as a space
        """
        digit_index = 0
        string_index = 0
        while string_index < len(s):
            ch = s[string_index]
            if ch == '-':
                self.write_digit_raw(digit_index, 0x40)
            elif ch >= '0' and ch <= '9':
                followed_by_dp = False
                if string_index < len(s)-1 and s[string_index+1] == '.':
                    followed_by_dp = True
                    string_index = string_index + 1
                self.write_digit_num(digit_index, int(ch), followed_by_dp)
            else:
                string_index = string_index + 1
            string_index = string_index + 1
            digit_index = digit_index + 1

#Newly added 'write_time_digits(arg1, arg2)'
    def write_time_digits(self,h_m,m_s):
	self.write_digit_raw(0,number_table[h_m//10])
	self.write_digit_raw(1,number_table[h_m%10])
	self.write_digit_raw(2,number_table[m_s//10])
	self.write_digit_raw(3,number_table[m_s%10])
