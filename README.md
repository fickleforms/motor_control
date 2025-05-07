## Open Questions

### Why is register 0x01 = 7?
The docs claim this takes values 0~1. Is it a bitfield? What do the other two bits mean?

### How do the PID parameters work?

### How does the motor acceleration parameter work?
What's up with the values 

### How does the acceleration + deceleration curve generation work?

### What the heck is going on with the bitfields of 0x18?
This appears to be both a limit *and* an alarm field?

## Answered Questions

### Why are there two sets of position registers?
The first set, 0x0C~0x0D, are relative. Setting them will make the motor move a given amount.
The second set, 0x16~0x17, are absolute.

So e.g. if the absolute position is (1000, 500) and we set the target position registers to (500, 0), then it will move until the new absolute position is (1500, 0).
