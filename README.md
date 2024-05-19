# SF8xxx-controller

Software for Maiman Electronics SF8xxx diode controllers.\
Commands:\
dial [port] [device] - Connect device at [port], addressable by [device].\
hangup [device] - Disconnect this device.\
qrd [device] - Quick RunDown of device status.\
configure [device] - Set device registers for easy lab use.\
tec set [device] [on/off] - Turn TEC of [device] on or off.\
tec temp [device] [temperature, C] - Set TEC temperature of [device].\
dri set [device] [on/off] - Turn driver of [device] on or off.\
dri cur(max) [device] [current, mA] - Set (max) driver current of [device].\
list - Print a list of connected devices with ports.\
exit - Exit program.\
[device] = "all" to perform the command for all devices (except for dial and driver current routines).\
Author: Douglas McCulloch, May 2024

Files:
`SF8xxx.py` - library to interface with Maiman SF8xxx controller boards
`Console.py` - console object
`main.py` - run this
