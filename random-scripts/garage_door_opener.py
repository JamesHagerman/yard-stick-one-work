#!/usr/bin/python2.7

# pylint: disable=W0614

import sys
from rflib import *

FREQ = 433920000 # Set my frequency to the gate remote
# FREQ = 313850000 # Set my frequency to the gate remote
PKTLEN = 6       # Set my packet length to 6 as I am sending
                 # 6 bytes in each packet
DRATE = 1000     # baud rate of 1000 means that a 1ms pulse
                 # can be counted as a bit

packet_1 = [
            '00010001', '00010111', '01110001',
            '01110011', '01110001', '00110000'
           ]
packet_2 = [
            '00010001', '00100100', '01100111',
            '01001010', '00001111', '00011110'
           ]
data_hex_1 = [chr(int(x, 2)) for x in packet_1]
data_hex_2 = [chr(int(x, 2)) for x in packet_2]

def send_data(d, data, repeat=1):
    # PCM'ify the packets
    for i in range(0, repeat):
        for packet in data:
            d.RFxmit(packet)
try:
    d = RfCat()
    # d.RESET
    d.setFreq(FREQ)
    d.setMdmModulation(MOD_ASK_OOK)
    d.makePktFLEN(PKTLEN)
    d.setMdmDRate(DRATE)
    d.setMdmSyncMode(0) # disable syncword and preamble as this is not used
                        # by the remote.
    #d.setMaxPower()    #imma chargin' mah lazer
    print "sending:", ["".join(data_hex_1), "".join(data_hex_2)]
    send_data(d, ["".join(data_hex_1), "".join(data_hex_2)])

except Exception, e:
    sys.exit("Error %s" % str(e))
    # TODO implement software reset in case of USB timeout
