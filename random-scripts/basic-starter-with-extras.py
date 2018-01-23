#!/usr/bin/python2.7

# pylint: disable=W0614

import sys
from rflib import *

# In Middle of a NoCal Experimental bands
FREQ = 434200000 # (BW = 0.6MHz = 600kHz) 433.60+(434.80-433.60)/2
# FREQ = 438500000 # (BW = 0.05MHz = 50kHz) 438.45+(438.55-438.45)/2

# Other systems
# FREQ = 433500100 # telephreak party pager
# FREQ = 313850000 # Car keyfob

PKTLEN = 1       # Set my packet length to 6 as I am sending
                 # 6 bytes in each packet
DRATE = 512     # baud rate of 1000 means

# d.setMdmSyncMode(0)
# d.setFreq(432250000)
# d.setMdmModulation(MOD_2FSK)
# d.RFxmit('01100110')
# d.setMdmDRate(45)

try:
    d = RfCat()
    d.setFreq(FREQ)
    # d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmModulation(MOD_2FSK)
    # d.setMdmModulation(MOD_MSK)
    # d.setMdmModulation(MOD_GFSK)

    # d.setMdmDeviatn(1400)
    # d.setMdmDeviatn(1900)
    d.setMdmDeviatn(4500)

    d.makePktFLEN(PKTLEN)
    d.setMdmDRate(DRATE)
    d.setMdmSyncMode(0) # disable syncword and preamble as this is not used
                        # by the remote.
    #d.setMaxPower()    #imma chargin' mah lazer

    bytes = [0, 0x55, 0xff]


    d.setModeTX() # Probably a good idea to actually enter the right mode first!
    # d.RFxmit("".join(map(chr, bytes)))

    # TODO: Write a OOK/Morse station identity tool...
    d.RFxmit('CALLSIGN, Sorry for the noise') # Station identity maaan

    # OH MY GOD YOU MUST MUST MUST DO THIS! Otherwise you get USB timeouts!
    d.setModeIDLE() # DO THIS OR GET USB TIMEOUTS!
    # OH MY GOD YOU MUST MUST MUST DO THIS! Otherwise you get USB timeouts!

except Exception, e:
    d.setModeIDLE()
    sys.exit("Error %s" % str(e))
    # TODO implement software reset in case of USB timeout
