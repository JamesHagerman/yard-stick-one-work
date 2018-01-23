# Some useful YARD Stick One notes

This thing is a bit of a beast. People don't give it NEARLY the credit, or the
documentation it deserves.

Two ways of using this thing: `rfcat` directly, or write a python script for it.

Basically, writing a python script is easier. Using rfcat directly is great but
often, there are just too many silly settings to configure

## NOTE ABOUT FREQUENCIES

Make sure you're transmitting in a band you're allowed to. No, this thing ain't that powerful
at 20dBm (100mW) output but it's worth knowing that can literally kill people if you end up
fucking with the wrong band...

Get a HAM license, look up the band plans the frequency coordinator in your area puts out, find
the experimental allocation range, and stick to the middle of that range.

... Unless you're super clear on what you're doing.

## NOTE ABOUT POWER OUTPUT

Basically, don't transmit into a null load. Throw a 50Ohm antenna on there. If you didn't get one
yet, go get one.

I found this note somewhere. It's as accurate as I've found:

```
>> What is the maximum transmitting power of the yardstick in mW?
>
> Roughly it is 100 mW (20 dBm).  The transmit power is reduced a bit as
> the frequency increases, and it may vary from unit to unit.  It is
> approximately 20 dBm at 300 MHz, 19 dBm at 450 MHz, and 18 dBm at 900
> MHz.  (Those numbers are with the TX amplifier enabled.)
```

## NOTE ABOUT MAXIMUM POWER INPUT

I don't know what the maximum input power this thing can handle is but basically don't
fire up your Baofeng right next to the YARD Stick One or connect a transmitter directly
to it without a good sized attenuator in the signal path.

## Using Python

There is a script named something like `basic-starter.py` kicking around near this document. It
would be a good place to get started.

Here's a short version of it:

```python
#!/usr/bin/python2.7
import sys
from rflib import *
# The middle of the two NoCal, 70cm, Experimental bands
FREQ = 434200000 # (BW = 0.6MHz = 600kHz) 433.60+(434.80-433.60)/2
# FREQ = 438500000 # (BW = 0.05MHz = 50kHz) 438.45+(438.55-438.45)/2
PKTLEN = 1       # Set packet length
DRATE = 512
try:
    d = RfCat()
    d.setFreq(FREQ)
    d.setMdmModulation(MOD_2FSK)
    d.setMdmDeviatn(4500)
    d.makePktFLEN(PKTLEN)
    d.setMdmDRate(DRATE)
    d.setMdmSyncMode(0) # disable syncword and preamble as this is not used
                        # by the remote.
    #d.setMaxPower()    # Pretty sure this turns on the TX amp
    bytes = [0, 0x41, 0xff] # Data to send
    d.setModeTX()       # It's good to enter the right mode first...
    d.RFxmit("".join(map(chr, bytes)))

    # WITHOUT THIS YOU WILL GET USB TIMEOUTS!
    d.setModeIDLE()  # DO THIS OR GET USB TIMEOUTS!
except Exception, e: # Make sure things are sane...
    d.setModeIDLE()  # Probably a good idea here too... just in case
    sys.exit("Error %s" % str(e))
```

## Using `rfcat`

Just start playing with: `rfcat -r`

### Getting help on  rfcat

The author highly suggests picking up the cc1111 manual from TI...

After using `rfcat -r` to get an interactive terminal, you can type the following to get some help:

```
help(d)
```

## Modulation modes:

These go for either using Python OR rfcat.

The simply way to see them is to just type `MOD_` and hit tab in the interactive console...

I was dumb when I started and I had a bit of a hard time finding these. They are defined in `rfcat/rflib/chipcon_nic.py` along with a bunch of other useful things.

NOTE: Keep in mind that some of these modes are limited in various ways. Either bandwidth
limitations (can't do RTTY using HAM 2FSK deviations), baud rate limitations, so on...

Also, each one has it's own strange ness with bit packing. Start digging... :D

```python
"""  MODULATIONS
Note that MSK is only supported for data rates above 26 kBaud and GFSK,
ASK , and OOK is only supported for data rate up until 250 kBaud. MSK
cannot be used if Manchester encoding/decoding is enabled.
"""
MOD_2FSK                        = 0x00
MOD_GFSK                        = 0x10
MOD_ASK_OOK                     = 0x30
MOD_MSK                         = 0x70
MANCHESTER                      = 0x08

MODULATIONS = {
        MOD_2FSK    : "2FSK",
        MOD_GFSK    : "GFSK",
        MOD_ASK_OOK : "ASK/OOK",
        MOD_MSK     : "MSK",
        MOD_2FSK | MANCHESTER    : "2FSK/Manchester encoding",
        MOD_GFSK | MANCHESTER    : "GFSK/Manchester encoding",
        MOD_ASK_OOK | MANCHESTER : "ASK/OOK/Manchester encoding",
        MOD_MSK  | MANCHESTER    : "MSK/Manchester encoding",
        }
```




## Projects I'm kinda half working on

### rfpwnon.py

This is a fun on:  
https://www.legacysecuritygroup.com/index.php/categories/13-sdr/22-rfpwnon-py-the-ultimate-rfcat-ask-ook-brute-force-tool


### Capture car key:

Car key's fcc id: `MLBHLIK-1TA`

https://fccid.io/MLBHLIK-1TA

It runs on:
```
313.85 MHz
313850000. Hz
```

So, we can use this to set the frequency:
```
d.setFreq(313850000)
d.discover()
```

On lock:
```
(1458374559.796) Received:  fffffffffffffffffdf25ffffff2fffffffbff0007efffe1fff000007fff
(1458374559.809) Received:  fffffff001fffffc07f000003ffffc00007e00007ffef820007ffff00000
(1458374559.823) Received:  000002000007f00ffe000003c000001fc0000002000001fe000000780000
(1458374559.832) Received:  fffffc0001ffff0000001f8000007fffffc000003fffffffc0000000fff0
(1458374559.840) Received:  007fffe000000fffffffe00000003fffffff80000001fffffffe00000003
(1458374559.846) Received:  fffe00000003fffffff80000000ffffffff00000001fffffff800000007f
(1458374559.853) Received:  ffe00000001fffffff800000007fff7fff000001fffffffe00000003ffff
(1458374559.860) Received:  00000fffffffc00000007fffffff00000001fffdfffc00000007ffffffe0
(1458374559.867) Received:  0003fffffff80000001fffffffe00000007fff7fff00000001fffffffc00
(1458374559.873) Received:  007fffffff80000001fffffffe00000007fffffff80000000fffffffe000
(1458374559.880) Received:  03fffffff00000000fffffffc00000007fffffff00000003fffbfff80000
(1458374559.887) Received:  fffffffe00000003fffffffc00000007fffffff00000001fffffffc00000
(1458374559.893) Received:  ffffffe00000003fffffffc00000007ffffffe00000003fffffff8000000
(1458374559.900) Received:  fffffe00000003fffffff80000000fffffffe00000003fffffff80000001
(1458374559.907) Received:  fff80000000ffffffff00000003fffffff00000001fffffff80000000fff
(1458374559.913) Received:  fe00000007fffffff80000000fffffffc00000003fffffff80000000fffe
(1458374559.920) Received:  e00000003fffffff80000000fffffffe00000003fffffff80000000fffff
(1458374559.927) Received:  00000003fffffff80000000fffffffe00000007fffffc000003fffe00000
(1458374559.934) Received:  fffbfff80000000fffffffe00000003fffffffc00000007ffffffe000000
(1458374559.941) Received:  ffffe00000007fffffff00000001fffffffc0000000fffffffc00000007f
(1458374559.947) Received:  fff80000001fffffffc00000003fffffff00000001fffffffc00000003ff
(1458374559.954) Received:  ff80000000fffffffe00000003fffffff000000000001fffffffffffffff
(1458374559.961) Received:  00000000001fffffffffffc00000000000fffe00000001fffffe00000000
(1458374559.968) Received:  fdfffffffe0000000000000003fffffff0000000000000003fffbfff0000
(1458374559.976) Received:  ffffffffffe0000000001fffffffe0000000fffffffffffffffc0000000f
(1458374559.983) Received:  fffffffffffc00000000000ffffe000000000007fffff80000000000ffff
(1458374559.992) Received:  f00000001ffffffc0000007ff8000007ffffff001fffffffc00000000000
(1458374560.000) Received:  fff801fffffff80000000fffeff80000000007fffffff000000000000fff
(1458374560.008) Received:  0000000000fffffffe000000007fffffc000003fff800800000000000000
(1458374560.019) Received:  03fffff80003fffbfffc000003fffffffffffff800000000000003ffff00
(1458374560.027) Received:  0003fe0000003fffff00000000003fffbfff80000000000007fffffe0000
(1458374560.037) Received:  00000000780000003ff000000001fffffffefffe01ffffffffffffffc000
(1458374560.047) Received:  fffffe000000000003f8000000001fff800000000001fffff00000001fff
(1458374560.055) Received:  c00007ffffffffffe00000007fff00000001ff7fff00000007fffffff000
(1458374560.063) Received:  03ffe00000007ffc0000000007fffffff000000000000fffffffc0000000
(1458374560.071) Received:  0fffffc00000000000fff80000000fff000000000000000000003ffffffd
(1458374560.078) Received:  ffffbfffffffc0000000fffffffffffffffffffffffffffffffffffffffd

```



## Install notes

### Get some packages:

```
sudo apt-get install mercurial ipython
```

#### Get rfcat firmware and userland tools

```
hg clone ssh://hg@bitbucket.org/JamesHagerman/rfcatssh://hg@bitbucket.org/JamesHagerman/rfcat
```

### Client install notes

This needs both libusb and python-usb.

#### install python-usb:
```
sudo pip install pyusb==1.0.0b1
```

```
cd rfcat
sudo python setup.py install
```



## Firmware compile notes:

You probably want to skip these:

### Get some packages:

```
sudo apt-get install sdcc
```

### Compile:

```
cd rfcat/firmware/
```

## Where the hell is the CODE!?

Basically, there are no docs for rfcat. you get to dig through the library source.

Once you start in interactive mode (which gets done in the libraries `__init__.py` file) than you can use ipython to dig through the options...

Or you can just go look in `chipcon_usb.py` for all the method definitions.

Good luck. It's still a god damn mess.

### Trying to get yardstick one working under android:

UPDATE: Obviously, this thing uses libusb. Direct control shouldn't be too hard...
But Termux, for example, has shitty libusb support :(

Basically, rfcat yells at us and says that we need to attach the dongle but it IS attached. So let's try to use the code that rfcat does to determine if there is a dongle.... and then we can at least start debugging wtf is going on with the driver.

This is the method that's supposed to grab all of the dongles via the libusb/usb python module:

```py
def getRfCatDevices():
    '''
    returns a list of USB device objects for any rfcats that are plugged in
    NOTE: if any rfcats are in bootloader mode, this will cause python to Exit
    '''
    rfcats = []
    for bus in usb.busses():
        for dev in bus.devices:
            # OpenMoko assigned or Legacy TI
            if (dev.idVendor == 0x0451 and dev.idProduct == 0x4715) or (dev.idVendor == 0x1d50 and (dev.idProduct == 0x6047 or dev.idProduct == 0x6048 or dev.idProduct == 0x605b)):
                rfcats.append(dev)

            elif (dev.idVendor == 0x1d50 and (dev.idProduct == 0x6049 or dev.idProduct == 0x604a)):
                print "Already in Bootloader Mode... exiting"
                exit(0)

    return rfcats
```









## List all available methods:

>>> dir(d)
['FHSSxmit', 'RESET', 'RFcapture', 'RFdump', 'RFlisten', 'RFrecv', 'RFxmit', '__doc__', '__init__', '__module__', '_bootloader', '_clear_buffers', '_d', '_debug', '_do', '_doSpecAn', '_init_on_reconnect', '_quiet', '_radio_configured', '_recvEP0', '_recvEP5', '_recv_time', '_rfmode', '_sendEP0', '_sendEP5', '_stopSpecAn', '_threadGo', '_usbcfg', '_usbeps', '_usberrorcnt', '_usbintf', '_usbmaxi', '_usbmaxo', 'adjustFreqOffset', 'bootloader', 'calculateFsIF', 'calculateFsOffset', 'calculateMdmDeviatn', 'calculatePktChanBW', 'changeChannel', 'checkRepr', 'chipnum', 'chipstr', 'cleanup', 'ctrl_thread', 'debug', 'devnum', 'discover', 'endec', 'ep0GetAddr', 'ep0Peek', 'ep0Ping', 'ep0Poke', 'ep0Reset', 'ep5timeout', 'freq_offset_accumulator', 'getAESmode', 'getAmpMode', 'getBSLimit', 'getBuildInfo', 'getChannel', 'getChannels', 'getDebugCodes', 'getEnableMdmDCFilter', 'getEnableMdmFEC', 'getEnableMdmManchester', 'getEnablePktAppendStatus', 'getEnablePktCRC', 'getEnablePktDataWhitening', 'getFHSSstate', 'getFreq', 'getFreqEst', 'getFsIF', 'getFsOffset', 'getInterruptRegisters', 'getLQI', 'getMACdata', 'getMACthreshold', 'getMARCSTATE', 'getMdmChanBW', 'getMdmChanSpc', 'getMdmDRate', 'getMdmDeviatn', 'getMdmModulation', 'getMdmNumPreamble', 'getMdmSyncMode', 'getMdmSyncWord', 'getPartNum', 'getPktAddr', 'getPktLEN', 'getPktPQT', 'getRSSI', 'getRadioConfig', 'idx', 'lowball', 'lowballRestore', 'mac_SyncCell', 'makePktFLEN', 'makePktVLEN', 'max_packet_size', 'mhz', 'nextChannel', 'peek', 'ping', 'poke', 'pokeReg', 'printClientState', 'printRadioConfig', 'printRadioState', 'radiocfg', 'recv', 'recvAll', 'recv_event', 'recv_mbox', 'recv_queue', 'recv_thread', 'recv_threadcounter', 'reprAESMode', 'reprClientState', 'reprFreqConfig', 'reprHardwareConfig', 'reprMACdata', 'reprMdmModulation', 'reprModemConfig', 'reprPacketConfig', 'reprRadioConfig', 'reprRadioState', 'reprRadioTestSignalConfig', 'reprSoftwareConfig', 'reset_event', 'resetup', 'rf_configure', 'rf_redirection', 'rsema', 'runEP5_recv', 'runEP5_send', 'run_ctrl', 'scan', 'send', 'send_thread', 'send_threadcounter', 'setAESiv', 'setAESkey', 'setAESmode', 'setAmpMode', 'setBSLimit', 'setChannel', 'setChannels', 'setEnDeCoder', 'setEnableCCA', 'setEnableMdmDCFilter', 'setEnableMdmFEC', 'setEnableMdmManchester', 'setEnablePktAppendStatus', 'setEnablePktCRC', 'setEnablePktDataWhitening', 'setFHSSstate', 'setFreq', 'setFsIF', 'setFsOffset', 'setMACdata', 'setMACperiod', 'setMACthreshold', 'setMaxPower', 'setMdmChanBW', 'setMdmChanSpc', 'setMdmDRate', 'setMdmDeviatn', 'setMdmModulation', 'setMdmNumPreamble', 'setMdmSyncMode', 'setMdmSyncWord', 'setModeIDLE', 'setModeRX', 'setModeTX', 'setPktAddr', 'setPktPQT', 'setPower', 'setRFRegister', 'setRFbits', 'setRFparameters', 'setRadioConfig', 'setRfMode', 'setup', 'setup24330MHz', 'setup900MHz', 'setup900MHzContTrans', 'setup900MHzHopTrans', 'setup_rfstudio_902PktTx', 'specan', 'startHopping', 'stopHopping', 'strobeModeCAL', 'strobeModeFSTXON', 'strobeModeIDLE', 'strobeModeRX', 'strobeModeReturn', 'strobeModeTX', 'testTX', 'trash', 'xmit_event', 'xmit_queue', 'xsema']


using ipython:

Display all 177 possibilities? (y or n)
d.FHSSxmit                   d.getMdmSyncMode             d.setAmpMode
d.RESET                      d.getMdmSyncWord             d.setBSLimit
d.RFcapture                  d.getPartNum                 d.setChannel
d.RFdump                     d.getPktAddr                 d.setChannels
d.RFlisten                   d.getPktLEN                  d.setEnDeCoder
d.RFrecv                     d.getPktPQT                  d.setEnableCCA
d.RFxmit                     d.getRSSI                    d.setEnableMdmDCFilter
d.adjustFreqOffset           d.getRadioConfig             d.setEnableMdmFEC
d.bootloader                 d.idx                        d.setEnableMdmManchester
d.calculateFsIF              d.lowball                    d.setEnablePktAppendStatus
d.calculateFsOffset          d.lowballRestore             d.setEnablePktCRC
d.calculateMdmDeviatn        d.mac_SyncCell               d.setEnablePktDataWhitening
d.calculatePktChanBW         d.makePktFLEN                d.setFHSSstate
d.changeChannel              d.makePktVLEN                d.setFreq
d.checkRepr                  d.max_packet_size            d.setFsIF
d.chipnum                    d.mhz                        d.setFsOffset
d.chipstr                    d.nextChannel                d.setMACdata
d.cleanup                    d.peek                       d.setMACperiod
d.ctrl_thread                d.ping                       d.setMACthreshold
d.debug                      d.poke                       d.setMaxPower
d.devnum                     d.pokeReg                    d.setMdmChanBW
d.discover                   d.printClientState           d.setMdmChanSpc
d.endec                      d.printRadioConfig           d.setMdmDRate
d.ep0GetAddr                 d.printRadioState            d.setMdmDeviatn
d.ep0Peek                    d.radiocfg                   d.setMdmModulation
d.ep0Ping                    d.recv                       d.setMdmNumPreamble
d.ep0Poke                    d.recvAll                    d.setMdmSyncMode
d.ep0Reset                   d.recv_event                 d.setMdmSyncWord
d.ep5timeout                 d.recv_mbox                  d.setModeIDLE
d.freq_offset_accumulator    d.recv_queue                 d.setModeRX
d.getAESmode                 d.recv_thread                d.setModeTX
d.getAmpMode                 d.recv_threadcounter         d.setPktAddr
d.getBSLimit                 d.reprAESMode                d.setPktPQT
d.getBuildInfo               d.reprClientState            d.setPower
d.getChannel                 d.reprFreqConfig             d.setRFRegister
d.getChannels                d.reprHardwareConfig         d.setRFbits
d.getDebugCodes              d.reprMACdata                d.setRFparameters
d.getEnableMdmDCFilter       d.reprMdmModulation          d.setRadioConfig
d.getEnableMdmFEC            d.reprModemConfig            d.setRfMode
d.getEnableMdmManchester     d.reprPacketConfig           d.setup
d.getEnablePktAppendStatus   d.reprRadioConfig            d.setup24330MHz
d.getEnablePktCRC            d.reprRadioState             d.setup900MHz
d.getEnablePktDataWhitening  d.reprRadioTestSignalConfig  d.setup900MHzContTrans
d.getFHSSstate               d.reprSoftwareConfig         d.setup900MHzHopTrans
d.getFreq                    d.reset_event                d.setup_rfstudio_902PktTx
d.getFreqEst                 d.resetup                    d.specan
d.getFsIF                    d.rf_configure               d.startHopping
d.getFsOffset                d.rf_redirection             d.stopHopping
d.getInterruptRegisters      d.rsema                      d.strobeModeCAL
d.getLQI                     d.runEP5_recv                d.strobeModeFSTXON
d.getMACdata                 d.runEP5_send                d.strobeModeIDLE
d.getMACthreshold            d.run_ctrl                   d.strobeModeRX
d.getMARCSTATE               d.scan                       d.strobeModeReturn
d.getMdmChanBW               d.send                       d.strobeModeTX
d.getMdmChanSpc              d.send_thread                d.testTX
d.getMdmDRate                d.send_threadcounter         d.trash
d.getMdmDeviatn              d.setAESiv                   d.xmit_event
d.getMdmModulation           d.setAESkey                  d.xmit_queue
d.getMdmNumPreamble          d.setAESmode                 d.xsema
