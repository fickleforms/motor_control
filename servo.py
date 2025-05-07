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

    def set_slow_speeds(self):
        self.write_register(R.MOTOR_TARGET_SPEED, 10)

    def home(self):
        self.write_register(R.SPECIFIC_FUNCTION, 1)

    # pass in e.g. [10000, 0] to turn a little bit
    def turn(self, amounts):
        self.client.write_registers(R.TARGET_POSITION_LOW_16_BITS, amounts)

    def write_register(self, reg, val):
        print(self.client.write_register(reg, val))

def main():
    s = Servo()
    s.get_all_registers()
    s.set_slow_speeds()
    s.home()

if __name__ == "__main__":
    main()
