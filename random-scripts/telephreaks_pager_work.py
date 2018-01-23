#!/usr/bin/python2.7

# pylint: disable=W0614

import sys
from rflib import *

# FREQ = 433920000 # Set my frequency to the gate remote
# FREQ = 433250000 # Good (usually empty) 70cm HAM band
FREQ = 433506000 # telephreak party pager (shifted because YS1 is off)
# FREQ = 313850000 # Car keyfob
PKTLEN = 10       # Set my packet length to 6 as I am sending
                 # 6 bytes in each packet
DRATE = 500     # baud rate of 1000 means

# d.setMdmSyncMode(0)
# d.setFreq(432250000)
# d.setMdmModulation(MOD_2FSK)
# d.RFxmit('01100110')
# d.setMdmDRate(45)

try:
    d = RfCat()
    d.setFreq(FREQ) #433500100
    realFreq = d.getFreq()
    print("Real frequency: ", realFreq)
    # d.setFreq(433500100) #
    # d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmModulation(MOD_2FSK)
    # d.setMdmModulation(MOD_MSK)
    # d.setMdmModulation(MOD_GFSK)

    # d.setMdmDeviatn(1400)
    # d.setMdmDeviatn(1900)
    d.setMdmDeviatn(4700)

    d.makePktFLEN(PKTLEN)
    d.setMdmDRate(DRATE)
    print("Modem rate: ", d.getMdmDRate())
    d.setMdmSyncWord(0b1010101010101010)
    d.setMdmSyncMode(SYNCM_CARRIER) # Enable sync word
    # d.setMdmSyncMode(0) # disable syncword and preamble as this is not used
                        # by the remote.
    #d.setMaxPower()    #imma chargin' mah lazer

    print("Real frequency: ", realFreq)

    bytes = [0, 0x55, 0xff]
    d.RFxmit('Sorry for the noise. Telephreaks, let me in!')
    # d.RFxmit("".join(map(chr, bytes)))

except Exception, e:
    sys.exit("Error %s" % str(e))
    # TODO implement software reset in case of USB timeout
