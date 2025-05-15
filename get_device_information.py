#!/usr/bin/env python3

import pymodbus
from pymodbus.constants import DeviceInformation as DI

from servo import *


def trace_pdu(b, pdu):
    print("trace_pdu: {b} {pdu}".format(b=b, pdu=pdu))
    return pdu

def trace_packet(b, bt):
    print("trace_packet: {b} {bt}".format(b=b, bt=bt.hex()))
    return bt

s = Servo(trace_pdu=trace_pdu, trace_packet=trace_packet)
s.get_all_registers()

def read_device_information(s, **kwargs):
    try:
        print(s.client.read_device_information(**kwargs))
    except pymodbus.exceptions.ModbusIOException as e:
        print("error:", e)

read_device_information(s, read_code=DI.BASIC, object_id=0)
read_device_information(s, read_code=DI.REGULAR, object_id=0)
read_device_information(s, read_code=DI.EXTENDED, object_id=0)
read_device_information(s, read_code=DI.SPECIFIC, object_id=0)
