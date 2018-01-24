#!/usr/bin/python2.7
#
# This script is supposed to work correctly with the "working-2fsk-frontend.grc"
# GNU Radio Companion flow found here:
# https://github.com/JamesHagerman/grc-flow-work/tree/master/basic-receivers
#
# This isn't done yet...
#
import sys
from rflib import *
# 434.3MHz - The middle of one of the two NoCal, 70cm, Experimental bands
FREQ = 434200000 # (BW = 0.6MHz = 600kHz) 433.60+(434.80-433.60)/2
#### Don't use this one for now... FREQ = 438500000 # (BW = 0.05MHz = 50kHz) 438.45+(438.55-438.45)/2
DEVIATION = 4500

# My car keyfob...
# FREQ = 313850000
# DEVIATION = 32500 # Calculated as half of distance between peaks in GQRX

PKTLEN = 8    # Set bytes per packet?
# DRATE = 256 # Baudrate of 256 means SLOOOOW
DRATE = 1000 # Baudrate of 1000 means 1ms pulse as a single bit
           # 25 dies. 75 dies. 100 dies. 256 is as low as I can
try:
    d = RfCat()
    d.setFreq(FREQ)
    d.setMdmModulation(MOD_2FSK) # Lower side band?
    # d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDeviatn(DEVIATION)
    d.makePktFLEN(PKTLEN)
    d.setMdmDRate(DRATE)

    # Configure some preamble and sync word stuff:
    # Preamble is usually alternating symbols, 01010101 or whatever
    # Syncword is a unique "start of frame" word that is usually non-repeating
    #   BTW, sometimes, the synword is configured to repeat...
    d.setPktPQT(1) # Set Preamble Quality Threshold to zero (disable it entirely) Register is: PKTCTRL1
    d.setMdmSyncWord(0b1111111111111111) # Registers are SYNC1 and SYNC0
    d.setMdmSyncMode(0b0) # Docs explaining this: Page 216 of 246 in PDF. Register is: MDMCFG2
    # d.setMdmNumPreamble(4) # Set number of preamble bits to transmit. Register MDMCFG1
    #d.setMaxPower()    # Pretty sure this turns on the TX amp
    bytes = [0, 0x41, 0xff] # Data to send
    d.setModeTX()       # It's good to enter the right mode first...
    # d.RFxmit("".join(map(chr, bytes)))
    d.RFxmit('KM6IDA, Sorry for the noise')

    # WITHOUT THIS YOU WILL GET USB TIMEOUTS!
    d.setModeIDLE()  # DO THIS OR GET USB TIMEOUTS!
except Exception, e: # Make sure things are sane...
    d.setModeIDLE()  # Probably a good idea here too... just in case
    sys.exit("Error %s" % str(e))
