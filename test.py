#!/usr/bin/env python

from FreshRoastSR700 import FreshRoastSR700

roaster = FreshRoastSR700()

s = roaster.genPacket()

print s.encode('hex')
