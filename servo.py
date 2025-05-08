import time
from enum import IntEnum
from pymodbus.client import ModbusSerialClient

class ServoRegisters(IntEnum):
    MODBUS_ENABLE = 0x00
    DRIVE_OUTPUT_ENABLE = 0x01
    MOTOR_TARGET_SPEED = 0x02
    MOTOR_ACCELERATION = 0x03
    WEAK_MAGNETIC_ANGLE = 0x04
    SPEED_LOOP_PROPORTIONAL_COEFFICIENT = 0x05
    SPEED_LOOP_INTEGRATION_TIME = 0x06
    POSITION_RING_PROPORTIONAL_COEFFICIENT = 0x07
    SPEED_FEED = 0x08
    DIR_POLARITY = 0x09
    ELECTRONIC_GEAR_MOLECULES = 0x0A
    ELECTRONIC_GEAR_DENOMINATOR = 0x0B
    TARGET_POSITION_LOW_16_BITS = 0x0C
    TARGET_POSITION_HIGH_16_BITS = 0x0D
    ALARM_CODE = 0x0E
    SYSTEM_CURRENT = 0x0F
    MOTOR_CURRENT_SPEED = 0x10
    SYSTEM_VOLTAGE = 0x11
    SYSTEM_TEMPERATURE = 0x12
    SYSTEM_OUTPUT_PWM = 0x13
    PARAMETER_SAVING_FLAG = 0x14
    DEVICE_ADDRESS = 0x15
    ABSOLUTE_POSITION_LOW_16_BITS = 0x16
    ABSOLUTE_POSITION_HIGH_16_BITS = 0x17
    STILL_MAXIMUM_ALLOWED_OUTPUT = 0x18
    SPECIFIC_FUNCTION = 0x19

    @classmethod
    def length_of_longest_name(e):
        l = 0
        for v in e:
            l = max(l, len(v.name))
        return l

R = ServoRegisters

PORT = "/dev/ttyUSB1"

class Servo:
    def __init__(self, p=PORT):
        self.client = ModbusSerialClient(port=p, baudrate=19200, timeout=1, parity='N', stopbits=1, bytesize=8)

    def get_all_registers(self):
        max_length = R.length_of_longest_name()
        for r in R:
            result = self.client.read_holding_registers(r.value)
            value = result.registers[0]
            print(f"{r.name.ljust(max_length)} ({r.value:02X}) = {value}")

    # TODO: figure out which special function actually does homing
    def home(self):
        self.write_register(R.SPECIFIC_FUNCTION, 1)

    # pass in e.g. [10000, 0] to turn a little bit
    def turn(self, amounts):
        self.client.write_registers(R.TARGET_POSITION_LOW_16_BITS, amounts)

    def write_register(self, reg, val):
        print(self.client.write_register(reg, val))

    def read_register(self, reg):
        return self.client.read_holding_registers(reg).registers[0]

    def system_current(self):
        return self.read_register(R.SYSTEM_CURRENT)

    def speed(self):
        return from_twos_complement(self.read_register(R.MOTOR_CURRENT_SPEED), 16) / 10

    def voltage(self):
        return self.read_register(R.SYSTEM_VOLTAGE) / 327

    # returns a value in the range -1.0 to 1.0
    # note the documented range is -32767 to 32767, but it appears to be actually 32000 based on comparisons to max output
    def output(self):
        return from_twos_complement(self.read_register(R.SYSTEM_OUTPUT_PWM), 16) / 32000

    # takes a value from 0 to 1.0
    # documented max might be 0.609? Docs are not good.
    def set_max_output(self, m):
        self.write_register(R.STILL_MAXIMUM_ALLOWED_OUTPUT, int(m * 1000))

    def max_output(self):
        return self.read_register(R.STILL_MAXIMUM_ALLOWED_OUTPUT) / 1000

    def target_position(self):
        response = self.client.read_holding_registers(R.TARGET_POSITION_LOW_16_BITS, count=2)
        return from_twos_complement(merge_16bit(response.registers), 32)

    def absolute_position(self):
        response = self.client.read_holding_registers(R.ABSOLUTE_POSITION_LOW_16_BITS, count=2)
        return from_twos_complement(merge_16bit(response.registers), 32)

    def wait_for_move_complete(self, l):
        while True:
            target = self.target_position()
            l(target)
            if (abs(target) < 10):
                return
            time.sleep(0.1)

def merge_16bit(vals):
    return sum(v << (i * 16) for i, v in enumerate(vals))

# Convert a 16 or 32-bit value from unsigned to signed
# if you have some weird system that doesn't use 2s complement this will fail
def from_twos_complement(val, bits):
    return int.from_bytes(val.to_bytes(bits // 8), signed=True)

def watch(l):
    while True:
        l()
        time.sleep(0.1)

def main():
    s = Servo()
    print("registers at startup")
    s.get_all_registers()
    print("setting speed and max output")
    s.write_register(R.MODBUS_ENABLE, 1)
    s.write_register(R.MOTOR_TARGET_SPEED, 20)
    s.set_max_output(0.1)
    print("running test movement")
    s.turn([0, 1])

    s.wait_for_move_complete(lambda p: print("target pos:", p))

    print("homing")
    s.home()
    while s.read_register(R.MODBUS_ENABLE):
        print(s.output(), s.absolute_position(), s.max_output())
    print("homing complete?")
    s.get_all_registers()

if __name__ == "__main__":
    main()
