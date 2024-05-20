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
                    dev.qrd()
                return
            
            print(self.tokens[1] + ':')
            self.devices[str(self.tokens[1])].qrd()
            
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
            if self.__token_len(4):
                return
            
            sel = self.tokens[1]  # set/temp
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
                
                self.__tec_temp(alias, int(value))
                
            else:
                print("[CONSOLE]: TEC control select not recognised.")
                
        elif root == 'dri':
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
        
        print("[CONSOLE]: ", self.devices[alias].serial_no, "connected on", 
              self.devices[alias].port)
        
        
    def __hang_up(self, alias):
        if alias not in self.devices.keys():
            print("[CONSOLE]: Device", alias, "not connected")
            return
        
        print("[CONSOLE]: Disconnecting", self.devices[alias].serial_no, "from",
              self.devices[alias].port)
        
        self.devices[alias].dev.close()
        self.devices[alias] = 0
        
        
    def __clean_devices(self):
        for alias in list(self.devices.keys()):
            if self.devices[alias] == 0:
                del self.devices[alias]               
        
    
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
        self.devices[alias].set_tec_on()
        
    
    def __tec_off(self, alias):
        self.devices[alias].set_tec_off()
            
    
    def __tec_temp(self, alias, value: int):
        self.devices[alias].set_tec_temperature(value)
        
        
    def __driver_set(self, alias, value):
        if value == 'on':
            self.__driver_on(alias)
            
        elif value == 'off':
            self.__driver_off(alias)
            
        else:
            print("[CONSOLE]: Driver set code unrecognised")
        
        
    def __driver_on(self, alias):
        self.devices[alias].set_driver_on()
        
        
    def __driver_off(self, alias):
        self.devices[alias].set_driver_off()
        
    
    def __driver_current(self, alias, value: int):
        self.devices[alias].set_driver_current(value)
        
    
    def __driver_current_max(self, alias, value: int):
        self.devices[alias].set_driver_current_max(value)

    
    def __list_devs(self):
        for k, v in self.devices.items():
            print("[CONSOLE]:", k, "on", v.port)

        
    def __token_len(self, length: int):
        if len(self.tokens) != length:
            print("[CONSOLE]: Incorrect number of parameters. Expected", length)
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
        print("SF8xxx controller.")
        
        
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
        print("list - Print a list of connected devices with ports.")
        print("exit - Exit program.")
        print("[device] = \"all\" to perform the command for all devices (except for dial and driver current routines).")
        print("Author: Douglas McCulloch, May 2024")
        
# Console()