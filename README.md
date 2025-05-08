## TODO
- [ ] Make the Servo object know how to interpret each register
- [ ] Add a __format__() method to Servo
- [ ] Build a setup where I can put a known load on the servo (e.g. OSSM with a weight) to explore output limiting


## Open Questions

### Why is register 0x01 = 7?
The docs claim this takes values 0~1. Is it a bitfield? What do the other two bits mean?

### How do the PID parameters work?

### How does the motor acceleration parameter work?
What's up with the values 

### How does the acceleration + deceleration curve generation work?
In particular, is there any way to get slow acceleration?

### How can we set maximum output?
There's a register for this, 0x18, which appears to set max output from 0~60.9%. That's a very odd range. Also, the low bit seems to have a meaning regarding alarm vs reduce output.

How is this interpreted? Is there any way to see the *current* output in these units? Is this limiting SYSTEM_CURRENT * SYSTEM_VOLTAGE to the value
configured for this specific motor? That would be 100W for the 57AIM30, so a limit of 60.9% would be 60.9W. At the voltage of 19, 60.9W is 3.2, which means a limit of 6400 for SYSTEM_CURRENT.

### What the heck is going on with the bitfields of 0x18?
This appears to be both a limit *and* an alarm field?

## Answered Questions

### Why are there two sets of position registers?
The first set, 0x0C~0x0D, are relative. Setting them will make the motor move a given amount.
The second set, 0x16~0x17, are absolute.

So e.g. if the absolute position is (1000, 500) and we set the target position registers to (500, 0), then it will move until the new absolute position is (1500, 0).
