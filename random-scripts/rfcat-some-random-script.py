#!/usr/bin/env python

import sys
import time
from rflib import *
from bitarray import bitarray

baudRate = 4800
freq = 433920000

dm_data = ""
rw_data = ""

def get_data():
	global rw_data
	#rw_data = "\xCC\xCD" + "This is some weird data!"

	# Generate some random data
	f = open('/dev/urandom', 'rb')
	rw_data = f.read(24)
	f.close()


def gen_manchester():
	global dm_data

	# Generate differential manchester code out of data bits
	rw_bits = bitarray()
	dm_bits = bitarray()

	rw_bits.frombytes(rw_data)
	dm_bit = True

	# Convert to differential manchester
	for bit in rw_bits:
		if bit == True: dm_bit = not dm_bit
		dm_bits.extend([dm_bit, not dm_bit])
	
	# Pause (guard time)
	dm_data = dm_bits.tobytes() + "\x00" * 4

	#print "RW: ", rw_bits
	#print "DM: ", dm_bits

def gen_morse():
	global dm_data

	# Generate PWM code out of the bits
	rw_bits = bitarray()
	dm_bits = bitarray()
	rw_bits.frombytes(rw_data)

	# Convert to morse
	for bit in rw_bits:
		dm_bits.extend([bit, False])

	# Pause (guard time)
	dm_data = dm_bits.tobytes() + "\x00" * 4

	#print "RW: ", rw_bits
	#print "DM: ", dm_bits


# Transmit the data!
d = RfCat()
d.setFreq(freq)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmSyncMode(0)
d.setMdmDRate(baudRate)
d.makePktFLEN(len(dm_data))

for x in range(0, 8):
	get_data()
	gen_morse()
	#print "Data length: ", len(dm_data)
	d.RFxmit(data=dm_data, repeat=8)

d.setModeIDLE()
