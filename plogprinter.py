#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bitstring import ConstBitStream
import sys

c = ConstBitStream(filename=sys.argv[1])
#Most log entry ends with 0A, this helps us to seek to the beginning of an entry
start = c.find('0x0A', bytealigned=True)[0]
#Seek 8 byte into the stream to skip EOL from previus log entry
start += 8

c.pos = start

while True:
  #Read and print the binary log header
  header = c.readlist('8*uintle:32')
  print header
  #Get the size in bits of the log message
  msgSize = (header[0] * 8 - 256)
  #Move pointer after message
  c.pos += msgSize
  #Check if EOL is present after message, if true, move pointer 8 byte
  if c.peek(8).hex == '0a':
    c.pos += 8
