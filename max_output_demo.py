#!/usr/bin/env python3

from servo import *

s = Servo()
s.write_register(R.MODBUS_ENABLE, 1)
s.write_register(R.MOTOR_TARGET_SPEED, 20)
s.write_register(R.DIR_POLARITY, 1)
s.set_max_output(0.09)
s.turn([0, 2])
print("stop the motor with your hand to watch the output change")
s.wait_for_move_complete(lambda _: print(s.output()))
