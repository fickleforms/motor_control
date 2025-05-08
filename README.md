## TODO

- [ ] Make the Servo object know how to interpret each register
- [ ] Add a **format**() method to Servo
- [ ] Build a setup where I can put a known load on the servo (e.g. OSSM with a
      weight) to explore output limiting

## Open Questions

### Why is register 0x01 = 7?

The docs claim this takes values 0~1. Is it a bitfield? What do the other two
bits mean?

### How do the PID parameters work?

### How does the motor acceleration parameter work?

What's up with the values

### How does the acceleration + deceleration curve generation work?

In particular, is there any way to get slow deceleration? Slow acceleration can
be accomplished by setting register 0x03.

### What the heck is going on with the bitfields of 0x18?

This appears to be both a limit _and_ an alarm field?

## Answered Questions

### Why are there two sets of position registers?

The first set, 0x0C~0x0D, are relative. Setting them will make the motor move a
given amount. The second set, 0x16~0x17, are absolute.

So e.g. if the absolute position is (1000, 500) and we set the target position
registers to (500, 0), then it will move until the new absolute position is
(1500, 0).

### What's going on with maximum output?

The register 0x13 allows seeing the current output. It is documented as
returning a value from -32768 through 32767, with that representing -100% to
100%. However, the actual range is from -32000 to 32000.

The register 0x18 allows setting the maximum output. It is documented as running
from 0 to 609, represinting 0 to 60.9%. I don't know why it has that range - it
seems very odd.

If we set 0x18 to 8% (80) and then run a test, we will see the current output
cap out at 0.79968 (2559). 2560 / 32000 = 0.8, so it appears that they are doing
a comparison like abs(output) < max_output to decide whether output may be
increased. This works consistently for other max output settings, moving in
either direction.

### How can we tell if there's an ongoing move?

The target position shows how far off the controller is. If PID settings are set
loosely, then it'll linger far away, but usually it'll get pretty close. So the
simplest thing is to do a threshold on position, e.g. abs(position) < 10.
