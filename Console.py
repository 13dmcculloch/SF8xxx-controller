# -*- coding: utf-8 -*-
"""
SF8xxx frontend

Created on Sun May 19 11:59:47 2024

@author: drm1g20
"""

import SF8xxx as sf8

class Console:
    def __init__(self):
        self.exit_status = False
        self.devices = {}
        
        self.__print_intro()
        
        while not self.exit_status:
            self.exit_status = self.__command(input("> "))
            
            
    def __del__(self):
        for d in self.devices.values():
            print("[CONSOLE]: Disconnecting", d.serial_no, "from",
                  d.port)
            
            d.dev.close()
            
    
    def __command(self, cmd: str):
        self.tokens = cmd.split()
        root = self.tokens[0]
        
        if root == 'exit':
            return True
        
        elif root == 'dial':
            if self.__token_len(3):
                return
            
            self.__dial(self.tokens[1], self.tokens[2])
            
        elif root == 'hangup':
            if self.__token_len(2):
                return
            
            if self.tokens[1] == 'all':
                for alias in self.devices.keys():
                    self.__hang_up(alias)
                
                self.__clean_devices()
                return
            
            self.__hang_up(self.tokens[1])
            self.__clean_devices()
            
            
        elif root == 'qrd':
            if self.__token_len(2):
                return
            
            if not self.__check(self.tokens[1]):
                return
            
            if self.tokens[1] == 'all':
                for alias, dev in self.devices.items():
                    print(alias + ':')
                    self.__qrd(alias)
                return
            
            print(self.tokens[1] + ':')
            self.__qrd(self.tokens[1])
            
        elif root == 'qrrd':
            if self.__token_len(2):
                return
            
            if not self.__check(self.tokens[1]):
                return
            
            if self.tokens[1] == 'all':
                for alias, dev in self.devices.items():
                    print(alias + ':')
                    self.__qrrd(alias)
                return
            
            print(self.tokens[1] + ':')
            self.__qrrd(self.tokens[1])
            
        elif root == 'configure':
            if self.__token_len(2):
                return
            
            if self.tokens[1] == 'all':
                for dev in self.devices.keys():
                    self.__configure(dev)
                return
            
            if not self.__check(self.tokens[1]):
                return
            
            self.__configure(self.tokens[1])
            
        elif root == 'tec':
            argc = len(self.tokens)
            if argc == 3:
                sel = self.tokens[1]
                alias = self.tokens[2]
                
                if sel == 'stat':
                    if alias == 'all':
                        for dev in self.devices.keys():
                            self.__print_tec_state(dev)
                        return
                    
                    self.__print_tec_state(alias)
                
                elif sel == 'on':
                    if alias == 'all':
                        for dev in self.devices.keys():
                            self.__is_tec_on(dev)
                        return
                    
                    self.__is_tec_on(alias)
                    
                return
                    
            if self.__token_len(4):
                return
            
            sel = self.tokens[1]  # set/temp/stat
            alias = self.tokens[2]
            value = self.tokens[3]  # on/off;(x)xx
            
            if not self.__check(alias):
                return
            
            if sel == 'set':
                if type(value) != str:
                    print("[CONSOLE]: Value not recognised. Want: 'on/off'.")
                    return
                
                if alias == 'all':
                    for dev in self.devices.keys():
                        self.__tec_set(dev, value)
                    return
                
                self.__tec_set(alias, value)
                
            elif sel == 'temp':
                if not self.__int_check(value):
                    return
                
                if alias == 'all':
                    for dev in self.devices.keys():
                        self.__tec_temp(dev, int(value))
                    return
                
                self.__tec_temp(alias, int(value))
                
            else:
                print("[CONSOLE]: TEC control select not recognised.")
                
        elif root == 'dri':
            argc = len(self.tokens)
            if argc == 3:
                sel = self.tokens[1]
                alias = self.tokens[2]
                
                if sel == 'stat':
                    if alias == 'all':
                        for dev in self.devices.keys():
                            self.__print_driver_state(dev)
                        return
                    
                    self.__print_driver_state(alias)
                
                elif sel == 'on':
                    if alias == 'all':
                        for dev in self.devices.keys():
                            self.__is_driver_on(dev)
                        return
                    
                    self.__is_driver_on(alias)
                    
                return

            if self.__token_len(4):
                return
            
            sel = self.tokens[1]
            alias = self.tokens[2]
            value = self.tokens[3]
            
            if not self.__check(alias):
                return
            
            if sel == 'set':  # turn driver on, off: dri set [alias] on/off
                if type(value) != str:
                    print("[CONSOLE]: Value not recognised. Want: 'on/off'.")
                    return
                
                if alias == 'all':
                    for dev in self.devices.keys():
                        self.__driver_set(dev, value)
                        
                self.__driver_set(alias, value)
                
            elif sel == 'cur':  # set driver current: dri cur [alias] xxx
                if not self.__int_check(value):
                    return
                
                self.__driver_current(alias, int(value))
                
            elif sel == 'curmax':
                if not self.__int_check(value):
                    return
                
                self.__driver_current_max(alias, int(value))
                
            else:
                print("[CONSOLE]: Driver control select not recognised.")
                
        elif root == 'lock':
            if self.__token_len(2):
                return
            
            if self.tokens[1] == 'all':
                for dev in self.devices.keys():
                    self.__print_lock_state(dev)
                return
            
            self.__print_lock_state(self.tokens[1])
            
        elif root == 'max':
            if self.__token_len(2):
                return
            
            if self.tokens[1] == 'all':
                for dev in self.devices.keys():
                    self.__mxma(dev)
                return
            
            self.__mxma(self.tokens[1])
            
        elif root == 'list':
            self.__list_devs()
            
        elif root == 'help':
            self.__print_help()
            
        else:
            print("[CONSOLE]: Command not found. Type \"help\".")
                    
        
    def __dial(self, port, alias):
        if alias in self.devices.keys():
            print("[CONSOLE]: Already connected to", alias)
            return 
        
        self.devices[alias] = sf8.SF8xxx(port)
        
        if not self.devices[alias].connected:
            print("Failed to connect to", port)
        
        print(self.devices[alias].serial_no, "connected on", 
              self.devices[alias].port, end='. ')
        print("Driver:", "OFF" if self.devices[alias].driver_off else "ON",
              "TEC:", "OFF" if self.devices[alias].tec_off else "ON")
        
        
    def __hang_up(self, alias):
        if alias not in self.devices.keys():
            print("[CONSOLE]: Device", alias, "not connected")
            return
        
        print("Disconnecting", 
              self.devices[alias].serial_no, "from", self.devices[alias].port)
        
        self.devices[alias].dev.close()
        self.devices[alias] = 0
        
        
    def __clean_devices(self):
        for alias in list(self.devices.keys()):
            if self.devices[alias] == 0:
                del self.devices[alias]               
        
        
    def __qrd(self, alias):
        """
        Quick rundown of device status
        """
        self.__is_driver_on(alias)
        self.__print_dri_current(alias)
        self.__print_dri_current_setpoint(alias)
        self.__print_dri_current_max(alias)
        
        self.__is_tec_on(alias)
        self.__print_tec_current_actual(alias)
        self.__print_temperature(alias)
        
        
    def __qrrd(self, alias):
        """
        Quicker rundown. Just prints driver, tec current (most important)
        """
        self.__print_dri_current(alias)
        self.__print_tec_current_actual(alias)
        
        
    def __mxma(self, alias):
        """
        Print maxima for a device
        """
        self.__print_dri_current_max(alias)
        self.__print_tec_current_max(alias)

    
    def __print_tec_current_actual(self, alias):
        cur_actual = self.devices[alias].get_tec_current()
        print("\tTEC =", cur_actual, "A")
        
        
    def __print_tec_current_max(self, alias):
        cur_max = self.devices[alias].get_tec_current_limit()
        print("\tTEC Max =", cur_max, "A")

        
    def __print_dri_current(self, alias):
        dri_cur = self.devices[alias].get_driver_current()
        print("\tValue =", dri_cur, "mA")
    
    
    def __print_dri_current_max(self, alias):
        dri_max = self.devices[alias].get_driver_current_max()
        print("\tMax =", dri_max, "mA")
    
    
    def __print_dri_current_setpoint(self, alias):
        dri_setpoint = self.devices[alias].get_driver_value()
        print("\tSetpoint =", dri_setpoint, "mA")
    
    
    def __print_temperature(self, alias):
        temp = self.devices[alias].get_tec_temperature()
        print("\tTemp =", temp, "C")
    
    
    def __configure(self, alias):
        self.devices[alias].set_tec_int()
        self.devices[alias].set_driver_state()


    def __tec_set(self, alias, value):
        if value == 'on':
            self.__tec_on(alias)
            
        elif value == 'off':
            self.__tec_off(alias)
            
        else:
            print("[CONSOLE]: Driver set code unrecognised")
            
            
    def __tec_on(self, alias):
        if self.devices[alias].set_tec_on():
            print(alias + ':', "failed to set TEC on!")
        
        
    def __is_tec_on(self, alias):
        tec = self.devices[alias].tec_on()
        
        print("TEC:\t\t", "ON" if tec else "OFF")
        
    
    def __tec_off(self, alias):
        ret = self.devices[alias].set_tec_off()
        if ret == 'driver':
            print(alias + ':', "Driver is on!")
        if ret:
            print(alias + ':', "failed to set TEC off!")
            
    
    def __tec_temp(self, alias, value: int):
        self.devices[alias].set_tec_temperature(value)
        
        
    def __print_tec_state(self, alias):
        tec, temp, enable = self.devices[alias].tec_state()
        
        print("TEC:\t\t", "ON" if tec else "OFF")
        print("Temp set:\t\t", "INT" if temp else "EXT")
        print("Enable:\t\t", "INT" if enable else "EXT")
        
        
    def __driver_set(self, alias, value):
        if value == 'on':
            self.__driver_on(alias)
            
        elif value == 'off':
            self.__driver_off(alias)
            
        else:
            print("[CONSOLE]: Driver set code unrecognised")
        
        
    def __driver_on(self, alias):
        ret = self.devices[alias].set_driver_on()
        if ret == 'tec':
            print(alias + ':', "TEC is off!")
        if ret:
            print(alias + ':', "failed to set driver on!")
        
        
    def __is_driver_on(self, alias):
        driver = self.devices[alias].driver_on()
        
        print("Driver:\t\t", "ON" if driver else "OFF")
        
        
    def __driver_off(self, alias):
        if self.devices[alias].set_driver_off():
            print(alias + ':', "failed to set driver on!")
    
    
    def __driver_current(self, alias, value: int):
        self.devices[alias].set_driver_current(value)
        
    
    def __driver_current_max(self, alias, value: int):
        self.devices[alias].set_driver_current_max(value)
        
        
    def __print_driver_state(self, alias):
        device, driver, current, enable, ntc, interlock = \
        self.devices[alias].driver_state()
        
        print("Device:\t\t", "ON" if device else "OFF")
        print("Driver:\t\t", "ON" if driver else "OFF")
        print("Current:\t\t", "INT" if current else "EXT")
        print("Enable:\t\t", "INT" if enable else "EXT")
        print("NTC int.:\t\t", "DENY" if ntc else "ALLOW")
        print("Interlock:\t\t", "DENY" if interlock else "ALLOW")

    
    def __print_lock_state(self, alias):
        interlock, ld_overct, ld_overheat, ntc, tec_error, tec_selfheat = \
        self.devices[alias].lock_state()
                
        print("Interlock:\t\t", "ON" if interlock else "OFF")
        print("LD OC:\t\t", "ON" if ld_overct else "OFF")
        print("LD OH:\t\t", "ON" if ld_overheat else "OFF")
        print("NTC ext.:\t\t", "ON" if ntc else "OFF")
        print("TEC err.:\t\t", "ON" if tec_error else "OFF")
        print("TEC SH:\t\t", "ON" if tec_selfheat else "OFF")
        
    
    def __list_devs(self):
        for k, v in self.devices.items():
            print(k, "on", v.port)

        
    def __token_len(self, length: int):
        if len(self.tokens) != length:
            print("[CONSOLE]: Incorrect number of parameters. Expected", 
                  length)
            return True
        
        
    def __check(self, alias):
        if alias == 'all':
            return True
        
        if alias not in self.devices.keys():
            print("[CONSOLE]: Requested device is not connected. Try \"list\".")
            return False

        return True
    
    
    def __int_check(self, x):
        try:
            int(x)
        except ValueError:
            print("[CONSOLE]: Value not recognised. Want: integer.")
            return False
        
        return True
    
    
    def __print_intro(self):
        print("SF8xxx controller 1.0")
        
        
    def __print_help(self):
        print("Software for Maiman Electronics SF8xxx diode controllers.")
        print("Commands:")
        print("dial [port] [device] - Connect device at [port], addressable by [device].")
        print("hangup [device] - Disconnect this device.")
        print("qrd [device] - Quick RunDown of device status.")
        print("configure [device] - Set device registers for easy lab use.")
        print("tec set [device] [on/off] - Turn TEC of [device] on or off.")
        print("tec temp [device] [temperature, C] - Set TEC temperature of [device].")
        print("dri set [device] [on/off] - Turn driver of [device] on or off.")
        print("dri cur(max) [device] [current, mA] - Set (max) driver current of [device].")
        print("dri/tec on/stat [device] - Driver/TEC of [device] on? Or print status register contents.")
        print("lock [device] - Print [device] register contents for lock status.")
        print("max [device] - Print [device] current maxima.")
        print("list - Print a list of connected devices with ports.")
        print("exit - Exit program.")
        print("[device] = \"all\" to perform the command for all devices (except for dial and driver current routines).")
        print("Author: Douglas McCulloch, May 2024")
        
# Console()