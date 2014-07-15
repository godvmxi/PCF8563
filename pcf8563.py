#!/usr/bin/python
# FIlename: geoLapse.py

'''
Created on 5th July 2014

@author: rmamba@gmail.com
'''

import os
import sys
import smbus

import datetime
import time

import ntplib

if __name__ == "__main__":
	pcf8563 = smbus.SMBus(1)
	DEVICE_ADDRESS = 0x51
	
	clk = pcf8563.read_i2c_block_data(DEVICE_ADDRESS, 0x02, 7)
	Y = (clk[6] / 16) * 10 + (clk[6] & 0x0F) + 2000
	M = ((clk[5] & 0x10) / 16) * 10 + (clk[5] & 0x0F)
	D = ((clk[3] & 0x30) / 16) * 10 + (clk[3] & 0x0F)
	h = ((clk[2] & 0x30) / 16) * 10 + (clk[2] & 0x0F)
	m = ((clk[1] & 0x70) / 16) * 10 + (clk[1] & 0x0F)
	s = ((clk[0] & 0x70) / 16) * 10 + (clk[0] & 0x0F)
	
	try:
		pcf = datetime.datetime(Y, M, D, h, m, s, 0 , None)
	except:
		pcf = None
		print "Error converting to datetime [%s, %s, %s, %s, %s, %s]!" % (Y, M, D, h, m, s)
	
	if len(sys.argv)>1:
		if sys.argv[1] == 'ntp':
			ntpc = ntplib.NTPClient()
			ntpr = ntpc.request('europe.pool.ntp.org', version=3)
			dt = datetime.datetime.strptime(time.ctime(ntpr.tx_time), "%a %b %d %H:%M:%S %Y")
			print "PCF8563: ", pcf
			print "    NTP: ", dt
			tmp = dt.year % 100
			Y = (tmp / 10) * 16 + tmp % 10
			M = (dt.month / 10) * 16 + dt.month % 10
			D = (dt.day / 10) * 16 + dt.day % 10
			WD = dt.isoweekday()
			h = (dt.hour / 10) * 16 + dt.hour % 10
			m = (dt.minute / 10) * 16 + dt.minute % 10
			s = (dt.second / 10) * 16 + dt.second % 10
			pcf8563.write_i2c_block_data(DEVICE_ADDRESS, 0x02, [s, m, h, D, WD, M, Y])
		elif sys.argv[1] == 'print':
			if pcf:
				print pcf.strftime('%m%d%H%M%Y.%S')
		else:
			if pcf:
				print pcf
	else:
		if pcf:
			print pcf.strftime('%a %b %d %H:%M:%S UTC %Y')
		else:
			print clk
