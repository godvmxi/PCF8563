#!/usr/bin/python
# FIlename: geoLapse.py

'''
Created on 5th July 2014

@author: rmamba@gmail.com
'''

import os
import sys
import smbus

if __name__ == "__main__":
	pcf8563 = smbus.SMBus(1)
	DEVICE_ADDRESS = 0x51
	
	clk = pcf8563.read_i2c_block_data(DEVICE_ADDRESS, 0x02, 7)
	print clk
	Y = (clk[6] / 16) * 10 + (clk[6] & 0x0F) + 1900
	if Y < 50:
		Y = Y + 100
	M = ((clk[5] & 0x10) / 16) * 10 + (clk[5] & 0x0F)
	D = ((clk[3] & 0x30) / 16) * 10 + (clk[3] & 0x0F)
	h = ((clk[2] & 0x30) / 16) * 10 + (clk[2] & 0x0F)
	m = ((clk[1] & 0x70) / 16) * 10 + (clk[1] & 0x0F)
	s = ((clk[0] & 0x70) / 16) * 10 + (clk[0] & 0x0F)
	print "%s:%s:%s %s/%s/%s" % ( h, m, s, D, M, Y)
