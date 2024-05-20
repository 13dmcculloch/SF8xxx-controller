# SF8xxx-controller
Basic terminal-based software to control output current and temperature on an arbitrary number of Maiman SF8xxx laser diode/SOA controllers connected over UART, using the pySerial library for this.

### To do
- ~~Fix the bug where "`hangup all`" would crash program~~ (The fix is untested.)
- Add functionality to get the current setpoint/actual (max) current/temperature outside of `qrd` which is quite limited and comes straight from `SF8xxx`.

### Synopsis
Software for Maiman Electronics SF8xxx diode controllers.\
Commands:\
`dial [port] [device]` - Connect device at `[port]`, addressable by `[device]`.\
`hangup [device]` - Disconnect this device.\
`qrd [device]` - Quick RunDown of device status.\
`configure [device]` - Set device registers for easy lab use.*\
`tec set [device] [on/off]` - Turn TEC of `[device]` on or off.\
`tec temp [device] [temperature, C]` - Set TEC temperature of `[device]`.\
`dri set [device] [on/off]` - Turn driver of `[device]` on or off.\
`dri cur(max) [device] [current, mA]` - Set (max) driver current of `[device]`.\
`list` - Print a list of connected devices with ports.\
`exit` - Exit program.\
`[device]` = "all" to perform the command for all devices (except for `dial` and driver current (`dri cur(max)`) routines).\
Author: Douglas McCulloch, May 2024

*"easy lab use" means: ignore external NTC thermistor, but interlock the driver output. This command will likely need to be run initially as the driver/TEC enable may be set to "external" on power-up.

Files:
`SF8xxx.py` - library to interface with Maiman SF8xxx controller boards.\
`Console.py` - console object.\
`main.py` - run this
