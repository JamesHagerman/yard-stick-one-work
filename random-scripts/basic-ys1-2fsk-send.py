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

PKTLEN = 1 #0b11110000    # Set number of payload bytes per packet (including optional address byte)
# DRATE = 101 # Baudrate of 256 means SLOOOOW
DRATE = 1000 # Baudrate in symbols per second.
             #1000 means 1ms pulse as a single bit
             # 25 dies. 75 dies. 100 dies. 101 is as low as I can
try:
    d = RfCat()
    d.setModeIDLE() # atlas used three different inflections in his talks...
    d.setFreq(FREQ)
    d.setMdmModulation(MOD_2FSK) # Lower side band?
    # d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDeviatn(DEVIATION)
    d.makePktFLEN(PKTLEN) # Fixed packet mode... PKTLEN is length of actual packet and is put into the packet structure.
    # d.makePktVLEN() # Variable Packet Mode = we have to define packet length ourselves... PKTLEN becomes maximum packet receive length
    d.setMdmDRate(DRATE)

    # Append RSSI and LQI and CRC OK if this is set to 1:
    # d.setEnablePktAppendStatus(0) # 1 = append, 0 = don't append

    # weird preamble insert: 010011000

    # Configure some preamble and sync word stuff:
    # Preamble is usually alternating symbols: 0b1010101010101010 
    # Syncword is a unique "start of frame" word that is usually non-repeating
    #   BTW, sometimes, the syncword is configured to repeat...
    # The CC1110/CC1111 can't be configured to do one or the other. It has to
    # send both. And it has to send both, twice at a minimum
    # d.setPktPQT(0) # Set Preamble Quality Threshold to zero (disable it entirely) Register is: PKTCTRL1
    d.setMdmSyncWord(0b1110101010101010) # Use Syncword as an extended preamble Registers are SYNC1 and SYNC0
    d.setMdmSyncMode(0b1) # 1 = enable preamble and syncword. Docs explaining this: Page 216 of 246 in PDF. Register is: MDMCFG2.SYNC_MODE
    d.setMdmNumPreamble(0b0) # Set number of preamble bits to transmit. 0b000 = 2 bytes. Register MDMCFG1.NUM_PREAMBLE
    d.setEnablePktCRC(0) # disable the crc calculation

    # Damnit, rfcat doesn't expose methods to control the address of this thing...
    # radiocfg = d.getRadioConfig()
    # modifiedcfg = radiocfg & somebit that controls address....
    # d.setRFRegister(PKTCTRL1, modifiedcfg)

    #d.setMaxPower()    # Pretty sure this turns on the TX amp
    # d.setModeTX()       # It's good to enter the right mode first...

    # Variable packet length = first byte has to describe LENGTH OF THE PACKET!
    # 4 byte payload = first byte is:
    # U = 0b01010101 = 0x55
    # x = 0b01111000 = 0x78
    # bytes = [0x21, 0x78] # Data to send
    # bytes = [4, 0x78, 0x55, 0x41, 0xff] # Data to send
    bytes = [0x78, 0x55] # Data to send

    # Both of these methods have been tested and work correctly:
    print("".join(map(chr, bytes)))
    # d.RFxmit("".join(map(chr, bytes)))
    d.RFxmit('xUUx')


    # WITHOUT THIS YOU WILL GET USB TIMEOUTS!
    d.setModeIDLE()  # DO THIS OR GET USB TIMEOUTS!
except Exception, e: # Make sure things are sane...
    d.setModeIDLE()  # Probably a good idea here too... just in case
    sys.exit("Error %s" % str(e))
