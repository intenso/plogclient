#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import binascii
import signal
from bitstring import ConstBitStream

host = sys.argv[1]
port = 19999
#Yes it's this simple, just open a socket towards the logclient port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def getHeader(bitstream):
  header = bitstream.readlist('8*uintle:32')
  return header

def printMessage(bitstream):
  msgSize = (header[0] * 8 - 256)
  print binascii.unhexlify(bitstream[256:msgSize].hex)
  bitstream.pos += msgSize

def signal_handler(signal, frame):
  """Make sure to close the socket on exit"""
  s.close()
  sys.exit(0)
#Since the STB only handles a few log sessions at the time we need to
#make sure we close every we open or else we will not be able to
#connect any more.
signal.signal(signal.SIGINT, signal_handler)

while True:
  data = s.recv(4096)
  bitstream = ConstBitStream(bytes=data)
  header = getHeader(bitstream)
  if header[3] == 1:
    print header
    printMessage(bitstream)
