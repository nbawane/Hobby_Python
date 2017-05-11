###########################################################################
# Copyright (c) SanDisk Corp. 2008-2009 - All rights reserved.
# This code, and all derivative work, is the exclusive property of SanDisk
# and may not be used without SanDisk's authorization.
###########################################################################

import serial
import sys
from optparse import OptionParser

parser=OptionParser()

parser.add_option("-p","--serialport",dest="port",default=-1,
                  help="Serial port number for the forced-download relay, starts at 0. comX => port X-1")
parser.add_option("--relaygroup",dest="set",default='0',
                   help="Identifies relays the forced download switch is connected to.  0-> relays 1 and 2, -> relays 2 and 3")
(options, args) = parser.parse_args()
#print options
#print options.port

ser=serial.Serial()
# Eventually need to get the port number from the relay.
# but for now hard wire it for the test station