# SF8xxx-controller 1.0
Basic terminal-based software to control output current and temperature on an arbitrary number of Maiman SF8xxx laser diode/SOA controllers connected over UART, using the pySerial library for this.

### To do
- Keep using it until there are bugs
- Implement system to load device defaults for quicker setup of multiple devices

### Synopsis
Software for Maiman Electronics SF8xxx diode controllers.

Commands:

`dial [port] [device]` - Connect device at `[port]`, addressable by `[device]`.
\
`hangup [device]` - Disconnect this device.


`qrd [device]` - Quick RunDown of device status.
\
`qrrd [device]` - QuickeR RunDown of device status.


`configure [device]` - Set device registers for easy lab use.*


`tec set [device] [on/off]` - Turn TEC on or off.
\
`tec temp [device] [temperature, C]` - Set TEC temperature.
\
`tec stat [device]` - TEC status register contents

`dri set [device] [on/off]` - Turn driver of on or off.
\
`dri cur(max) [device] [current, mA]` - Set (max) driver current.
\
`dri stat [device]` - Driver status register contents

`lock [device]` - Print register contents for lock status.


`max [device]` - Print current maxima (no pun intended).


`list` - Print a list of connected devices with ports.

`exit` - Exit program.

(`[device]` = "all" to perform the command for all devices (except for `dial` and driver current (`dri cur(max)`) routines).)
Author: Douglas McCulloch, May 2024

*"easy lab use" means: ignore external NTC thermistor, but interlock the driver output between analog pins 15 and 16 (any GND). This command will likely need to be run initially as the driver/TEC enable may be set to "external" on power-up.

### Usage and installation
If on Linux or whatever you need to add yourself to the `dialout` group in
order to access serial devices.

The executable (currently `main.py`) contains the shebang necessary for
execution on Linux or whatever but can still be run under python.

### Files
`SF8xxx.py` - library to interface with Maiman SF8xxx controller boards.

`Console.py` - console object.

`main.py` - run this for now
