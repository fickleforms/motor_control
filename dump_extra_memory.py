#!/usr/bin/env python3

from servo import *

s = Servo()
s.get_all_registers()
print(s.client.read_holding_registers(0, 0x19))
